import logging

import pygame

from app.assets import AssetManager
from app.events import UE_GAME_QUIT
from app.scene import Scene
from app.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class TitleScene(Scene):
    BACKGROUND_COLOR = pygame.Color('black')
    TEXT_COLOR = pygame.Color('white')
    TITLE_FONT_ID = "bold"
    TITLE_FONT_SIZE = 32
    SUBTITLE_FONT_ID = "future"
    SUBTITLE_FONT_SIZE = 16

    def __init__(self, screen):
        super().__init__(screen)
        self.assets = AssetManager.get_instance()
        self.title = self.assets.get_font(TitleScene.TITLE_FONT_ID, TitleScene.TITLE_FONT_SIZE).render(
            "Shotting Gallery", True, TitleScene.TEXT_COLOR)
        self.subtitle = self.assets.get_font(TitleScene.SUBTITLE_FONT_ID, TitleScene.SUBTITLE_FONT_SIZE).render(
            "Press 'Enter' to start", True, TitleScene.TEXT_COLOR)
        self.title_pos = (SCREEN_WIDTH / 2 - self.title.get_width() / 2, SCREEN_HEIGHT / 2 - self.title.get_height() / 2 - 25)
        self.subtitle_pos = (SCREEN_WIDTH / 2 - self.subtitle.get_width() / 2, SCREEN_HEIGHT / 2 - self.subtitle.get_height() / 2 + 25)

    def process(self):
        for ev in self.get_scene_events():
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.do_exit()
                    break
            logging.debug(f"Dropping event: {ev}")

    def draw(self):
        self.screen.fill(TitleScene.BACKGROUND_COLOR)
        self.screen.blit(self.title, self.title_pos)
        self.screen.blit(self.subtitle, self.subtitle_pos)

    def do_exit(self):
        pygame.event.post(pygame.event.Event(UE_GAME_QUIT))
