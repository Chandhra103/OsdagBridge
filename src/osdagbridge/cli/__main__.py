"""Command-line interface for project-file utilities."""
from __future__ import annotations

import argparse
from collections.abc import Sequence

from osdagbridge.cli.commands import analyze_cmd, init_cmd, inspect_cmd, validate_cmd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="osdagbridge-cli",
        description="Create, validate, and inspect starter OsdagBridge JSON project files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create a starter JSON project file")
    init_parser.add_argument("path", help="destination path ending in .json")
    init_parser.add_argument("--force", action="store_true", help="replace an existing file")

    for name, help_text in (
        ("validate", "check the lightweight project-file schema"),
        ("inspect", "print basic project metadata"),
        ("analyze", "analysis is not currently available in the CLI"),
    ):
        command_parser = subparsers.add_parser(name, help=help_text)
        command_parser.add_argument("path", help="JSON project file")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "init":
        return init_cmd(args.path, force=args.force)
    if args.command == "validate":
        return validate_cmd(args.path)
    if args.command == "inspect":
        return inspect_cmd(args.path)
    if args.command == "analyze":
        return analyze_cmd(args.path)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
