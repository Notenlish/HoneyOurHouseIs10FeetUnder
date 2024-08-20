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
    WOOD_WOOD_SOUND_IMPULSE,
)


class CollisionHandler:
    def __init__(self, physics: "PhysicsManager") -> None:
        self.physics = physics
        self.app = self.physics.app
        self.sounds = self.app.sounds

        self.init_handlers()

    def plastic_ground_col(self, arbiter, space, data):
        arbiter: pymunk.Arbiter = arbiter
        self.sounds.play_random_sound("plastic")
        return True

    def plastic_wood_col(self, arbiter, space, data):
        arbiter: pymunk.Arbiter = arbiter
        self.sounds.play_random_sound("plastic")
        return True

    def plastic_plastic_col(self, arbiter, space, data):
        arbiter: pymunk.Arbiter = arbiter
        self.sounds.play_random_sound("plastic")
        return True

    def wood_wood_col(self, arbiter, space, data):
        arbiter: pymunk.Arbiter = arbiter
        self.sounds.play_random_sound("wood")
        return True

    def wood_ground_col(self, arbiter, space, data):
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
        self.add_handler(self.wood_wood_col, COLLTYPE_WOOD, COLLTYPE_WOOD)
        self.add_handler(self.plastic_ground_col, COLLTYPE_PLASTIC, COLLTYPE_GROUND)
        self.add_handler(self.plastic_plastic_col, COLLTYPE_PLASTIC, COLLTYPE_PLASTIC)
        self.add_handler(self.plastic_wood_col, COLLTYPE_PLASTIC, COLLTYPE_WOOD)
