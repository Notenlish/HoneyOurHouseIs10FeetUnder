import random

import pygame

from src.constants import SC_HEIGHT, SC_WIDTH, COLORKEY


class Cloud:
    def __init__(self, spr: pygame.Surface, starty=SC_HEIGHT * (0.2)) -> None:
        self.spr = spr
        self.rect = spr.get_frect()
        self.rect.top = starty
        self.rect.left = random.random() * SC_WIDTH
        self.speed = 10 + random.randint(0, 10)

    def update(self, dt: float):
        self.rect.move_ip(dt * self.speed, 0)

        if self.rect.left > (SC_WIDTH + 10):
            self.rect.right = 5

    def draw(self, screen: pygame.Surface):
        screen.blit(self.spr, self.rect.topleft)


class Background:
    def __init__(self) -> None:
        self.sprites = []
        for file in [f"cloud{i}.png" for i in range(1, 5 + 1)]:
            spr = pygame.image.load(f"assets/bg/{file}").convert()
            spr.set_colorkey(COLORKEY)
            self.sprites.append(spr)

        self.clouds: list[Cloud] = []
        for _ in range(10):
            spr_i = round(random.random() * (len(self.sprites) - 1))
            spr = self.sprites[spr_i]
            self.clouds.append(Cloud(spr))

    def update(self, dt: float):
        for cloud in self.clouds:
            cloud.update(dt)

    def draw(self, screen):
        for cloud in self.clouds:
            cloud.draw(screen)
