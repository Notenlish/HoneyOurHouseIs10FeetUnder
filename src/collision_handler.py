from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.physics import PhysicsManager


import pymunk


from src.constants import (
    COLLTYPE_WOOD,
    COLLTYPE_GROUND,
    COLLTYPE_ICE,
    COLLTYPE_METAL,
    COLLTYPE_PLASTIC,
    COLLAPSE_IMPULSE,
)


class CollisionHandler:
    def __init__(self, physics: "PhysicsManager") -> None:
        self.physics = physics
        self.app = self.physics.app
        self.sounds = self.app.sounds

        self.init_handlers()

    def wood_ground_col(self, arbiter, space, data):
        # print(arbiter, data)
        # pov: type hints
        arbiter: pymunk.Arbiter = arbiter
        if arbiter.is_first_contact:
            self.sounds.play_random_sound("wood")
        if arbiter.total_impulse.length >= COLLAPSE_IMPULSE:
            print("WOW, building collapsed")
            # TODO: play collapse sound
            # also delete the object bcuz it collapsed
            pass
        return True

    def add_handler(self, func, type1, type2):
        handler = self.physics.space.add_collision_handler(type1, type2)
        handler.begin = func

    def init_handlers(self):
        self.add_handler(self.wood_ground_col, COLLTYPE_WOOD, COLLTYPE_GROUND)
