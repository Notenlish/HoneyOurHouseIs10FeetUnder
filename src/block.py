import pymunk

from math import radians

from src.constants import SC_WIDTH, SC_HEIGHT


class Block:
    def __init__(
        self, position, size, degrees=0, friction=0.5, mass=10, color="red"
    ) -> None:
        self.body = pymunk.Body()
        self.body.position = position
        self.body.angle = radians(degrees)
        # TODO: Test different radiuses to see whether blocks get stuck or not
        self.poly = pymunk.Poly.create_box(self.body, size=size, radius=1)
        self.poly.mass = mass
        self.poly.friction = friction
        self.color = color


class StaticBlock(Block):
    def __init__(self, center, size, friction: float = 0.5) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.poly = pymunk.Poly.create_box(self.body, size=size)
        self.body.position = center
        self.poly.friction = friction
        self.color = "green"


class WoodenSquare(Block):
    def __init__(self, position, degrees=0) -> None:
        size = [24, 24]
        friction = 0.6
        super().__init__(position, size, degrees, friction, mass=20, color="#d9a066")


class WoodenLongRect(Block):
    def __init__(self, position, degrees=0) -> None:
        size = [24, 48]
        friction = 0.6
        mass = 50
        super().__init__(position, size, degrees, friction, mass, color="#d9a066")


class PlasticCircle(Block):
    def __init__(self, position, degrees=0) -> None:
        # I spent like 4 hours trying to figure out an dashed outline algorithm with offset,
        # IK block class can be refactored to be more abstract and so that the classes that subclass it can just use `super()`
        # I dont have enough time for it.
        radius = 36
        friction = 0.4
        mass = 5
        self.body = pymunk.Body()
        self.body.position = position
        self.body.angle = radians(degrees)
        # TODO: Test different radiuses to see whether blocks get stuck or not
        self.poly = pymunk.Circle(self.body, radius)
        self.poly.mass = mass
        self.poly.friction = friction
        self.color = "#cbdbfc"


class SteelFrame(Block):
    def __init__(self, position, degrees=0) -> None:
        size = [16, 48]
        friction = 0.8
        mass = 60
        super().__init__(position, size, degrees, friction, mass, color="#485257")
