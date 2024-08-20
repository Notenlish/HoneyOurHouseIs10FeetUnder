from typing import TYPE_CHECKING

import math

import pygame

from src.block import Block, WoodenSquare, WoodenLongRect, PlasticCircle, SteelFrame

from src.card import Card

if TYPE_CHECKING:
    from main import App


class Game:
    def __init__(self, app: "App") -> None:
        self.app = app
        self.camera = self.app.camera
        self.highscore = 0
        self.physics = self.app.physics

        self.blocks = []
        self.blocks_i = 0
        self.cur_block: Block = None
        self.obj_rot = 0

        self.card = None

        self.started = False
        self.lost = False
        self.score_per_second = 1

    def increase_score(self, dt):
        if self.started:
            self.highscore += dt * self.score_per_second

    def start(self):
        self.started = True
        self.lost = False
        self.app.music.play_music("game", fade_ms=10)
        self.camera.go_up_time = 0

    def restart(self):
        self.started = False
        self.lost = False
        self.camera.go_up_time = 0
        self.highscore = 0
        new = self.app.physics.kinematics.copy()
        for k in new:
            self.app.physics.remove_kinematic(k)
        self.app.physics.kinematics = []
        self.app.music.stop()

    def end(self):
        self.started = False
        self.lost = True
        self.app.music.play_music("lost")

    def rotate_block(self, v: int):
        MUL = 10
        self.obj_rot += MUL * v  # deg
        self.obj_rot %= 360

    def set_block(self, card: Card, block: Block):
        self.card = card
        self.blocks = [block]
        self.cur_block = block
        self.blocks_i = 0

    def change_block(self, v: int):
        return
        self.blocks_i = v
        self.blocks_i %= len(self.blocks)
        self.cur_block = self.blocks[self.blocks_i]

    def hover_block(self, screen: pygame.Surface, mpos: tuple[int, int]):
        if not self.blocks:
            return
        pos = self.app.camera.to_game(mpos)
        pos = [pos.x, pos.y]
        block = self.cur_block(pos, degrees=self.obj_rot)
        self.physics.set_hover_obj(block)

        # normally we wouldnt need to convert to game pos
        # However the physics func for drawing hover obj uses the __get_rotated func which converts from gamepos to display pos
        # so its just doing a -> b -> a
        # its bad, IK.

    def spawn_block(self, mpos: tuple[int, int]):
        if not self.blocks:
            return
        self.app.ui.spawned(self.card)
        pos = self.app.camera.to_game(mpos)
        pos = [pos.x, pos.y]
        block = self.cur_block(pos, degrees=self.obj_rot)
        self.physics.add_kinematic(block)

        self.blocks = []
        self.cur_block = None
        self.physics.set_hover_obj(None)
        self.card = None
        if not self.started:
            self.start()
