import json
import numpy as np
from itertools import compress
from PIL import Image


class Region:
    """Class for a region, consisting of a number of pre-defined map tiles.
    """

    def __init__(self, map_tiles=[]):
        self.map_tiles = []

    def load_map_tiles(self, map_image_paths=[], map_data_paths=[]):
        # check size of paths is the same
        if len(map_image_paths) != len(map_data_paths):
            raise Exception("Length of map_image_paths must match length of map_data_paths")

        for (i, map_image_path) in enumerate(map_data_paths):
            new_map_tile = MapTile(map_image_path=map_image_path, map_data_path=map_data_paths[i])
            self.map_tiles.append(new_map_tile)


    def generate_region_map(self, route):
        (used_tiles, extents) = self.route_within_tiles(route=route)
        map_list = list(compress(self.map_tiles, used_tiles))
        map_grid = np.empty(shape=(extents[3] - extents[1] + 1, extents[2] - extents[0] + 1), dtype=object)

        # populate map_grid
        for map_tile in map_list:
            # calculate array index
            idx = np.array([map_tile.tile_position[0] - extents[0], extents[3] - map_tile.tile_position[1]])
            print(idx)
            map_grid[idx] = map_tile
            print(map_grid)

        print(map_grid)


    def route_within_tiles(self, route):
        """Checks to see which tiles are required to display the route and returns the tile extents of the combined
        map.
        """

        route_bounding_box = route.bounding_box
        used_tiles = []
        extents = [999, 999, -999, -999] # tile extents [xmin, ymin, xmax, ymax]

        for map_tile in self.map_tiles:
            is_used = map_tile.within_bounding_box(bounding_box=route_bounding_box)
            used_tiles.append(is_used)

            if is_used:
                pos = map_tile.tile_position
                extents[0] = min(extents[0], pos[0])
                extents[1] = min(extents[1], pos[1])
                extents[2] = max(extents[2], pos[0])
                extents[3] = max(extents[3], pos[1])

        return (used_tiles, extents)



class MapTile:
    """Class for a map tile.

    N.B Corners are ordered clockwise from top left, i.e. top left, top right, bottom right, bottom
    left.
    """

    def __init__(self, map_image_path, map_data_path):
        Image.MAX_IMAGE_PIXELS = None

        self.map_image = None
        self.map_image_path = map_image_path

        with open(map_data_path) as json_file:
            map_data = json.load(json_file)

        self.map_name = map_data["name"]
        self.x_px = [
            map_data["top_left"]["x_px"],
            map_data["top_right"]["x_px"],
            map_data["bottom_right"]["x_px"],
            map_data["bottom_left"]["x_px"],
        ]
        self.y_px = [
            map_data["top_left"]["y_px"],
            map_data["top_right"]["y_px"],
            map_data["bottom_right"]["y_px"],
            map_data["bottom_left"]["y_px"],
        ]
        self.latitude = [
            map_data["top_left"]["latitude"],
            map_data["top_right"]["latitude"],
            map_data["bottom_right"]["latitude"],
            map_data["bottom_left"]["latitude"],
        ]
        self.longitude = [
            map_data["top_left"]["longitude"],
            map_data["top_right"]["longitude"],
            map_data["bottom_right"]["longitude"],
            map_data["bottom_left"]["longitude"],
        ]
        self.tile_position = map_data["tile_position"]
        self.alignment = map_data["alignment"]

    def load_image(self):
        try:
            self.map_image = Image.open(self.map_image_path)
        except FileNotFoundError:
            self.map_image = None

    def extent_crop(self):
        left = min(self.x_px[0], self.x_px[3])
        upper = min(self.y_px[0], self.y_px[1])
        right = max(self.x_px[1], self.x_px[2])
        lower = max(self.y_px[2], self.y_px[3])

        self.load_image()

        return self.map_image.crop(box=(left, upper, right, lower))

    def within_bounding_box(self, bounding_box):
        """Check to see whether any part of the map tile lies within the bounding box in gps
        coordinates."""

        bbox_left = bounding_box[0]
        bbox_upper = bounding_box[1]
        bbox_right = bounding_box[2]
        bbox_lower = bounding_box[3]
        map_left = self.longitude[0]
        map_upper = self.latitude[0]
        map_right = self.longitude[2]
        map_lower = self.latitude[2]

        if (bbox_left > map_right or bbox_right < map_left or
                bbox_upper < map_lower or bbox_lower > map_upper):
            return False
        else:
            return True

    def __repr__(self):
        return self.map_name

    def __str__(self):
        return self.map_name


# class CombinedMap:
#
#
#     def combine_images(self, crop=True):
#         image_list = []
#
#         for map_image in self.map_images:
#             if crop:
#                 image_list.append(map_image.extent_crop())
#             else:
#                 image_list.append(map_image.image)
#
#         # determine width & height
#         x_mins = []
#         x_maxs = []
#         height = 0
#
#         for (i, im) in enumerate(image_list):
#             x_mins.append(-0.5 * im.width + self.map_images[i].alignment[0])
#             x_maxs.append(0.5 * im.width + self.map_images[i].alignment[0])
#             print(im.width)
#             height += im.height
#
#         print(x_mins)
#         print(x_maxs)
#
#         width = max(x_maxs) - min(x_mins)
#
#         # check ints
#         if width % 2 != 0:
#             raise Exception('Width is an odd number!')
#         elif height % 2 != 0:
#             raise Exception('Height is an odd number!')
#
#         width = int(width)
#         height = int(height)
#
#         combined = Image.new('RGB', (width, height), (0, 0, 0))
#         cum_height = 0
#
#         for (i, im) in enumerate(image_list):
#             left = 0.5 * (width - im.width) + self.map_images[i].alignment[0]
#
#             if left % 2 != 0:
#                 raise Exception('Left is an odd number!')
#
#             left = int(left)
#             print(left)
#
#             combined.paste(im, box=(left, cum_height))
#             cum_height += im.height
#
#         return combined

class Route:
    def __init__(self, gpx_path):
        self.gpx_path = gpx_path

        self.load_gpx()

        self.bounding_box = self.calculate_bounding_box()

    def load_gpx(self):
        pass

    def calculate_bounding_box(self):
        return [150.3, -33.55, 150.4, -33.7]
