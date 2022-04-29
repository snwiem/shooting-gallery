from typing import Any

import pygame

from app.assets import AssetManager


class FrameRate(pygame.sprite.Sprite):

    TEXT_COLOR = pygame.Color('white')
    FONT_ID = "future_narrow"
    FONT_SIZE = 12

    def __init__(self, groups, clock: pygame.time.Clock):
        super().__init__(groups)
        self.clock = clock
        self.font = AssetManager.get_instance().get_font(FrameRate.FONT_ID, FrameRate.FONT_SIZE)
        self.image = self.font.render("", False, FrameRate.TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.last_fps = 0

    def update(self):
        current_fps = round(self.clock.get_fps(), 1)
        if current_fps != self.last_fps:
            self.image = self.font.render(f"FPS: {current_fps}", True, FrameRate.TEXT_COLOR)
            self.last_fps = current_fps


