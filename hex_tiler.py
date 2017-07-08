import numpy as np
import pygame as pg
from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfilename

import hexy as hx
import hextiler as ht


class HexTileEditor():
    def __init__(self, size=(800, 600), hex_radius=16, caption="Hex Tile Editor"):
        self.size = np.array(size)
        self.hex_radius = hex_radius
        self.caption = caption

        # Initialize PyGame
        pg.init()
        self.main_surf = pg.display.set_mode(self.size, pg.RESIZABLE)
        pg.display.set_caption(self.caption)

        pg.font.init()
        self.font = pg.font.SysFont("monospace", 12, True)
        self.clock = pg.time.Clock()

        self.width, self.height = self.size
        self.camera = ht.Camera(-self.size / 2)
        self.first_click = np.array([0, 0])
        self.scrolling = False

        self.cursor = ht.Cursor(hex_radius)
        self.hex_map = hx.HexMap()
        self.selector = ht.TileSelector()

        self.selection_tile = ht.SelectionTile(np.array([0, 0]), (20, 20, 20), self.hex_radius)
        self.clicked_hex = np.array([0, 0, 0])

    def clear_tile(self, position):
        del self.hex_map[position]

    def set_tile(self, position):
        if self.selector.empty():
            return

        new_tile = hx.HexTile(position.flatten(), self.hex_radius, self.selector.get_selected_idx())
        try:
            self.hex_map[position] = [new_tile]
        except hx.HexExistsError:
            self.hex_map.overwrite_entry(position.flatten(), new_tile)

    def handle_events(self):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 2:
                    self.scrolling = False
                    self.camera.move_camera(pg.mouse.get_pos() - self.first_click)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.set_tile(self.cursor.mouse_axial)
                if event.button == 2:
                    self.scrolling = True
                    self.first_click = np.array(pg.mouse.get_pos())
                if event.button == 3:
                    self.clear_tile(self.cursor.mouse_axial)
                if event.button == 4:
                    pass
                if event.button == 5:
                    pass

            if event.type == pg.KEYUP:
                pass

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_i:
                    Tk().withdraw()
                    filename = askopenfilename(filetypes=[('PNG Files', '.png')])
                    if filename: self.selector.load_tiles(filename, self.hex_radius)
                elif event.key == pg.K_UP:
                    self.camera.move_camera((0, -10))
                elif event.key == pg.K_DOWN:
                    self.camera.move_camera((0, 10))
                elif event.key == pg.K_LEFT:
                    self.camera.move_camera((-10, 0))
                elif event.key == pg.K_RIGHT:
                    self.camera.move_camera((10, 0))
                elif event.key == pg.K_l:
                    Tk().withdraw()
                    filename = askopenfilename(filetypes=[('JSON Files', '.json')])
                    if filename: self.hex_map = ht.load_tilemap(filename)
                elif event.key == pg.K_s:
                    Tk().withdraw()
                    filename = asksaveasfilename(filetypes=[('JSON Files', '.json')])
                    if filename: ht.save_tilemap(self.hex_map, filename)
                if event.key == pg.K_COMMA:
                    self.selector.shift_selector(-1)
                if event.key == pg.K_PERIOD:
                    self.selector.shift_selector(1)

        return running

    def update(self):
        running = self.handle_events()

        if self.scrolling:
            new_pos = np.array(pg.mouse.get_pos())
            offset = self.first_click - new_pos
            self.first_click = new_pos
            self.camera.move_camera(offset)

        self.cursor.update(self.camera)

        return running

    def draw(self):
        # show all hexes
        for hexagon in self.hex_map.values():
            if hexagon.tile_id < self.selector.num_imgs:
                tile_img = self.selector[hexagon.tile_id]
                draw_position = hexagon.position.flatten() - [tile_img.get_width() / 2, tile_img.get_height() / 2]
                draw_position = self.camera.translate(draw_position)
                self.main_surf.blit(tile_img, draw_position)

        self.selection_tile.set_position(self.cursor.mouse_hex)
        draw_position = self.selection_tile.get_draw_position()
        draw_position = self.camera.translate(draw_position)
        self.main_surf.blit(self.selection_tile.image, draw_position)

        if not self.selector.empty():
            selected_tile = self.selector.get_selected_tile()
            menu_rect = self.selector.tilemap_img.get_rect()

            pg.draw.rect(self.main_surf, (230, 230, 230), menu_rect)
            for i, tile in enumerate(self.selector.tile_imgs):
                self.main_surf.blit(tile, (i * selected_tile.get_width(), 0))

            select_rect = selected_tile.get_rect()
            select_rect[0] = self.selector.get_selected_idx() * selected_tile.get_width()
            pg.draw.rect(self.main_surf, (255, 0, 0), select_rect, 1)

        bar_text = "Camera Pos: [%d, %d] Cursor: [%.2f, %+.2f]" % \
                   (self.camera.position[0], self.camera.position[1],
                   self.cursor.mouse_hex.flatten()[0], self.cursor.mouse_hex.flatten()[1])
        bar_surface = self.font.render(
            bar_text,
            True, (50, 50, 50))
        self.main_surf.blit(bar_surface, (2, self.size[1] - bar_surface.get_height()))

        pg.display.update()
        self.main_surf.fill([200, 200, 200])
        self.clock.tick(30)

    def quit_app(self):
        pg.quit()


if __name__ == '__main__':
    ehm = HexTileEditor()
    while ehm.update():
        ehm.draw()
    ehm.quit_app()
