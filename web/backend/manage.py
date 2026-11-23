#!/usr/bin/env python
"""Django command-line entry point for OsdagBridge web backend."""
import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django is required for the web backend. Install the web backend requirements first."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
