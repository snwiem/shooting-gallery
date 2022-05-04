import logging

import pygame.mouse

from app.assets import AssetManager
from app.events import UE_GAME_STOP, UE_AMMO_EMPTY, UE_AMMO_RELOAD
from app.scene import Scene
from app.settings import SCREEN_HEIGHT, SCREEN_WIDTH, RELOAD_DELAY, MAX_SHOTS


class PlayerData(object):

    def __init__(self):
        self.max_shots = MAX_SHOTS
        self.num_shots = 0
        self.score = 0
        self.reloading = False

    def can_shoot(self):
        if self.reloading:
            return False
        if self.num_shots >= self.max_shots:
            return False
        return True


class PlayerSprite(pygame.sprite.Sprite):
    SPRITE_CROSSHAIR = "crosshair"

    def __init__(self, player_data: PlayerData):
        super().__init__()
        self.player_data = player_data
        self.image = AssetManager.get_instance().get_sprite(PlayerSprite.SPRITE_CROSSHAIR)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class BulletsSprite(pygame.sprite.Sprite):
    SPRITE_EMPTY = "bullet_empty_long"
    SPRITE_FULL = "bullet_gold_long"
    SPRITE_BORDER = 3
    SPRITE_WIDTH = 21
    SPRITE_HEIGHT = 44

    def __init__(self, player_data: PlayerData):
        super().__init__()
        self.player_data = player_data
        self.bullet_empty = AssetManager.get_instance().get_sprite(BulletsSprite.SPRITE_EMPTY)
        self.bullet_gold = AssetManager.get_instance().get_sprite(BulletsSprite.SPRITE_FULL)
        self.surface = self.create_surface()
        self.image = self.surface.copy()
        self.render_bullets(self.image)
        self.rect = self.image.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.update_required = False

    def create_surface(self):
        image = pygame.Surface(
            (self.player_data.max_shots * (BulletsSprite.SPRITE_WIDTH + (2 * BulletsSprite.SPRITE_BORDER)),
             BulletsSprite.SPRITE_HEIGHT),
            pygame.SRCALPHA, 32).convert_alpha()
        return image

    def render_bullets(self, surface):
        for i in range(0, self.player_data.num_shots):
            x = BulletsSprite.SPRITE_BORDER + (i * (BulletsSprite.SPRITE_WIDTH + (2 * BulletsSprite.SPRITE_BORDER)))
            surface.blit(self.bullet_empty, (x, 0))
        for i in range(self.player_data.num_shots, self.player_data.max_shots):
            x = BulletsSprite.SPRITE_BORDER + (i * (BulletsSprite.SPRITE_WIDTH + (2 * BulletsSprite.SPRITE_BORDER)))
            surface.blit(self.bullet_gold, (x, 0))

    def update(self):
        if self.update_required:
            self.image = self.surface.copy()
            self.render_bullets(self.image)
            self.update_required = False


class StallScene(Scene):
    BACKGROUND_COLOR = pygame.Color('darkgreen')
    SOUND_SHOT = "shotgun-fire"
    SOUND_RELOAD = "bullet-reload"
    SOUND_RELOAD_START = "bullet-reload-start"
    SOUND_RELOAD_END = "bullet-reload-end"

    def __init__(self, screen):
        super().__init__(screen)
        self.shot_sound = AssetManager.get_instance().get_sound(StallScene.SOUND_SHOT)
        self.reload_sound = AssetManager.get_instance().get_sound(StallScene.SOUND_RELOAD)
        self.reload_sound_open = AssetManager.get_instance().get_sound(StallScene.SOUND_RELOAD_START)
        self.reload_sound_close = AssetManager.get_instance().get_sound(StallScene.SOUND_RELOAD_END)

        self.player_group = pygame.sprite.GroupSingle()
        self.hud_group = pygame.sprite.Group()

        self.player_data = PlayerData()
        self.player_sprite = PlayerSprite(self.player_data)
        self.player_sprite.add(self.player_group)

        self.ammo = BulletsSprite(self.player_data)
        self.hud_group.add(self.ammo)

        self.is_trigger_released = True
        self.is_reloading = False

    def process(self):
        # do all scene event handling
        for ev in self.get_scene_events():
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.do_quit()
                    break
            if ev.type == UE_AMMO_RELOAD:
                self.do_reload()

        # check for user input
        (bt1, bt2, bt3) = pygame.mouse.get_pressed(num_buttons=3)
        if bt1:
            if self.is_trigger_released and not self.is_reloading:
                if self.player_data.can_shoot():
                    self.do_shoot(self.player_sprite.rect.center)
                    self.is_trigger_released = False
        else:
            self.is_trigger_released = True
        if bt3:
            if not self.is_reloading:
                if self.player_data.num_shots > 0:
                    self.is_reloading = True
                    self.reload_sound_open.play()
                    pygame.time.set_timer(UE_AMMO_RELOAD, RELOAD_DELAY, 1)

    def update(self):
        self.player_group.update()
        self.hud_group.update()

    def draw(self):
        self.screen.fill(StallScene.BACKGROUND_COLOR)
        self.player_group.draw(self.screen)
        self.hud_group.draw(self.screen)

    def on_blur(self):
        pass

    def on_focus(self):
        pygame.mouse.set_visible(False)

    def do_quit(self):
        self.emit_event(UE_GAME_STOP)

    def do_shoot(self, pos):
        logging.debug(f"shot at pos: {pos}")
        self.shot_sound.play()
        self.player_data.num_shots += 1
        self.ammo.update_required = True

    def do_reload(self):
        if self.player_data.num_shots > 0:
            self.is_reloading = True
            self.reload_sound.play()
            self.player_data.num_shots -= 1
            self.ammo.update_required = True
            if 0 == self.player_data.num_shots:
                self.is_reloading = False
                self.reload_sound_close.play()
            else:
                pygame.time.set_timer(UE_AMMO_RELOAD, RELOAD_DELAY, 1)

