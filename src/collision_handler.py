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
            self.sounds.play_random_sound("wood_crumble")
            # TODO: play collapse sound
            # also delete the object bcuz it collapsed
            pass
        return True

    def wood_steel_col(self, arbiter, space, data):
        self.sounds.play_random_sound("wood")
        return True

    def ice_ice_col(self, arbiter, space, data):
        self.sounds.play_random_sound("ice")
        return True

    def ice_ground_col(self, arbiter,space,data):
        self.sounds.play_random_sound("ice")
        return True

    def ice_wood_col(self, arbiter, space, data):
        self.sounds.play_random_sound("ice")
        return True

    def ice_steel_col(self, arbiter, space, data):
        self.sounds.play_random_sound("ice")
        return True

    def steel_steel_col(self, arbiter, space, data):
        self.sounds.play_random_sound("steel")
        return True

    def steel_wood_col(self, arbiter, space, data):
        self.sounds.play_random_sound("steel")
        return True

    def steel_ground_col(self, arbiter, space, data):
        self.sounds.play_random_sound("steel")
        return True

    def add_handler(self, func, type1, type2):
        handler = self.physics.space.add_collision_handler(type1, type2)
        handler.begin = func

    def init_handlers(self):
        self.add_handler(self.wood_ground_col, COLLTYPE_WOOD, COLLTYPE_GROUND)
        self.add_handler(self.wood_wood_col, COLLTYPE_WOOD, COLLTYPE_WOOD)
        self.add_handler(self.wood_steel_col, COLLTYPE_WOOD, COLLTYPE_METAL)
        self.add_handler(self.plastic_ground_col, COLLTYPE_PLASTIC, COLLTYPE_GROUND)
        self.add_handler(self.plastic_plastic_col, COLLTYPE_PLASTIC, COLLTYPE_PLASTIC)
        self.add_handler(self.plastic_wood_col, COLLTYPE_PLASTIC, COLLTYPE_WOOD)
        self.add_handler(self.ice_wood_col, COLLTYPE_ICE, COLLTYPE_WOOD)
        self.add_handler(self.ice_steel_col, COLLTYPE_ICE, COLLTYPE_METAL)
        self.add_handler(self.ice_ice_col, COLLTYPE_ICE, COLLTYPE_ICE)
        self.add_handler(self.ice_ground_col, COLLTYPE_ICE, COLLTYPE_GROUND)
        self.add_handler(self.steel_steel_col, COLLTYPE_METAL, COLLTYPE_METAL)
        self.add_handler(self.steel_wood_col, COLLTYPE_METAL, COLLTYPE_WOOD)
        self.add_handler(self.steel_ground_col, COLLTYPE_METAL, COLLTYPE_GROUND)

        # todo: use | operator for colltypes so I dont have to have a bajillion functions to play sounds
