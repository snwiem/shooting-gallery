import pygame.mouse

from app.assets import AssetManager
from app.events import UE_GAME_STOP
from app.scene import Scene


class Player(pygame.sprite.Sprite):
    SPRITE_CROSSHAIR = "crosshair"
    SOUND_SHOT = "shotgun-fire"

    def __init__(self, groups):
        super().__init__(groups)
        self.shot_sound = AssetManager.get_instance().get_sound(Player.SOUND_SHOT)
        self.image = AssetManager.get_instance().get_sprite(Player.SPRITE_CROSSHAIR)
        self.rect = self.image.get_rect()
        self.can_shoot = True

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        (bt1, bt2, bt3) = pygame.mouse.get_pressed(num_buttons=3)
        if bt1:
            if self.can_shoot:
                self.shot_sound.play()
                self.can_shoot = False
        else:
            self.can_shoot = True



class StallScene(Scene):
    BACKGROUND_COLOR = pygame.Color('darkgreen')

    def __init__(self, screen):
        super().__init__(screen)
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player(self.player_group)

    def process(self):
        for ev in self.get_scene_events():
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.do_quit()

    def update(self):
        self.player_group.update()

    def draw(self):
        self.screen.fill(StallScene.BACKGROUND_COLOR)
        self.player_group.draw(self.screen)

    def on_blur(self):
        pass

    def on_focus(self):
        pygame.mouse.set_visible(False)

    def do_quit(self):
        self.emit_event(UE_GAME_STOP)
