import hexy as hx
import numpy as np


class GenericTile(hx.HexTile):
    def __init__(self, axial_coordinates, radius, tile_id):
        self.axial_coordinates = np.array([axial_coordinates])
        self.cube_coordinates = hx.axial_to_cube(self.axial_coordinates)
        self.position = hx.axial_to_pixel(self.axial_coordinates, radius)
        self.radius = radius
        self.tile_id = tile_id

    def set_position(self, position):
        self.position = position
        self.axial_coordinates = hx.pixel_to_axial(self.position, self.radius)
        self.cube_coordinates = hx.pixel_to_cube(self.position, self.radius)

    def get_draw_position(self, image):
        """
        Get the location to draw this hex so that the center of the hex is at `self.position`.
        :return: The location to draw this hex so that the center of the hex is at `self.position`.
        """
        draw_position = self.position[0] - [image.get_width() / 2, image.get_height() / 2]
        return draw_position

    def get_position(self):
        """
        Retrieves the location of the center of the hex.
        :return: The location of the center of the hex.
        """
        return self.position[0]
