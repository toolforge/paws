import json
import os
import errno
import importlib.util
from unittest.mock import patch

import pytest

spec = importlib.util.spec_from_file_location(
    "maintain_dumps_nfs",
    os.path.join(os.path.dirname(__file__), "maintain-dumps-nfs.py"),
)
mdn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mdn)

SAMPLE_MOUNTINFO_NFS = (
    "1 2 3:4 / / rw,relatime shared:1 - ext4 /dev/root rw\n"
    "5 6 7:8 /mnt/nfs/dumps /mnt/nfs/dumps rw,noatime shared:2 - nfs4 server:/ rw,soft,noatime\n"
    "9 10 11:12 /public/dumps /public/dumps rw,relatime shared:3 - ext4 /dev/sda1 rw\n"
)


class TestIsNfsMounted:
    def test_returns_true_when_nfs_mounted(self):
        with patch.object(mdn, "read_mountinfo", return_value=SAMPLE_MOUNTINFO_NFS.splitlines(keepends=True)):
            assert mdn.is_nfs_mounted("/mnt/nfs/dumps") is True


class TestCheckMountHealthy:
    def test_returns_false_on_stale_handle(self):
        def raiser(_):
            raise OSError(errno.ESTALE, os.strerror(errno.ESTALE))

        with (
            patch.object(mdn, "is_nfs_mounted", return_value=True),
            patch.object(mdn.os, "listdir", side_effect=raiser),
        ):
            assert mdn.check_mount_healthy("test", {"host_path": "/mnt/nfs/dumps"}) is False

    def test_returns_false_on_ls_failure(self):
        def raiser(_):
            raise OSError("some error")

        with (
            patch.object(mdn, "is_nfs_mounted", return_value=True),
            patch.object(mdn.os, "listdir", side_effect=raiser),
        ):
            assert mdn.check_mount_healthy("test", {"host_path": "/mnt/nfs/dumps"}) is False


class TestEnsureCompatSymlinks:
    def test_creates_missing_symlink(self):
        os_err = OSError()
        os_err.errno = errno.ENOENT
        with (
            patch.object(mdn, "load_config", return_value={"compatSymlinks": ["old-name"]}),
            patch.object(mdn.os, "readlink", side_effect=os_err),
            patch.object(mdn.os.path, "isdir"),
            patch.object(mdn.os, "symlink") as mock_symlink,
        ):
            mdn.ensure_compat_symlinks("/host/mnt/nfs")
            mock_symlink.assert_called_once_with("dumps", "/host/mnt/nfs/old-name")

    def test_updates_wrong_symlink(self):
        with (
            patch.object(mdn, "load_config", return_value={"compatSymlinks": ["old-name"]}),
            patch.object(mdn.os, "readlink", return_value="wrong-target"),
            patch.object(mdn.os, "unlink") as mock_unlink,
            patch.object(mdn.os, "symlink") as mock_symlink,
        ):
            mdn.ensure_compat_symlinks("/host/mnt/nfs")
            mock_unlink.assert_called_once_with("/host/mnt/nfs/old-name")
            mock_symlink.assert_called_once_with("dumps", "/host/mnt/nfs/old-name")

    def test_removes_empty_dir(self):
        os_err = OSError()
        os_err.errno = errno.EINVAL
        with (
            patch.object(mdn, "load_config", return_value={"compatSymlinks": ["old-name"]}),
            patch.object(mdn.os, "readlink", side_effect=os_err),
            patch.object(mdn.os.path, "isdir", return_value=True),
            patch.object(mdn.os, "listdir", return_value=[]),
            patch.object(mdn.os, "rmdir") as mock_rmdir,
            patch.object(mdn.os, "symlink") as mock_symlink,
        ):
            mdn.ensure_compat_symlinks("/host/mnt/nfs")
            mock_rmdir.assert_called_once_with("/host/mnt/nfs/old-name")
            mock_symlink.assert_called_once_with("dumps", "/host/mnt/nfs/old-name")

    def test_skips_non_empty_dir(self):
        os_err = OSError()
        os_err.errno = errno.EINVAL
        with (
            patch.object(mdn, "load_config", return_value={"compatSymlinks": ["old-name"]}),
            patch.object(mdn.os, "readlink", side_effect=os_err),
            patch.object(mdn.os.path, "isdir", return_value=True),
            patch.object(mdn.os, "listdir", return_value=["file.txt"]),
            patch.object(mdn.os, "rmdir") as mock_rmdir,
            patch.object(mdn.os, "symlink") as mock_symlink,
        ):
            mdn.ensure_compat_symlinks("/host/mnt/nfs")
            mock_rmdir.assert_not_called()
            mock_symlink.assert_not_called()


