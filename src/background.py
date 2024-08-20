from typing import TYPE_CHECKING

import random

if TYPE_CHECKING:
    from main import App

import pygame

from src.constants import SC_HEIGHT, SC_WIDTH, COLORKEY


class Cloud:
    def __init__(self, bg_manager: "Background", spr: pygame.Surface, starty) -> None:
        self.bg_manager = bg_manager
        self.camera = bg_manager.camera
        self.spr = spr
        self.rect = spr.get_frect()
        self.rect.top = starty
        self.rect.left = random.random() * SC_WIDTH
        self.speed = 10 + random.randint(0, 10)

    def update(self, dt: float):
        self.rect.move_ip(dt * self.speed, 0)

        if self.rect.left > (SC_WIDTH + 10):
            self.rect.right = -5

    def draw(self, screen: pygame.Surface):
        pos = self.camera.to_display(self.rect.topleft)
        pos.y %= SC_HEIGHT * 3  # in case the user goes higher than 10 meters lol
        screen.blit(self.spr, pos)


class Background:
    def __init__(self, app: "App") -> None:
        self.app = app
        self.camera = app.camera
        self.sprites = []
        for file in [f"cloud{i}.png" for i in range(1, 5 + 1)]:
            spr = pygame.image.load(f"assets/bg/{file}").convert()
            spr.set_colorkey(COLORKEY)
            self.sprites.append(spr)

        self.clouds: list[Cloud] = []
        for ring in [0, 1, 2, 3]:
            for _ in range(14):
                spr_i = round(random.random() * (len(self.sprites) - 1))
                spr = self.sprites[spr_i]
                starty = (
                    SC_HEIGHT * (0.2) - ring * SC_HEIGHT * 0.7 + random.randint(-20, 20)
                )
                self.clouds.append(Cloud(self, spr, starty))

    def update(self, dt: float):
        for cloud in self.clouds:
            cloud.update(dt)

    def draw(self, screen):
        for cloud in self.clouds:
            cloud.draw(screen)
