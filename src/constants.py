import pygame
import sys

WEB = sys.platform in ("emscripten", "wasi")
DEBUG = False
SC_SIZE = SC_WIDTH, SC_HEIGHT = 640, 360

COLORKEY = (255, 16, 240)


# meh, wrong file but who cares
class Cache:
    def __init__(self) -> None:
        self._cache = {}
        # 0.0 to 1.1
        self.sizes = [i / 10 for i in range(11 + 1)]

    def add_cache(self, name, spr):
        # cache already exists
        if self._cache.get(name, False):
            return
        self._cache[name] = {}
        # TODO: measure cache size, increase step size to like 10
        for size in self.sizes:
            self._cache[name][size] = {}
            for rot in range(0, 360 + 1, 1):
                rotated = pygame.transform.rotozoom(spr, rot, size)
                surf = pygame.Surface(rotated.get_size())
                surf.fill(COLORKEY)
                rotated.set_colorkey((0, 0, 0))
                surf.blit(rotated)
                surf.set_colorkey(COLORKEY)

                self._cache[name][size][rot] = surf

    def get_cache(self, name, size, rot):
        cached_rot = round(rot % 360)
        cached_size = round(size * 10) / 10
        spr:pygame.Surface = self._cache[name][cached_size][cached_rot]
        return spr, cached_rot


CACHE = Cache()
