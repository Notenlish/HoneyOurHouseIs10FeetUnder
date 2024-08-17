# /// script
# dependencies = [
#  "pygame",
#  "pymunk"
# ]
# ///

import asyncio


import pygame
# fmt:off
import pymunk
# fmt:on
from pymunk import pygame_util

from src.physics import PhysicsManager
from src.block import Block

import sys

from src.constants import SC_SIZE, SC_WIDTH, SC_HEIGHT, WEB
from src.game import Game
from src.ui import UI

pygame_util.positive_y_is_up = False


class App:
    def __init__(self) -> None:
        if WEB:
            self.screen = pygame.display.set_mode(SC_SIZE)
        else:
            try:
                self.screen = pygame.display.set_mode(SC_SIZE, pygame.SCALED | pygame.RESIZABLE, vsync=True)
            except pygame.error:
                self.screen = pygame.display.set_mode(SC_SIZE, pygame.SCALED | pygame.RESIZABLE, vsync=False)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.fps = 0
        self.frame = 0
        
        self.debug_options = pygame_util.DrawOptions(self.screen)
        
        self.physics = PhysicsManager()
        self.physics.add_kinematic(
            Block(position=(SC_WIDTH/2,0), size=[10, 50])
        )
        
        self.game = Game(self)
        self.ui = UI(self)
 
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game.spawn_block(pygame.mouse.get_pos())
    
    def update(self):
        # if fps low, only update every 2nd frame so it can get faster
        if self.fps < 45:
            if self.frame % 2:
                self.physics.update(1 / 30)
        else:
            self.physics.update(self.dt)
        # is this overengineering? Or just too complicated?
        # dunno
    
    def draw(self):
        self.screen.fill("black")
        self.physics.draw(self.screen)
        # self.physics.space.debug_draw(self.debug_options)
        self.ui.draw(self.screen)
    
    def fps_limit(self):
        self.frame += 1
        self.dt = self.clock.tick(60) / 1000
        self.fps = 1 / self.dt
        
        # if fps goes below 30, limit dt so calculations dont get broken
        self.dt = min(self.dt, 1/30)
    
    async def run(self):
        while True:
            self.input()
            self.update()
            self.draw()
            
            self.fps_limit()
            
            pygame.display.update()
            await asyncio.sleep(0)

if __name__ == '__main__':
    app = App()
    asyncio.run(app.run())