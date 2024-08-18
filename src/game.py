from typing import TYPE_CHECKING

import pygame

from src.block import Block

if TYPE_CHECKING:
    from main import App


class Game:
    def __init__(self, app: "App") -> None:
        self.app = app
        self.highscore = 0
        self.physics = self.app.physics

        self.cur_block = Block

    def hover_block(self, screen: pygame.Surface, mpos: tuple[int, int]):
        block = self.cur_block(mpos, [24, 24], degrees=0)
        self.physics.set_hover_obj(block)

    def spawn_block(self, mpos: tuple[int, int]):
        block = self.cur_block(mpos, [24, 24], degrees=0)
        self.physics.add_kinematic(block)
