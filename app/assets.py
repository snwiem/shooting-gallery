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
        self.load_assets()

    def _get_asset(self, asset_type, asset_id):
        match = next((i for i in self.assets_config[asset_type] if i['id'] == asset_id), None)
        if not match:
            raise Exception("No such asset")
        return match['res']

    def get_font(self, id, size):
        font_key = f"{id}_{size}"
        if font_key in self.fonts:
            return self.fonts[font_key]
        font_res = self._get_asset("fonts", id)
        font = pygame.font.Font(os.path.join('assets', font_res), size)
        self.fonts[font_key] = font
        return font

    def load_assets(self):
        with open('assets/assets.json') as assets_file:
            self.assets_config = json.load(assets_file)

    # FONT_TITLE = 0x01
    #
    # def __load_fonts(self):
    #     self._fonts = {
    #         AssetManager.FONT_TITLE: pygame.font.Font('assets/fonts/Kenney Bold.ttf', 24)
    #     }
    #
    # def get_font(self, font_id, font_size):
    #     font_key = f"{font_id}_{font_size}"
    #     if self._fonts.has_key(font_key):
    #         return self._fonts[font_key]
    #     font = pygame.font.Font()
    #
    #     return self._fonts[font]
