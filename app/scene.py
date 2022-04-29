import pygame

from app.events import UE_GAME_QUIT


class Scene:

    GAME_EVENTS = [pygame.QUIT, UE_GAME_QUIT]

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def get_scene_events(self):
        return pygame.event.get(exclude=Scene.GAME_EVENTS)

    def process(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def on_blur(self):
        pass

    def on_focus(self):
        pass