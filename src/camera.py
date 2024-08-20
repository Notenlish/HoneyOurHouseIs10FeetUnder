from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App

import pygame


from src.constants import SC_WIDTH, SC_HEIGHT


class Camera:
    def __init__(self, app: "App", scroll=pygame.Vector2()) -> None:
        self.app = app
        self.scroll = scroll
        self.go_up_time = 0

    def get_game_rect(self) -> pygame.Rect:
        """Returns a rect containing a rect for the viewable area(in game coords)"""
        r = pygame.Rect(0, 0, SC_WIDTH, SC_HEIGHT)
        r.topleft -= self.scroll
        return r

    def __move_cam(self):
        segments = [
            {"val": max(self.go_up_time - 10, 0), "mul": 2},
            {"val": max(self.go_up_time - 20, 0), "mul": 4},
            {"val": max(self.go_up_time - 50, 0), "mul": 6},
            {"val": max(self.go_up_time - 80, 0), "mul": 10},
        ]

        if False:
            # testing purposes
            segments = [
                {"val": max(self.go_up_time - 5, 0), "mul": 2},
                {"val": max(self.go_up_time - 10, 0), "mul": 4},
                {"val": max(self.go_up_time - 20, 0), "mul": 6},
                {"val": max(self.go_up_time - 30, 0), "mul": 10},
            ]
        self.scroll.y = 0
        for segment in segments:
            v = segment["val"]
            mul = segment["mul"]
            self.scroll.y += v * mul

    def go_up_auto(self, dt):
        if True:
            if self.app.game.started:
                self.go_up_time += dt
            if self.app.game.lost:
                self.go_up_time -= dt * 3
        else:
            self.go_up_time += dt * 5
        self.__move_cam()

    def to_game(self, pos):
        if type(pos) != pygame.Vector2:
            pos = pygame.Vector2(*pos)
        return pos - self.scroll

    def to_display(self, pos):
        if type(pos) != pygame.Vector2:
            pos = pygame.Vector2(*pos)
        return pos + self.scroll
