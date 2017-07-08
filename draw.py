import numpy as np
import pygame as pg


def make_hex_surface(color, radius, border_color=(100, 100, 100), border=True, hollow=False):
    """
    Draws a hexagon with gray borders on a pygame surface.
    :param color: The fill color of the hexagon.
    :param radius: The radius (from center to any corner) of the hexagon.
    :param border_color: Color of the border.
    :param border: Draws border if True.
    :param hollow: Does not fill hex with color if True.
    :return: A pygame surface with a hexagon drawn on it
    """
    offset = np.array([radius * np.sqrt(3)/2, radius])

    angles_in_radians = np.deg2rad([60 * i + 30 for i in range(6)])
    x = np.cos(angles_in_radians)
    y = np.sin(angles_in_radians)
    points = radius * np.vstack([x, y]).T
    points = np.round(points+offset)

    height = round(2 * radius)


    points[points[:, 1] == height, 1] = height -1
    print points

    minx= np.min(points[:, 0])
    maxx= np.max(points[:, 0])
    miny= np.min(points[:, 1])
    maxy= np.max(points[:, 1])

    size = np.array([maxx - minx + 1, maxy - miny + 1])
    print size
    surface = pg.Surface(size)
    surface.set_colorkey((0, 0, 0))
    if len(color) >= 4:
        surface.set_alpha(color[-1])
    if not hollow:
        pg.draw.polygon(surface, color, points, 0)

    if border or hollow:
        pg.draw.polygon(surface, border_color, points, 1)
    return surface
