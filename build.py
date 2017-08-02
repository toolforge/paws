#!/usr/bin/python3
import os
import argparse
import subprocess


def last_git_modified(path):
    return subprocess.check_output([
        'git',
        'log',
        '-n', '1',
        '--pretty=format:%h',
        path
    ]).decode('utf-8')

def build_images(prefix, images, push=False):
    for image in images:
        image_path = os.path.join('images', image)
        tag = last_git_modified(image_path)
        image_spec = '{}{}:{}'.format(prefix, image, tag)
        subprocess.check_call([
            'docker', 'build', '-t', image_spec, image_path
        ])
        if push:
            subprocess.check_call([
                'docker', 'push', image_spec
            ])

def deploy(prefix, images):
    image_map = {
        'singleuser': 'jupyterhub.singleuser.image',
        'db-proxy': 'dbProxy.image',
        'query-killer': 'query-killer.image'
    }

    args = []

    for image in images:
        image_path = os.path.join('images', image)
        image_name = prefix + image
        tag = last_git_modified(image_path)
        args.append('--set={}.name={}'.format(image_map[image], image_name))
        args.append('--set={}.tag={}'.format(image_map[image], tag))

    print(' '.join(
        ['helm', 'upgrade', 'paws-prod', 'paws/', '-f', 'secrets.yaml'] + args
    ))


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--image-prefix',
        default='quay.io/wikimedia-paws/'
    )
    argparser.add_argument(
        '--push',
        action='store_true'
    )

    argparser.add_argument(
        'action',
        choices={'build', 'deploy'}
    )

    args = argparser.parse_args()

    images = ['singleuser', 'db-proxy', 'query-killer']
    if args.action == 'build':
        build_images(args.image_prefix, images, args.push)
    else:
        deploy(args.image_prefix, images)

main()
