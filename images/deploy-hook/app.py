from functools import partial
import subprocess
import uuid
import tornado.ioloop
import tornado.web
import tempfile
import os
from tornado.log import enable_pretty_logging
def execute_cmd(cmd, **kwargs):
    """
    Call given command, yielding output line by line
    """
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.STDOUT

    proc = subprocess.Popen(cmd, **kwargs)

    # Capture output for logging.
    # Each line will be yielded as text.
    # This should behave the same as .readline(), but splits on `\r` OR `\n`,
    # not just `\n`.
    buf = []
    def flush():
        line = b''.join(buf).decode('utf8', 'replace')
        buf[:] = []
        return line

    c_last = ''
    try:
        for c in iter(partial(proc.stdout.read, 1), b''):
            if c_last == b'\r' and buf and c != b'\n':
                yield flush()
            buf.append(c)
            if c == b'\n':
                yield flush()
            c_last = c
    finally:
        ret = proc.wait()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, cmd)


class DeployHandler(tornado.web.RequestHandler):
    def get(self, user, repo, commit, release):
        with tempfile.TemporaryDirectory() as git_dir:
            for line in execute_cmd([
                    'git',
                    'clone',
                    '--recursive',
                    'https://github.com/{}/{}'.format(user, repo),
                    git_dir
            ]):
                self.write(line)

            os.chdir(git_dir)
            for line in execute_cmd(['git', 'reset', '--hard', commit]):
                self.write(line)

            for line in execute_cmd([
                    './build.py',
                    'deploy',
                    release
            ]):
                self.write(line)

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/deploy/(.*)/(.*)/(.*)/(.*)", DeployHandler),
    ])
    app.listen(8888)
    enable_pretty_logging()
    tornado.ioloop.IOLoop.current().start()
