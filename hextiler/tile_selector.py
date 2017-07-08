import pygame as pg
import numpy as np


class TileSelector:
    def __init__(self):
        self.tilemap_img = None
        self.tile_imgs = []
        self.num_imgs = 0
        self.current_tile_idx = 0

    def load_tiles(self, filename, radius):
        self.tilemap_img = pg.image.load(filename).convert_alpha()
        self.tile_imgs = []

        tile_width = int(radius * np.sqrt(3)) + 1
        tile_height = 2 * radius

        num_hexes =  self.tilemap_img.get_width() / tile_width
        for i in range(num_hexes):
            clip = [tile_width * i, 0, tile_width, tile_height]
            self.tile_imgs.append(self.tilemap_img.subsurface(clip))

        self.num_imgs = len(self.tile_imgs)

    def __getitem__(self, idx):
        return self.tile_imgs[idx]

    def empty(self):
        return self.num_imgs == 0

    def shift_selector(self, dx):
        if self.num_imgs > 0:
            self.current_tile_idx += dx
            self.current_tile_idx %= self.num_imgs

    def get_selected_idx(self):
        return self.current_tile_idx

    def get_selected_tile(self):
        if self.num_imgs > 0:
            return self.tile_imgs[self.current_tile_idx]
        else:
            return None
