from typing import TYPE_CHECKING

import math
import random

if TYPE_CHECKING:
    from main import App

import pygame

from src.constants import SC_WIDTH, SC_HEIGHT
from src.util import render_text_to
from src.card import Card
from src.block import WoodenSquare, WoodenLongRect, SteelFrame, PlasticSquare, IceBlock
from src.apartments import SingularApartment, Villa, FamilyHome


from copy import deepcopy


class UI:
    def __init__(self, app: "App") -> None:
        self.app = app
        self.font = pygame.Font("assets/font/pixelmix.ttf", 20)
        self.small_font = pygame.Font("assets/font/pixelmix.ttf", 10)

        self.card_bg = pygame.image.load("assets/card/card.png").convert()

        self.available: list[Card] = [
            Card(self.card_bg, "Wood\nSquare", WoodenSquare, sort_val=100),
            Card(self.card_bg, "Wood\nRect", WoodenLongRect, sort_val=200),
            Card(self.card_bg, "Steel\nFrame", SteelFrame, sort_val=300),
            Card(self.card_bg, "Plastic\nSquare", PlasticSquare, sort_val=400),
            Card(self.card_bg, "Ice\nBlock", IceBlock, sort_val=500),
            # Card(self.card_bg, self.small_font, "Singular", SingularApartment),
            # Card(self.card_bg, self.small_font, "Villa", Villa),
            # Card(self.card_bg, self.small_font, "Family", FamilyHome),
        ]
        self.cards: list[Card] = []

    def update(self, dt):
        self.hover_card(pygame.mouse.get_pos(), dt)

        if len(self.cards) == 0:
            self.spawn_cards()

    def spawn_cards(self):
        for _ in range(10):
            i = round(random.random() * (len(self.available) - 1))
            c = deepcopy(self.available[i])
            self.cards.append(c)

        self.cards = sorted(self.cards, key=lambda x: x.text)

    def spawned(self, card):
        self.cards.remove(card)

    def click_card(self, mpos):
        changed = False
        for card in self.cards:
            if card.moved_rect.collidepoint(mpos) and not card.held:
                card.held = True
                changed = True
                self.app.game.set_block(card, card.block)
            else:
                card.held = False
        return changed

    def draw(self, screen: pygame.Surface):
        self.draw_highscore(screen)
        self.draw_cards(screen)

        if self.app.game.lost:
            render_text_to(self.font, screen, (50, 50), "Press R To restart", "black")

    def draw_cards(self, screen: pygame.Surface):
        if not self.cards or not len(self.cards):
            return
        first_card = self.cards[0]
        card_w = pygame.Vector2(first_card.rect.w, 0)
        center = pygame.Vector2(SC_WIDTH // 2, SC_HEIGHT - (first_card.rect.h / 2))
        # pos = center.copy()
        card_count = len(self.cards)
        for i, card in enumerate(self.cards):
            to_center = math.ceil(i / 2)
            _dir = -1 if i % 2 == 0 else 1
            pos = center + card_w * 1.05 * to_center * _dir  # 1.05 ==> add spacing
            card.set_center(pos)

            card.draw(screen, self.small_font)

    def hover_card(self, mpos, dt):
        for i, card in enumerate(self.cards):
            card.set_hover(mpos)
            card.update(dt)

    def draw_highscore(self, screen: pygame.Surface):
        text = f"Score: {self.app.game.highscore:.0f}"
        rect = self.font.render(text, False, "white").get_rect()
        rect.centerx = SC_WIDTH / 2
        render_text_to(self.font, screen, rect.topleft, text, "white")
