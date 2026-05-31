#!/usr/bin/env python3
from sys import argv
from typing import List, Dict

import subprocess
import os
import shutil

OUTPUT_DIRECTORY = "target/generated-sources/jextract"

def check_for_output(output_dir: str) -> bool:
	return os.path.exists(output_dir)

def generate_bindings(output_dir: str, environment_variables: Dict[str, str]) -> None:
	subprocess.run(
	  	[
			"jextract",
			"-I", "/usr/include",
			"--output", output_dir,
			"--target-package", "io.github.machineswillrise.javawm.xlib",
			"--source", "/usr/include/X11/Xlib.h",
			"--include-function", "XOpenDisplay",
			"--include-function", "XDefaultScreen",
			"--include-function", "XCloseDisplay"
	  	], env=environment_variables
	)

def clean_bindings(output_dir: str) -> None:
	shutil.rmtree(output_dir)

def package_project() -> None:
	subprocess.run(["mvn", "package"])

def main(argc: int, argv: List[str]) -> int:
	command = argv[1]
	env = os.environ.copy()
	env["JDK_JAVA_OPTIONS"] = "--enable-native-access=org.openjdk.jextract"

	match command:
		case "generate":
			if check_for_output(OUTPUT_DIRECTORY):
				print("Output directory already exists")
				return 1
			generate_bindings(OUTPUT_DIRECTORY, env)
		case "clean":
			clean_bindings(OUTPUT_DIRECTORY)
		case "package":
			package_project()
		case _:
			print("Invalid command")
			return 1
	return 0

if __name__ == "__main__":
	argc = len(argv)
	exit(main(argc, argv))