class TestEnsurePublicDumpsSymlink:
    def test_skips_when_symlink_exists(self):
        with (
            patch.object(mdn.os, "readlink", return_value="/mnt/nfs/dumps"),
            patch.object(mdn.os, "symlink") as mock_symlink,
            patch.object(mdn.os, "makedirs") as mock_mkdir,
        ):
            mdn.ensure_public_dumps_symlink()
            mock_symlink.assert_not_called()
            mock_mkdir.assert_not_called()

    def test_creates_when_missing(self):
        os_err = OSError()
        os_err.errno = errno.ENOENT
        with (
            patch.object(mdn.os, "readlink", side_effect=os_err),
            patch.object(mdn.os.path, "isdir"),
            patch.object(mdn.os, "makedirs") as mock_mkdir,
            patch.object(mdn.os, "symlink") as mock_symlink,
        ):
            mdn.ensure_public_dumps_symlink()
            mock_mkdir.assert_called_once_with("/host/public/dumps", exist_ok=True)
            mock_symlink.assert_called_once_with("/mnt/nfs/dumps", "/host/public/dumps/public")

    def test_errors_when_path_is_directory(self):
        os_err = OSError()
        os_err.errno = errno.EINVAL
        with (
            patch.object(mdn.os, "readlink", side_effect=os_err),
            patch.object(mdn.os.path, "isdir", return_value=True),
            patch.object(mdn.os, "symlink") as mock_symlink,
            patch.object(mdn.os, "makedirs") as mock_mkdir,
        ):
            mdn.ensure_public_dumps_symlink()
            mock_symlink.assert_not_called()
            mock_mkdir.assert_not_called()


class TestMountHost:
    def test_creates_dir_and_mounts(self):
        with (
            patch.object(mdn.os, "makedirs") as mock_mkdir,
            patch.object(mdn.subprocess, "run") as mock_run,
        ):
            mdn.mount_host("nfs.example.com", "/mnt/nfs/test")
            mock_mkdir.assert_called_once_with("/mnt/nfs/test", exist_ok=True)
            mock_run.assert_called_once_with(
                ["mount", "-t", "nfs", "-o", mdn.MOUNT_OPTIONS, "nfs.example.com:", "/mnt/nfs/test"],
                capture_output=True, text=True, check=True,
            )


class TestReadMountinfo:
    def test_returns_lines_when_file_exists(self):
        with patch("builtins.open") as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_value = ["line1\n", "line2\n"]
            result = mdn.read_mountinfo()
            assert result == ["line1\n", "line2\n"]

    def test_returns_empty_when_file_missing(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = mdn.read_mountinfo()
            assert result == []


class TestLoadConfig:
    def test_loads_existing_config(self, tmp_path):
        config_dir = tmp_path / "etc" / "maintain-dumps-nfs"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "maintain-dumps-nfs.json"
        config_file.write_text(json.dumps({"enabled": True, "server": "test.example.com"}))
        with patch.object(mdn, "CONFIG_PATH", str(config_dir)):
            assert mdn.load_config() == {"enabled": True, "server": "test.example.com"}

    def test_raises_when_config_missing(self, tmp_path):
        config_dir = tmp_path / "etc" / "maintain-dumps-nfs"
        config_dir.mkdir(parents=True)
        with patch.object(mdn, "CONFIG_PATH", str(config_dir)):
            with pytest.raises(FileNotFoundError):
                mdn.load_config()
