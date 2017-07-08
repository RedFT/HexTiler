import json
import numpy as np
import hexy as hx
import pygame as pg

from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfilename

from generic_tile import GenericTile
from selection_tile import SelectionTile


def load_tiles(filename, radius):
    imgs = []
    img = pg.image.load(filename).convert_alpha()

    tile_width = int(radius * np.sqrt(3)) + 1
    tile_height = 2 * radius

    num_hexes = img.get_width() / tile_width
    for i in range(num_hexes):
        clip = [tile_width * i, 0, tile_width, tile_height]
        imgs.append(img.subsurface(clip))

    return imgs


class HexTileEditor():
    def __init__(self, size=(600, 600), hex_radius=16, caption="Hex Tile Editor"):
        self.caption = caption
        self.size = np.array(size)
        self.width, self.height = self.size
        self.camera_center = self.size / 2
        self.first_click = np.array([0, 0])
        self.scrolling = False
        self.zoom_level = 1.

        self.main_surf = None
        self.font = None
        self.clock = None
        self.init_pg()

        self.hex_radius = hex_radius
        self.hex_apothem = hex_radius * np.sqrt(3) / 2
        self.hex_offset = np.array([self.hex_radius * np.sqrt(3) / 2, self.hex_radius])

        self.hex_map = hx.HexMap()
        self.max_coord = 7

        self.rad = 3

        self.tile_imgs = []
        self.current_tile_idx = 0

        self.selection_tile = SelectionTile(np.array([0, 0]), (20, 20, 20), self.hex_radius)
        self.clicked_hex = np.array([0, 0, 0])


    def init_pg(self):
        pg.init()
        self.main_surf = pg.display.set_mode(self.size)
        pg.display.set_caption(self.caption)

        pg.font.init()
        self.font = pg.font.SysFont("monospace", 12, True)
        self.clock = pg.time.Clock()

    def clear_tile(self, position):
        del self.hex_map[position]

    def set_tile(self, position):
        new_tile = GenericTile(position[0], self.hex_radius, self.current_tile_idx)
        try:
            self.hex_map[position] = [new_tile]
        except hx.HexExistsError:
            self.hex_map.overwrite_entry(position[0], new_tile)

    def load_tilemap(self, filename):
        new_hex_map = hx.HexMap()
        with open(filename, 'r') as f:
            loaded_json = json.load(f)

        for key, value in loaded_json.iteritems():
            coord = list(map(int, key.split(',')))
            pos = hx.bases_mat.dot(coord).T
            tile_id = int(value)
            new_tile = GenericTile(pos, self.hex_radius, tile_id)
            new_hex_map[np.array([pos])] = [new_tile]

        self.hex_map = new_hex_map

    def save_tilemap(self, filename):
        json_to_save = {}
        for k, v in self.hex_map.iteritems():
            json_to_save[k] = v.tile_id

        with open(filename, 'w') as f:
            json.dump(json_to_save, f)

    def handle_events(self):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 2:
                    self.scrolling = False
                    second_click = np.array(pg.mouse.get_pos())
                    self.camera_center += second_click - self.first_click

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    set_position_axial = hx.pixel_to_axial(np.array([pg.mouse.get_pos() - self.camera_center]),
                                                           self.hex_radius)
                    self.set_tile(set_position_axial)
                if event.button == 2:
                    self.scrolling = True
                    self.first_click = np.array(pg.mouse.get_pos())
                if event.button == 3:
                    clear_position_axial = hx.pixel_to_axial(np.array([pg.mouse.get_pos() - self.camera_center]),
                                                             self.hex_radius)
                    self.clear_tile(clear_position_axial)
                if event.button == 4:
                    self.zoom_level -= 0.1
                if event.button == 5:
                    self.zoom_level += 0.1
                ''' 
                if event.button == 4:
                    self.current_tile_idx -= 1
                    self.current_tile_idx %= len(self.tile_imgs)
                if event.button == 5:
                    self.current_tile_idx += 1
                    self.current_tile_idx %= len(self.tile_imgs)
                '''

            if event.type == pg.KEYUP:
                pass

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_i:
                    Tk().withdraw()
                    filename = askopenfilename()
                    self.tile_imgs = load_tiles(filename, self.hex_radius)
                elif event.key == pg.K_UP:
                    self.camera_center[1] += 10
                elif event.key == pg.K_DOWN:
                    self.camera_center[1] -= 10
                elif event.key == pg.K_LEFT:
                    self.camera_center[0] += 10
                elif event.key == pg.K_RIGHT:
                    self.camera_center[0] -= 10
                elif event.key == pg.K_l:
                    Tk().withdraw()
                    filename = askopenfilename()
                    self.load_tilemap(filename)
                elif event.key == pg.K_s:
                    Tk().withdraw()
                    filename = asksaveasfilename()
                    self.save_tilemap(filename)


        return running

    def main_loop(self):
        running = self.handle_events()
        if self.rad > 5:
            self.rad = 5
        elif self.rad < 1:
            self.rad = 1

        return running

    def draw(self):
        tmp_surf = pg.Surface(self.size)
        tmp_surf.fill([200, 200, 200])

        offset = [0, 0]
        if self.scrolling:
            offset = (np.array(pg.mouse.get_pos()) - self.first_click)
        camera_center_with_scroll = (self.camera_center + offset)
        # show all hexes
        for hexagon in self.hex_map.values():
            tile_img = self.tile_imgs[hexagon.tile_id]
            tmp_surf.blit(tile_img, hexagon.get_draw_position(tile_img) + camera_center_with_scroll)

        mouse_pos = np.array([np.array(pg.mouse.get_pos()) - camera_center_with_scroll]) * self.zoom_level
        cube_mouse = hx.pixel_to_cube(mouse_pos, self.hex_radius)
        mouse_hex = hx.cube_to_pixel(cube_mouse, self.hex_radius)
        self.selection_tile.set_position(mouse_hex)
        tmp_surf.blit(self.selection_tile.image, self.selection_tile.get_draw_position() + camera_center_with_scroll)

        # Update screen
        sub_shape = np.array(self.size) * self.zoom_level
        sub_pos = (self.size - sub_shape) / 2
        sub_rect = np.hstack([sub_pos, sub_shape])
        focus = tmp_surf.subsurface(sub_rect)

        pg.transform.scale(focus, self.size, self.main_surf)

        if self.tile_imgs:
            menu_rect = np.array(self.tile_imgs[0].get_rect())
            menu_rect[2] = self.tile_imgs[0].get_width() * len(self.tile_imgs)

            pg.draw.rect(self.main_surf, (255, 255, 255), menu_rect)
            for i, tile in enumerate(self.tile_imgs):
                x = i * self.tile_imgs[i].get_width()
                self.main_surf.blit(self.tile_imgs[i], (x, 0))

            select_rect = self.tile_imgs[0].get_rect()
            select_rect[0] = self.current_tile_idx * self.tile_imgs[0].get_width()
            pg.draw.rect(self.main_surf, (255, 0, 0), select_rect, 1)

        fps_text = self.font.render(
            "Camera Center: " + str(camera_center_with_scroll) + " " +
            "Cursor: " + str(mouse_hex[0]) + " " +
            "Zoom: " + str(self.zoom_level)
            , True, (50, 50, 50))
        self.main_surf.blit(fps_text, (2, self.size[1] - fps_text.get_height()))

        pg.display.update()
        self.clock.tick(30)

    def quit_app(self):
        pg.quit()


if __name__ == '__main__':
    ehm = HexTileEditor()
    while ehm.main_loop():
        ehm.draw()
    ehm.quit_app()
