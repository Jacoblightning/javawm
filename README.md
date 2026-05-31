# JavaWM

A tiling window manager written in Java.

## Building
Before you try to build the project, make sure you have `jextract` installed. Note that Java 21 does not include the `jextract` tool and you need to install it separately. The build script will fail if it is not installed. Note that SDKMAN! only ships `jextract` for Java 22. Therefore, you need to download `jextract` from the official Java website for Java 21. Then, you can extract it to a directory of your choice and manually install it with SDKMAN!.

Next, you need to install the system-wide Xlib headers. If you run Debian, the proper command would be `sudo apt install libx11-dev`.

The build script written in Python can help you generate the Panama bindings for Xlib and build the project. It also includes the ability to run the project directly from the command line.

```bash
./build.py generate
./build.py package
```