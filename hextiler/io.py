import numpy as np
import hexy as hx
import json


def load_tilemap(filename):
    new_hex_map = hx.HexMap()
    with open(filename, 'r') as f:
        loaded_json = json.load(f)

    for item in loaded_json['tiles']:
        pos, hex_radius, tile_id = item
        new_tile = hx.HexTile(np.array(pos), hex_radius, tile_id)
        new_hex_map[new_tile.axial_coordinates] = [new_tile]

    return new_hex_map



def save_tilemap(hex_map, filename):
    json_to_save = {'tiles': []}
    for hexagon in hex_map.itervalues():
        properties = [list(hexagon.axial_coordinates[0]), hexagon.radius, hexagon.tile_id]
        json_to_save['tiles'].append(properties)

    with open(filename, 'w') as f:
        json.dump(json_to_save, f)


