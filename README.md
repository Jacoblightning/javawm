# JavaWM

A tiling window manager written in Java.
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/machineswillrise/javawm)

## Building

### Docker Build
JavaWM can be easily built using Docker. However, this is not recommended for developers, as, upon any code change, the whole build process must be repeated without caches. You can use the following command to build a JAR into `target`:

```bash
IIDF=$(mktemp -u); sudo docker build --iidfile $IIDF .; sudo docker run --rm -v ./target:/output -it $(cat $IIDF); unset IIDF
```

The Dockerfile doesn't use SDKMAN! since it would just add bloat for the container.

### Manual Build
First, install Java 21, either using SDKMAN! or from your distribution's repository. Please only report issues if you are using standard OpenJDK or Temurin! These JDK builds are open-source and known to be the most stable.

Before you try to build the project, make sure you have `jextract` installed. Note that Java 21 does not include the `jextract` tool and you need to install it separately. The build script will fail if it is not installed. Note that SDKMAN! only ships `jextract` for Java 22. Therefore, you need to download `jextract` from the official Java website for Java 21. Then, you can extract it to a directory of your choice and manually install it with SDKMAN!. Alternatively, if you don't use SDKMAN, just add it to your `$PATH`.

Next, you need to install the system-wide Xlib headers. If you run Debian, the proper command would be `sudo apt install libx11-dev`.

The build script written in Python can help you generate the Panama bindings for Xlib and build the project. It calls `jextract` under the hood along with all the required symbols and can also start the Maven build process. Symbols are **whitelist only** instead of generating bindings for everything inside Xlib since `jextract` errors on some parts of it. You can use it like this:

```bash
./build.py generate
./build.py package
```

The project loads the libx11 shared library during runtime. It finds the proper one according to the computer architecture. Therefore, it will only work on a Unix-like system.

### Running
A fat JAR will be outputted in `target`. When you run it, make sure to enable native access or you'll get a warning. Make sure to kill any X11 Window managers you have open.

### Roadmap
1. Moving windows to different sides of the screen with the keyboard
2. Virtual desktops
3. Config loading from home directory
4. EWMH? Not sure how complicated compliance with it is.

### License
This project is licensed under the Unlicense. Therefore, you can use it without attribution and modify it as you wish, and even use it commercially.

### Credits
- Thank you @Jacoblightning for adding better error handling to the Python build script and adding Docker build support.
