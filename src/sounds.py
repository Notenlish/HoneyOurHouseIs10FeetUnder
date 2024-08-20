import os
import random

import pygame


class Sounds:
    def __init__(self) -> None:
        self.sounds = {}

        self.define_sound("wood", "wood")
        self.define_sound("plastic", "plastic")

    def define_sound(self, name, folder):
        self.sounds[name] = []
        for f in os.listdir(f"assets/sounds/{folder}"):
            file = os.path.join(f"./assets/sounds/{folder}/{f}")
            if not os.path.isfile(file):
                continue
            if not file.endswith(".ogg"):
                raise Exception("Ogg istiyom ulan.")
            self.sounds[name].append(pygame.mixer.Sound(file))

    def get_random_sound(self, name) -> pygame.mixer.Sound:
        random_i = random.randint(0, len(self.sounds[name]) - 1)
        return self.sounds[name][random_i]

    def play_random_sound(self, name):
        self.get_random_sound(name).play()
