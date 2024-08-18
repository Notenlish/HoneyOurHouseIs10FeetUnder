from typing import TYPE_CHECKING

import pygame

from src.block import WoodenSquare, WoodenLongRect, PlasticCircle, SteelFrame

if TYPE_CHECKING:
    from main import App


class Game:
    def __init__(self, app: "App") -> None:
        self.app = app
        self.highscore = 0
        self.physics = self.app.physics

        self.blocks = [WoodenSquare, WoodenLongRect, PlasticCircle, SteelFrame]
        self.blocks_i = 0
        self.cur_block = self.blocks[self.blocks_i]

    def change_block(self, v: int):
        self.blocks_i += v
        self.blocks_i %= len(self.blocks)
        self.cur_block = self.blocks[self.blocks_i]

    def hover_block(self, screen: pygame.Surface, mpos: tuple[int, int]):
        block = self.cur_block(mpos)
        self.physics.set_hover_obj(block)

    def spawn_block(self, mpos: tuple[int, int]):
        block = self.cur_block(mpos)
        self.physics.add_kinematic(block)
