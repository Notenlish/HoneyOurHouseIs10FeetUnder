# /// script
# dependencies = [
#  "pymunk",
#  "numpy",
#  "cffi"
# ]
# ///

import asyncio


import pygame

# fmt:off
import _cffi_backend
import pymunk
import pymunk.pygame_util
# Idk if I need to spesifically import pymunk even tho I defined it at the top,
# but just to be sure...
# fmt:on

from src.physics import PhysicsManager
from src.block import Block

import sys

from src.constants import SC_SIZE, SC_WIDTH, SC_HEIGHT, WEB, DEBUG, COLORKEY
from src.game import Game
from src.ui import UI
from src.camera import Camera

from src.background import Background


class App:
    def __init__(self) -> None:
        if WEB:
            self.screen = pygame.display.set_mode(SC_SIZE)
        else:
            try:
                self.screen = pygame.display.set_mode(
                    SC_SIZE, pygame.SCALED | pygame.RESIZABLE, vsync=True
                )
            except pygame.error:
                self.screen = pygame.display.set_mode(
                    SC_SIZE, pygame.SCALED | pygame.RESIZABLE, vsync=False
                )
        self.screen.set_colorkey(COLORKEY)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.fps = 0
        self.frame = 0
        self.elapsed_time = 0

        # self.debug_options = pygame_util.DrawOptions(self.screen)

        self.camera = Camera()

        self.physics = PhysicsManager(self)

        self.game = Game(self)
        self.ui = UI(self)

        self.bg = Background(self)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.game.spawn_block(pygame.mouse.get_pos())
                if pygame.mouse.get_pressed()[0]:
                    self.ui.click_card(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEWHEEL:
                self.game.rotate_block(event.y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.game.change_block(0)
                elif event.key == pygame.K_F1:
                    self.camera.scroll.y += 100
                elif event.key == pygame.K_2:
                    self.game.change_block(1)
                elif event.key == pygame.K_3:
                    self.game.change_block(2)
                elif event.key == pygame.K_4:
                    self.game.change_block(3)
                elif event.key == pygame.K_5:
                    self.game.change_block(4)
                elif event.key == pygame.K_6:
                    self.game.change_block(5)

    def update(self):
        # if fps low, only update every 2nd frame so it can get faster
        if self.fps < 45:
            if self.frame % 2:
                self.physics.update(1 / 35)
        else:
            self.physics.update(self.dt)
        # is this overengineering? Or just too complicated?
        # dunno

        self.game.hover_block(self.screen, pygame.mouse.get_pos())
        self.ui.update(self.dt)
        self.bg.update(self.dt)

    def draw(self):
        self.screen.fill("#94b1ed")
        self.physics.draw(self.screen, self.elapsed_time)
        # self.physics.space.debug_draw(self.debug_options)
        self.ui.draw(self.screen)
        self.bg.draw(self.screen)

    def fps_limit(self):
        self.frame += 1
        self.dt = self.clock.tick(60) / 1000
        self.elapsed_time += self.dt
        self.fps = 1 / self.dt

        # if fps goes below 30, limit dt so calculations dont get broken
        self.dt = min(self.dt, 1 / 30)

    async def run(self):
        while True:
            self.input()
            self.update()
            self.draw()

            self.fps_limit()

            pygame.display.update()
            await asyncio.sleep(0)


if __name__ == "__main__":
    app = App()
    asyncio.run(app.run())
