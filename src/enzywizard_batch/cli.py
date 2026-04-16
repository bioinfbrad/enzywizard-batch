from __future__ import annotations
import argparse

from .commands.batch import add_batch_parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="enzywizard",
        description="EnzyWizard: an integrated toolkit for enzyme analysis."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_batch_parser(subparsers)


    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)