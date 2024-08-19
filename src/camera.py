import pygame


class Camera:
    def __init__(self, scroll=pygame.Vector2()) -> None:
        self.scroll = scroll

    def to_game(self, pos):
        if type(pos) != pygame.Vector2:
            pos = pygame.Vector2(*pos)
        return pos - self.scroll

    def to_display(self, pos):
        if type(pos) != pygame.Vector2:
            pos = pygame.Vector2(*pos)
        return pos + self.scroll
