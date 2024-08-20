import pygame
import sys

WEB = sys.platform in ("emscripten", "wasi")
DEBUG = False
SC_SIZE = SC_WIDTH, SC_HEIGHT = 640, 360

COLORKEY = (0, 0, 0)

COLLTYPE_GROUND = 1
COLLTYPE_WOOD = 2
COLLTYPE_METAL = 3
COLLTYPE_ICE = 4
COLLTYPE_PLASTIC = 5

COLLAPSE_IMPULSE = 1000
WOOD_WOOD_SOUND_IMPULSE = 50


# meh, wrong file but who cares
class Cache:
    def __init__(self) -> None:
        self._cache = {}
        # 0.0 to 1.1
        self.sizes = [i / 10 for i in range(11 + 1)]
        self.rot_step_size = 5

    def add_cache(self, name, spr):
        # cache already exists
        if self._cache.get(name, False):
            return
        self._cache[name] = {}
        for size in self.sizes:
            self._cache[name][size] = {}
            for rot in range(0, 360 + self.rot_step_size, self.rot_step_size):
                # DONT use rotozoom for colorkey as rotozoom results in weird black artifacts
                # instead rotate and then scale
                rotated = pygame.transform.scale_by(
                    pygame.transform.rotate(spr, rot), size
                )

                self._cache[name][size][rot] = rotated

    def get_cache(self, name, size, rot):
        cached_rot = round(rot / self.rot_step_size) * self.rot_step_size
        cached_rot %= 360
        cached_size = round(size * 10) / 10
        spr: pygame.Surface = self._cache[name][cached_size][cached_rot]
        return spr, cached_rot


CACHE = Cache()
