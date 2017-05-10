import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vendor'))  # noqa


def lambda_handler(event, context):
    print('hello world')


if __name__ == '__main__':
    lambda_handler(None, None)
