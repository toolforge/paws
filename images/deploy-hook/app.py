from functools import partial
import subprocess
import uuid
import tornado.ioloop
import tornado.web
import tempfile
import os
import base64
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
    def initialize(self, auth_token):
        self.auth_token = auth_token

    def prepare(self):
        super().prepare()
        auth_header = self.request.headers.get('Authorization', '')
        if auth_header != 'Bearer {}'.format(self.auth_token):
            raise tornado.web.HTTPError(403)

    def post(self):
        repo = self.get_argument('repo')
        commit = self.get_argument('commit')
        release = self.get_argument('release')
        # We might lose some '+' (part of base64) into spaces from our
        # POST processing. Put 'em back.
        crypt_key = base64.standard_b64decode(self.get_argument('crypt-key').replace(' ', '+'))
        with tempfile.TemporaryDirectory() as git_dir:
            for line in execute_cmd([
                    'git',
                    'clone',
                    '--recursive',
                    repo,
                    git_dir
            ]):
                self.write(line)

            os.chdir(git_dir)

            for line in execute_cmd(['git', 'reset', '--hard', commit]):
                self.write(line)
                self.flush()

            with open('key', 'wb') as f:
                f.write(crypt_key)

            for line in execute_cmd(['git', 'crypt', 'unlock', 'key']):
                self.write(line)
                self.flush()

            for line in execute_cmd([
                    './build.py',
                    'deploy',
                    release
            ]):
                self.write(line)
                self.flush()

if __name__ == "__main__":
    auth_token = os.environ['DEPLOY_HOOK_TOKEN']
    app = tornado.web.Application([
        (r"/deploy", DeployHandler,
         {'auth_token': auth_token}),
    ])
    app.listen(8888)
    enable_pretty_logging()
    tornado.ioloop.IOLoop.current().start()
