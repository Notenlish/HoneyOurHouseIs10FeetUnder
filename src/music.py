import pygame


class Music:
    def __init__(self) -> None:
        self.music_inp = {"game": "music.ogg", "lost": "sad.ogg"}
        self.music = {}

        self.load_music()

    def load_music(self):
        for name, path in self.music_inp.items():
            path = f"assets/music/{path}"
            self.music[name] = path
            # SDL only allows you to keep 1 music file in memory
            # so loading multiple music at once without playing is useless
            # unless you use pygame.mixer.Sound() but meh
            # pygame.mixer.music.load(path)

    def play_music(self, name, loops=-1, start=0, fade_ms=10):
        pygame.mixer.music.unload()
        path = self.music[name]
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops, start, fade_ms)
