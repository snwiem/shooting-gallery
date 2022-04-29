import logging
import sys

import pygame as pygame

from app.assets import AssetManager
from app.events import UE_GAME_QUIT
from app.scene import Scene
from app.scenes.title import TitleScene
from app.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, FRAMES_PER_SECOND


class Game:

    def __init__(self):
        pygame.init()
        self.running = False
        self.screen = None
        self.clock = None
        self.scene = None
        self.asset_manager = AssetManager.get_instance()
        self.init_core()
        self.init_screen()
        self.init_scene()


    def init_core(self):
        self.clock = pygame.time.Clock()

    def init_screen(self):
        self.screen =pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        # TODO: add icon

    def init_scene(self):
        self.scene = TitleScene(self.screen)

    def do_exit(self):
        self.running = False
        pygame.quit()
        sys.exit(0)

    def run(self):
        self.running = True
        while self.running:
            self.scene.process()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    logging.info("Received pygame.QUIT")
                    self.do_exit()
                    break
                if ev.type == UE_GAME_QUIT:
                    logging.info("Received UE_GAME_QUIT")
                    self.do_exit()
                    break
            self.scene.update()
            self.scene.draw()

            self.clock.tick(FRAMES_PER_SECOND)
            pygame.display.flip()
