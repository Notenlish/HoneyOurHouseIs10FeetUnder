import pymunk

from math import radians
from random import random

from src.constants import SC_WIDTH, SC_HEIGHT

class Block:
    def __init__(self, position, size, degrees=0, friction=0.5) -> None:
        self.body = pymunk.Body()
        self.body.position = position
        self.body.angle = radians(degrees + random())
        # TODO: Test different radiuses to see whether blocks get stuck or not
        self.poly = pymunk.Poly.create_box(self.body, size=size, radius=1)
        self.poly.mass = 10
        self.poly.friction = friction

class StaticBlock(Block):
    def __init__(self, center, size, friction: float = 0.5) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.poly = pymunk.Poly.create_box(self.body, size=size)
        self.body.position = center
        self.poly.friction = friction


class Square(Block):
    def __init__(self, position, size, degrees=0, friction=0.5) -> None:
        super().__init__(position, size, degrees, friction)
