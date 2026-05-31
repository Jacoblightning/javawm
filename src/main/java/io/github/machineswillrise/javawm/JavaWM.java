package io.github.machineswillrise.javawm;

import java.lang.foreign.MemorySegment;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static io.github.machineswillrise.javawm.xlib.Xlib_h.XCloseDisplay;
import static io.github.machineswillrise.javawm.xlib.Xlib_h.XDefaultScreen;
import static io.github.machineswillrise.javawm.xlib.Xlib_h.XOpenDisplay;

public class JavaWM {
	private static final Logger log = LoggerFactory.getLogger(JavaWM.class);

	static {
		var architecture = System.getProperty("os.arch");
		var libraryToLoad = switch (architecture) {
			case "x86"             -> "/usr/lib/i386-linux-gnu/libX11.so.6";
			case "x86_64", "amd64" -> "/usr/lib/x86_64-linux-gnu/libX11.so.6";
			default                -> "/usr/lib/aarch64-linux-gnu/libX11.so.6";
		};

		System.load(libraryToLoad);
	}

	private static void fatal(String msg) {
		log.error(msg);
		System.exit(1);
	}

	public static void main(String[] args) {
		MemorySegment display = XOpenDisplay(MemorySegment.NULL);
		if (display.equals(MemorySegment.NULL)) {
			fatal("Failed to open display");
		}

		int screen = XDefaultScreen(display);
		log.info("Screen: {}", screen);

		XCloseDisplay(display);
	}
}
