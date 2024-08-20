import pygame


from src.constants import SC_WIDTH, SC_HEIGHT


class Camera:
    def __init__(self, scroll=pygame.Vector2()) -> None:
        self.scroll = scroll

    def get_game_rect(self) -> pygame.Rect:
        """Returns a rect containing a rect for the viewable area(in game coords)"""
        r = pygame.Rect(0, 0, SC_WIDTH, SC_HEIGHT)
        r.topleft = self.scroll
        return r

    def go_up_auto(self, elapsed_time):
        segments = [
            {"val": max(elapsed_time - 10, 0), "mul": 2},
            {"val": max(elapsed_time - 20, 0), "mul": 4},
            {"val": max(elapsed_time - 50, 0), "mul": 8},
            {"val": max(elapsed_time - 80, 0), "mul": 12},
        ]
        self.scroll.y = 0
        for segment in segments:
            v = segment["val"]
            mul = segment["mul"]
            self.scroll.y += v * mul

    def to_game(self, pos):
        if type(pos) != pygame.Vector2:
            pos = pygame.Vector2(*pos)
        return pos - self.scroll

    def to_display(self, pos):
        if type(pos) != pygame.Vector2:
            pos = pygame.Vector2(*pos)
        return pos + self.scroll
