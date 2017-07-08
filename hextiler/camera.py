import numpy as np


class Camera:
    def __init__(self, screen_size):
        self.position = np.array(screen_size[:2])
        self.size = np.array(screen_size[2:4])

    def move_camera(self, position):
        self.position += position

    def follow_camera(self, position):
        return position + self.position

    def set_position(self, position):
        self.position = np.array(position)

    def translate(self, position):
        return position - self.position
