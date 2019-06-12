import os
import argparse

ROOT_DIR: str = os.path.dirname(
    os.path.dirname(__file__)
)


def parse_cli_args(args=None):
    """
    Parse command line arguments.
    Note:
        `arg` here is for using in unit tests only

    """
    arg_parser = argparse.ArgumentParser(
        description="Start"
    )

    arg_parser.add_argument(
        '-n', '--non-build',
        default=15,
    )

    arg_parser.add_argument(
        '-b', '--build',
        default=5,
    )

    arg_parser.add_argument(
        '-c', '--consumers',
        default=15,
    )

    arg_parser.add_argument(
        '-p', '--file-path',
        default=os.path.join(ROOT_DIR, 'input_data.txt')
    )

    arg_parser.add_argument(
        '-r', '--range-file-path',
        default=os.path.join(ROOT_DIR, 'range.txt')
    )

    arg_parser.add_argument(
        '-i', '--input-type',
        default='range'
    )

    arg_parser.add_argument(
        '-e', '--evaluating-type',
        default='single'
    )

    return arg_parser.parse_args(args)
