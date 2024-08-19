import pygame


from src.block import Block
from src.util import lerp, ease_in_out, ease_in, ease_out


class Card:
    def __init__(
        self, card_bg: pygame.Surface, block: Block, size=[45, 80], position=[0, 0]
    ) -> None:
        self.bg = card_bg
        self.rect = pygame.Rect(*position, *size)
        self.moved_rect = self.rect.copy()
        self.offset = pygame.Vector2()
        self.hovered = False
        self.held = False
        self.since_hover_raw = 0
        self.since_hover = 0

    def set_hover(self, mpos):
        if self.rect.collidepoint(mpos):
            self.hovered = True
        else:
            self.hovered = False

    def update(self, dt):
        transition_time = 0.4
        if self.hovered:
            self.since_hover_raw += dt
        else:
            self.since_hover_raw -= dt
        self.since_hover_raw = max(0, self.since_hover_raw)

        time_input = self.since_hover_raw * (1 / transition_time)

        self.since_hover = min(time_input, 1)
        self.since_hover = ease_in_out(self.since_hover)

        wanted_offset = pygame.Vector2()
        wanted_offset.y = -30

        self.moved_rect.topleft = pygame.Vector2(
            # weird float inconsistency
            # lerp(self.rect.x, self.rect.move(wanted_offset).x, self.since_hover),
            self.rect.left,
            lerp(self.rect.y, self.rect.move(wanted_offset).y, self.since_hover),
        )

    def set_center(self, pos):
        self.rect.center = pos

    def draw(self, screen: pygame.Surface):
        # pygame.draw.rect(screen, "grey", self.moved_rect)
        # pygame.draw.rect(screen, "black", self.moved_rect, width=2)
        screen.blit(self.bg, self.moved_rect.topleft)
        if self.held:
            pygame.draw.rect(screen, "white", self.moved_rect.inflate(4,4), width=2)
