#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
from typing import Dict


def print_error(*args, **kwargs) -> None:
    return print("\033[91m[ERROR]\033[0m", *args, file=sys.stderr, **kwargs)


def check_for_output(output_dir: str) -> bool:
    return os.path.exists(output_dir)


def generate_bindings(output_dir: str, environment_variables: Dict[str, str]) -> int:
    try:
        subprocess.run(
            [
                "jextract",
                "-I", "/usr/include",
                "--output", output_dir,
                "--target-package", "io.github.machineswillrise.javawm.xlib",
                "--source", "/usr/include/X11/Xlib.h",
                "--include-function", "XOpenDisplay",
                "--include-function", "XDefaultScreen",
                "--include-function", "XCloseDisplay",
            ],
            env=environment_variables,
        )
    except FileNotFoundError:
        print_error("Please install jextract to generate bindings.")
        return 1
    else:
        return 0


def clean_bindings(output_dir: str) -> int:
    try:
        shutil.rmtree(output_dir)
    except FileNotFoundError:
        print_error("Output directory does not exist.")
        return 1
    return 0


def package_project() -> int:
    try:
        subprocess.run(["mvn", "package"])
    except FileNotFoundError:
        print_error("Please install maven to package this project.")
        return 1
    else:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, dest="command")

    generate_parser = subparsers.add_parser(
        "generate", help="generate the Panama bindings for Xlib"
    )
    generate_parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite build directory if exists"
    )
    generate_parser.add_argument(
        "--output",
        "-o",
        help="Bindings output directory",
        default="target/generated-sources/jextract",
    )

    clean_parser = subparsers.add_parser(
        "clean", help="clean the build files and bindings"
    )
    clean_parser.add_argument(
        "--output",
        "-o",
        help="Bindings directory to clean",
        default="target/generated-sources/jextract",
    )

    package_parser = subparsers.add_parser(
        "package", help="build and package the project"
    )

    args = parser.parse_args()

    env = os.environ.copy()
    env["JDK_JAVA_OPTIONS"] = "--enable-native-access=org.openjdk.jextract"

    match args.command:
        case "generate":
            if check_for_output(args.output):
                if args.force:
                    clean_bindings(args.output)
                else:
                    print_error("Output directory already exists")
                    return 1
            return generate_bindings(args.output, env)
        case "clean":
            clean_bindings(args.output)
        case "package":
            package_project()
    return 0


if __name__ == "__main__":
    exit(main())
