import logging
import sys

import pygame as pygame

from app.assets import AssetManager
from app.events import UE_GAME_QUIT, UE_GAME_START, UE_GAME_STOP
from app.scene import Scene
from app.scenes.stall import StallScene
from app.scenes.title import TitleScene
from app.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, FRAMES_PER_SECOND
from app.ui import FrameRate


class Game:

    def __init__(self):
        pygame.init()
        self.running = False
        self.screen = None
        self.clock = None
        self.scene = None
        self.ui_group = None
        self.asset_manager = AssetManager.get_instance()
        self.init_core()
        self.init_screen()
        self.init_ui()

    def init_ui(self):
        self.ui_group = pygame.sprite.Group()
        FrameRate(self.ui_group, self.clock)

    def init_core(self):
        self.clock = pygame.time.Clock()

    def init_screen(self):
        self.screen =pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        # TODO: add icon

    def set_scene(self, scene: Scene):
        if self.scene:
            self.scene.on_blur()
        self.scene = scene
        self.scene.on_focus()

    def do_exit(self):
        self.running = False
        pygame.quit()
        sys.exit(0)

    def run(self):
        self.running = True
        self.set_scene(TitleScene(self.screen))
        while self.running:
            self.scene.process()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.do_exit()
                    break
                if ev.type == UE_GAME_QUIT:
                    self.do_exit()
                    break
                if ev.type == UE_GAME_START:
                    self.set_scene(StallScene(self.screen))
                    break
                if ev.type == UE_GAME_STOP:
                    self.set_scene(TitleScene(self.screen))
            self.scene.update()
            self.scene.draw()
            self.ui_group.update()
            self.ui_group.draw(self.screen)

            self.clock.tick(FRAMES_PER_SECOND)
            pygame.display.flip()
