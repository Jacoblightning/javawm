# JavaWM

A tiling window manager written in Java.

## Building

### Docker Build

JavaWM can be easily built using docker.
However, this is not recommended for developers as, upon any code change, the whole build process must be repeated without caches.

Also be aware that the resulting jar may not run if your system differs significantly from the build container.

The following is one-liner to build a jar in the `target` directory:

```bash
IIDF=$(mktemp -u); sudo docker build --iidfile $IIDF .; sudo docker run --rm -v ./target:/output -it $(cat $IIDF); unset IIDF
```

### Manual Build

Before you try to build the project, make sure you have `jextract` installed. Note that Java 21 does not include the `jextract` tool and you need to install it separately. The build script will fail if it is not installed. Note that SDKMAN! only ships `jextract` for Java 22. Therefore, you need to download `jextract` from the official Java website for Java 21. Then, you can extract it to a directory of your choice and manually install it with SDKMAN!.

Next, you need to install the system-wide Xlib headers. If you run Debian, the proper command would be `sudo apt install libx11-dev`.

The build script written in Python can help you generate the Panama bindings for Xlib and build the project.

```bash
./build.py generate
./build.py package
```
