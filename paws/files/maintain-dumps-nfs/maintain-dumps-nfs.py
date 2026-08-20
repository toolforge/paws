"""Daemon that mounts the dumps NFS export on each node and keeps it healthy.

Runs as a DaemonSet with Bidirectional mount propagation so the mount is
visible on the host.  Also manages clouddumps100[12]-compat symlinks within
/mnt/nfs.

Similar to dumps-nfs-client-sitter in the puppet repo, but differs in that it
also manages symlinks as opposed to puppet in production.

/mnt/nfs is then bind-mounted from the host into singleuser pods by the
jupyterhub spawner.
"""

import errno
import json
import logging
import os
import subprocess
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("maintain-dumps-nfs")

CONFIG_PATH = "/etc/maintain-dumps-nfs"

MOUNT_OPTIONS = "ro,fg,soft,tcp,noatime,lookupcache=all,nofsc,timeo=20,retrans=1"

DUMPS_MOUNT = "/host/mnt/nfs/dumps"


def load_config():
    """Load daemonset config from the configmap JSON file.

    The config file is authoritative and must be present.
    """
    config_file = os.path.join(CONFIG_PATH, "maintain-dumps-nfs.json")
    try:
        with open(config_file) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.critical("Config file %s not found", config_file)
        raise


def read_mountinfo():
    """Read the container's own mount table from /proc/self/mountinfo."""
    try:
        with open("/proc/self/mountinfo") as f:
            return f.readlines()
    except FileNotFoundError:
        logger.error("Cannot read /proc/self/mountinfo")
        return []


def is_nfs_mounted(mount_point):
    """Check whether an NFS filesystem is mounted at mount_point."""
    for line in read_mountinfo():
        parts = line.split()
        if len(parts) < 10:
            continue
        try:
            sep = parts.index("-")
        except ValueError:
            continue
        fstype = parts[sep + 1]
        mp = parts[4]
        if mp == mount_point and fstype in ("nfs", "nfs4"):
            return True
    return False


def check_mount_healthy(mount_name, mount_info):
    """Check that the NFS mount exists, is accessible, and is not stale."""
    host_path = mount_info["host_path"]
    if not is_nfs_mounted(host_path):
        logger.warning("Mount %s (%s) not present", mount_name, host_path)
        return False
    try:
        os.listdir(host_path)
    except OSError as e:
        if e.errno == errno.ESTALE:
            logger.warning("Mount %s (%s) has ESTALE", mount_name, host_path)
        else:
            logger.warning("Mount %s (%s) unhealthy: %s", mount_name, host_path, e)
        return False
    logger.debug("Mount %s (%s) is healthy", mount_name, host_path)
    return True


def umount_host(mount_point):
    """Force-unmount a filesystem."""
    logger.info("Unmounting %s", mount_point)
    try:
        subprocess.run(["umount", "-f", mount_point], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.warning("umount failed: %s", e.stderr.strip())


def mount_host(server, mount_point):
    """Mount an NFS export. The mount propagates to the host via Bidirectional propagation."""
    logger.info("Mounting %s on %s", server, mount_point)
    os.makedirs(mount_point, exist_ok=True)
    try:
        subprocess.run(
            ["mount", "-t", "nfs", "-o", MOUNT_OPTIONS, f"{server}:", mount_point],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.warning("mount failed: %s", e.stderr.strip())


def ensure_compat_symlinks(host_mnt_nfs):
    """Create or repair compat symlinks inside the NFS mount root based on config."""
    config = load_config()
    compat_symlinks = config.get("compatSymlinks", [])
    for name in compat_symlinks:
        link_path = os.path.join(host_mnt_nfs, name)
        target = "dumps"
        current_target = None
        try:
            current_target = os.readlink(link_path)
        except OSError as e:
            if e.errno == errno.ENOENT:
                logger.info("Compat symlink %s missing — creating", link_path)
            elif os.path.isdir(link_path):
                try:
                    entries = os.listdir(link_path)
                except OSError:
                    entries = []
                if entries:
                    logger.warning(
                        "Compat symlink %s is a non-empty directory — skipping",
                        link_path,
                    )
                    continue
                logger.info(
                    "Compat symlink %s is an empty directory — removing",
                    link_path,
                )
                try:
                    os.rmdir(link_path)
                except OSError:
                    logger.warning("Failed to remove empty directory %s", link_path)
            else:
                logger.warning("Cannot read symlink %s: %s", link_path, e)
                continue
        if current_target != target:
            if current_target is not None:
                logger.info(
                    "Compat symlink %s points to %s, updating to %s",
                    link_path, current_target, target,
                )
                try:
                    os.unlink(link_path)
                except OSError:
                    logger.warning("Failed to remove symlink %s", link_path)
            try:
                os.symlink(target, link_path)
            except OSError as e:
                logger.warning("Failed to create symlink %s -> %s: %s", link_path, target, e)
        else:
            logger.debug("Compat symlink %s -> %s ok", link_path, target)


def main():
    """Mount NFS dumps, create compat symlinks, then loop for health checks and remounts."""
    config = load_config()
    logger.info("Config: %s", json.dumps(config, default=str))

    server = config["server"]
    mount_info = {"host_path": DUMPS_MOUNT}

    ensure_compat_symlinks("/host/mnt/nfs")

    while True:
        if not is_nfs_mounted(DUMPS_MOUNT):
            logger.info("Mount dumps-src (%s) not present — mounting", DUMPS_MOUNT)
            mount_host(server, DUMPS_MOUNT)
        elif not check_mount_healthy("dumps-src", mount_info):
            logger.info("Mount dumps-src (%s) unhealthy — remounting", DUMPS_MOUNT)
            umount_host(DUMPS_MOUNT)
            time.sleep(2)
            if not is_nfs_mounted(DUMPS_MOUNT):
                mount_host(server, DUMPS_MOUNT)
        time.sleep(60)


if __name__ == "__main__":
    main()
