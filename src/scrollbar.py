import pygame

from src.constants import SC_WIDTH, SC_HEIGHT


class HoldButton:
    def __init__(self, rect) -> None:
        self.rect = rect
        self.held = False


class Scrollbar:
    def __init__(self) -> None:
        topright = pygame.Vector2(SC_WIDTH, SC_HEIGHT)
        topright += pygame.Vector2(-20, 10)

        self.button = HoldButton(pygame.Rect(*topright, (30, 20)))
        self.bar = pygame.Rect(topright, (10, SC_HEIGHT))

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, "black", self.button.rect, 2)
        pygame.draw.rect(screen, "black", self.bar.rect, 2)
