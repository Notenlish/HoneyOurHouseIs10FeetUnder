from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App

import pygame

from src.constants import SC_WIDTH


class UI:
    def __init__(self, app: "App") -> None:
        self.app = app
        pygame.font.init()
        self.font = pygame.Font("assets/font/pixelmix.ttf", 20)
    
    def render_text_to(self, font, surface:pygame.Surface, pos, text, color, antialias=False, bgcol=None):
        surf = font.render(text, antialias, color, bgcol)
        return surface.blit(surf, pos)
    
    def draw(self, screen: pygame.Surface):
        self.draw_highscore(screen)
    
    def draw_highscore(self, screen:pygame.Surface):
        text = f"Score: {self.app.game.highscore}"
        rect = self.font.render(text, False, "white").get_rect()
        rect.centerx = SC_WIDTH/2
        self.render_text_to(self.font, screen, rect.topleft, text, "white")
