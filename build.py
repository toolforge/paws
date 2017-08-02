#!/usr/bin/python3
import os
import argparse
import subprocess


def last_git_modified(path):
    return subprocess.check_output([
        'git',
        'log',
        '-n', '1',
        '--pretty=format:%H',
        path
    ]).decode('utf-8')

def build_images(prefix, images, push=False):
    for image in images:
        image_name = prefix + image
        image_path = os.path.join('images', image)
        tag = last_git_modified(image_path)
        image_name = '{}:{}'.format(image_name, tag[:6])
        subprocess.check_call([
            'docker', 'build', '-t', image_name, image_path
        ])
        if push:
            subprocess.check_call([
                'docker', 'push', image_name
            ])


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

    args = argparser.parse_args()

    build_images(args.image_prefix, ['singleuser'], args.push)

main()

