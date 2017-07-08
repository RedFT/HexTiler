import numpy as np
import hexy as hx
import pygame as pg


class Cursor:
    def __init__(self, radius):
        self.hex_radius = radius
        self.mouse_pos = np.array([pg.mouse.get_pos()])
        self.mouse_cube = hx.pixel_to_cube(self.mouse_pos, self.hex_radius)
        self.mouse_axial = hx.pixel_to_axial(self.mouse_pos, self.hex_radius)
        self.mouse_hex = hx.cube_to_pixel(self.mouse_cube, self.hex_radius)


    def update(self, camera):
        self.mouse_pos = np.array([camera.follow_camera(pg.mouse.get_pos())])
        self.mouse_cube = hx.pixel_to_cube(self.mouse_pos, self.hex_radius)
        self.mouse_axial = hx.pixel_to_axial(self.mouse_pos, self.hex_radius)
        self.mouse_hex = hx.cube_to_pixel(self.mouse_cube, self.hex_radius)
