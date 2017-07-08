import numpy as np
import hexy as hx
from draw import make_hex_surface


class SelectionTile(hx.HexTile):
    def __init__(self, axial_coordinates, border_color, radius):
        self.axial_coordinates = np.array([axial_coordinates])
        self.cube_coordinates = hx.axial_to_cube(self.axial_coordinates)
        self.position = hx.axial_to_pixel(self.axial_coordinates, radius)
        self.color = border_color
        self.radius = radius
        self.image = make_hex_surface((0, 0, 0, 140), self.radius, self.color, hollow=True)

    def set_position(self, position):
        self.position = position
        self.axial_coordinates = hx.pixel_to_axial(self.position, self.radius)
        self.cube_coordinates = hx.pixel_to_cube(self.position, self.radius)

    def get_draw_position(self):
        """
        Get the location to draw this hex so that the center of the hex is at `self.position`.
        :return: The location to draw this hex so that the center of the hex is at `self.position`.
        """
        draw_position = self.position[0] - [self.image.get_width() / 2, self.image.get_height() / 2]
        return draw_position

    def get_position(self):
        """
        Retrieves the location of the center of the hex.
        :return: The location of the center of the hex.
        """
        return self.position[0]

    def copy(self):
        return SelectionTile(self.axial_coordinates[0], self.color, self.radius)