import sys

WEB = sys.platform in ("emscripten", "wasi")
SC_SIZE = SC_WIDTH, SC_HEIGHT = 640, 360