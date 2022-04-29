import json
import os

import pygame.font


class AssetManager:
    __instance = None

    @staticmethod
    def get_instance():
        if AssetManager.__instance is None:
            AssetManager()
        return AssetManager.__instance

    def __init__(self):
        if AssetManager.__instance is not None:
            raise Exception("Use this class as a singleton!")
        else:
            AssetManager.__instance = self
        self.assets_config = None
        self.fonts = {}
        self.sprites = {}
        self.sounds = {}
        self._load_assets()

    def _load_assets(self):
        with open('assets/assets.json') as assets_file:
            self.assets_config = json.load(assets_file)

    def _get_asset(self, asset_type, asset_id):
        match = next((i for i in self.assets_config[asset_type] if i['id'] == asset_id), None)
        if not match:
            raise Exception("No such asset")
        return match['res']

    def get_sound(self, sound_id):
        key = sound_id
        if key in self.sounds:
            return self.sounds[key]
        sound_res = self._get_asset("sounds", key)
        sound = pygame.mixer.Sound(os.path.join('assets', sound_res))
        self.sounds[key] = sound
        return sound

    def get_font(self, id, size):
        font_key = f"{id}_{size}"
        if font_key in self.fonts:
            return self.fonts[font_key]
        font_res = self._get_asset("fonts", id)
        font = pygame.font.Font(os.path.join('assets', font_res), size)
        self.fonts[font_key] = font
        return font

    def get_sprite(self, sprite_id, copy=False):
        sprite_key = sprite_id
        if sprite_key in self.sprites:
            sprite = self.sprites[sprite_key]
        else:
            sprite_res = self._get_asset("sprites", sprite_id)
            sprite = pygame.image.load(os.path.join('assets', sprite_res))
            self.sprites[sprite_key] = sprite
        if copy:
            sprite = sprite.copy()
        return sprite




