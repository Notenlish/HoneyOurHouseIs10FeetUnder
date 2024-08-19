import math

from typing import Literal

import pygame
import pymunk

from math import radians

from src.constants import SC_WIDTH, SC_HEIGHT, COLORKEY, CACHE


class Block:
    def __init__(
        self,
        position,
        size,
        degrees=0,
        friction=0.5,
        mass=10,
        color="red",
        outline="black",
        body_type=pymunk.Body.DYNAMIC,
        shape_type: Literal["poly", "circle"] = "poly",
        radius: int = None,
        sprite_name: str = None,
        dont_cache=False,
    ) -> None:
        self.body = pymunk.Body(body_type=body_type)
        self.body.position = position
        self.body.angle = radians(degrees)
        if shape_type == "poly":
            self.shape_type = "poly"
            self.poly = pymunk.Poly.create_box(self.body, size=size, radius=1)
        elif shape_type == "circle":
            self.shape_type = "circle"
            self.poly = pymunk.Circle(self.body, radius=radius)

        self.sprite_name = sprite_name
        if self.sprite_name is None:
            self.sprite_name = "assets/block/not_found.png"
        else:
            self.sprite_name = f"assets/block/{self.sprite_name}"
        self.sprite = pygame.image.load(self.sprite_name).convert()

        self.sprite.set_colorkey(COLORKEY)

        self.dont_cache = dont_cache
        if not self.dont_cache:
            CACHE.add_cache(self.sprite_name, self.sprite)

        self.poly.mass = mass
        self.poly.friction = friction
        self.color = color
        self.outline = outline
        self.spr_size = 1.0

    def get_spr(self):
        if not self.dont_cache:
            spr, _ = CACHE.get_cache(
                self.sprite_name, self.spr_size, math.degrees(-self.body.angle)
            )
            return spr
        else:
            return self.sprite


class StaticBlock(Block):
    def __init__(self, position, size, degrees=0, sprite_name=None) -> None:
        friction = 0.5
        mass = 20
        color = "green"
        outline = "black"
        super().__init__(
            position,
            size,
            degrees,
            friction,
            mass,
            color,
            outline,
            body_type=pymunk.Body.STATIC,
            sprite_name=sprite_name,
            dont_cache=True,
        )


class WoodenSquare(Block):
    def __init__(self, position, degrees=0) -> None:
        size = [24, 24]
        friction = 0.6
        super().__init__(
            position,
            size,
            degrees,
            friction,
            mass=20,
            color="#d9a066",
            sprite_name="small_wood.png",
        )


class WoodenLongRect(Block):
    def __init__(self, position, degrees=0) -> None:
        size = [24, 48]
        friction = 0.6
        mass = 50
        super().__init__(
            position,
            size,
            degrees,
            friction,
            mass,
            color="#d9a066",
            sprite_name="large_wood.png",
        )


class PlasticCircle(Block):
    def __init__(self, position, degrees=0) -> None:
        radius = 36
        friction = 0.4
        mass = 5
        friction = 0.4
        self.color = "#cbdbfc"
        self.outline = "grey"
        super().__init__(
            position,
            [0, 0],
            degrees,
            friction,
            mass,
            self.color,
            self.outline,
            shape_type="circle",
            radius=radius,
            sprite_name="plastic_circle.png",
        )


class SteelFrame(Block):
    def __init__(self, position, degrees=0) -> None:
        size = [16, 48]
        friction = 0.8
        mass = 60
        super().__init__(
            position,
            size,
            degrees,
            friction,
            mass,
            color="#485257",
            sprite_name="steel_frame.png",
        )
