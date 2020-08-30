#!/usr/bin/env python

import argparse
import sys

import latex_ji18n


def build_parser():
    parser = argparse.ArgumentParser(description=latex_ji18n.__description__)
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + latex_ji18n.__version__,
        help="Show program version number and exit.",
    )
    return parser


def parse_options(args):
    parser = build_parser()
    return parser.parse_args(args)


def run(args=[]):
    parse_options(args)

    latex_ji18n.render()

    return 0


if __name__ == "__main__":
    sys.exit(run(args=sys.argv[1:]))
