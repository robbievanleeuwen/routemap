import json
import time
import numpy as np
from itertools import compress
from PIL import Image
import gpxpy
import srtm
import matplotlib.pyplot as plt


class Region:
    """Class for a region, consisting of a number of pre-defined map tiles.
    """

    def __init__(self, map_tiles=[]):
        self.map_tiles = []
        self.tile_image_size = (None, None)

    def load_map_tile_data(self, map_image_paths=[], map_data_paths=[]):
        # check size of paths is the same
        if len(map_image_paths) != len(map_data_paths):
            raise Exception("Length of map_image_paths must match length of map_data_paths")

        for (i, map_image_path) in enumerate(map_image_paths):
            new_map_tile = MapTile(map_image_path=map_image_path, map_data_path=map_data_paths[i])
            self.map_tiles.append(new_map_tile)

    def generate_route_map(self, route, filename, crop=[1, 1, 1, 1]):
        """crop is in gps minutes (left, top, right, bottom)"""

        # generate map based on route
        (region_map, gps_extents) = self.generate_region_map(route, crop)

        dpi = 300
        width = region_map.width
        height = region_map.height
        figsize = width / float(dpi), height / float(dpi)

        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.imshow(region_map)

        # plot route
        width = region_map.width
        height = region_map.height
        x_s = []
        y_s = []

        for point in route.gpx.walk(only_points=True):
            (x, y) = self.gps_to_image(
                (point.longitude, point.latitude), gps_extents, width, height
            )
            x_s.append(x)
            y_s.append(y)

        ax.plot(x_s, y_s, 'b-', linewidth=3, alpha=0.5)

        ax.set(xlim=[-0.5, width - 0.5], ylim=[height - 0.5, -0.5], aspect=1)
        fig.savefig(filename + '.jpg', dpi=dpi, transparent=True)

    def generate_region_map(self, route, crop):
        """crop is in gps minutes (left, top, right, bottom)"""

        (used_tiles, extents) = self.route_within_tiles(route, crop)
        map_list = list(compress(self.map_tiles, used_tiles))
        map_grid = np.empty(
            shape=(extents[3] - extents[1] + 1, extents[2] - extents[0] + 1), dtype=object)

        # populate map_grid
        for map_tile in map_list:
            row = extents[3] - map_tile.tile_position[1]
            col = map_tile.tile_position[0] - extents[0]
            map_grid[row, col] = map_tile

        # print map grid
        print(map_grid)

        # calculate width & height
        grid_width = int(map_grid.shape[1] * self.tile_image_size[0])
        grid_height = int(map_grid.shape[0] * self.tile_image_size[1])

        # build image
        grid = Image.new('RGB', (grid_width, grid_height), (255, 255, 255))
        top = 0
        gps_extents = [0, 0, 0, 0]

        for (i, grid_row) in enumerate(map_grid):
            left = 0

            for (j, map_tile) in enumerate(grid_row):
                str = "Transforming map tile: {0}".format(map_tile)
                im = function_timer(str, map_tile.transform_image, self.tile_image_size)
                grid.paste(im, box=(left, top))
                left += self.tile_image_size[0]

                if i == 0 and j == 0:
                    gps_extents[0] = map_tile.longitude[0]
                    gps_extents[1] = map_tile.latitude[0]

            top += self.tile_image_size[1]

        gps_extents[2] = map_tile.longitude[2]
        gps_extents[3] = map_tile.latitude[2]

        # crop image
        gps_bbox = route.calculate_bounding_box()
        gps_crop = (
            gps_bbox[0] - crop[0] / 60,
            gps_bbox[1] + crop[1] / 60,
            gps_bbox[2] + crop[2] / 60,
            gps_bbox[3] - crop[3] / 60
        )

        (l, t) = self.gps_to_image(
            (gps_crop[0], gps_crop[1]),
            gps_extents, grid_width, grid_height
        )
        (r, b) = self.gps_to_image(
            (gps_crop[2], gps_crop[3]),
            gps_extents, grid_width, grid_height
        )

        return (grid.crop((l, t, r, b)), gps_crop)

    def route_within_tiles(self, route, crop):
        """Checks to see which tiles are required to display the route and returns the tile extents
        of the combined map.
        """

        route_bounding_box = route.calculate_bounding_box()
        route_bounding_box = (
            route_bounding_box[0] - crop[0] / 60,
            route_bounding_box[1] + crop[1] / 60,
            route_bounding_box[2] + crop[2] / 60,
            route_bounding_box[3] - crop[3] / 60
        )

        # add crop to bounding box
        used_tiles = []
        extents = [999, 999, -999, -999]  # tile extents [xmin, ymin, xmax, ymax]

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

    def gps_to_image(self, pt, gps_extents, width, height):
        x = width / (gps_extents[2] - gps_extents[0]) * (pt[0] - gps_extents[0])
        y = height / (gps_extents[3] - gps_extents[1]) * (pt[1] - gps_extents[1])

        return (x, y)

    def print_tile_dimensions(self):
        grid_shape = (3, 3)
        top_widths = map_grid = np.empty(shape=grid_shape)
        bot_widths = map_grid = np.empty(shape=grid_shape)
        left_heights = map_grid = np.empty(shape=grid_shape)
        right_heights = map_grid = np.empty(shape=grid_shape)
        delta_x_left = map_grid = np.empty(shape=grid_shape)
        delta_x_right = map_grid = np.empty(shape=grid_shape)
        delta_y_top = map_grid = np.empty(shape=grid_shape)
        delta_y_bot = map_grid = np.empty(shape=grid_shape)

        map_grid = np.empty(shape=grid_shape, dtype=object)

        for map_tile in self.map_tiles:
            row = 1 - map_tile.tile_position[1]
            col = map_tile.tile_position[0] + 1
            map_grid[row, col] = map_tile
            top_widths[row, col] = map_tile.x_px[1] - map_tile.x_px[0]
            bot_widths[row, col] = map_tile.x_px[2] - map_tile.x_px[3]
            left_heights[row, col] = map_tile.y_px[3] - map_tile.y_px[0]
            right_heights[row, col] = map_tile.y_px[2] - map_tile.y_px[1]
            delta_x_left[row, col] = map_tile.x_px[3] - map_tile.x_px[0]
            delta_x_right[row, col] = map_tile.x_px[2] - map_tile.x_px[1]
            delta_y_top[row, col] = map_tile.y_px[1] - map_tile.y_px[0]
            delta_y_bot[row, col] = map_tile.y_px[2] - map_tile.y_px[3]

        print("Map Tiles:\n" + str(map_grid) + "\n")
        print("Top Widths:\n" + str(top_widths) + "\n")
        print("Bottom Widths:\n" + str(bot_widths) + "\n")
        print("Left Heights:\n" + str(left_heights) + "\n")
        print("Right Heights:\n" + str(right_heights) + "\n")
        print("Left dx:\n" + str(delta_x_left) + "\n")
        print("Right dx:\n" + str(delta_x_right) + "\n")
        print("Top dy:\n" + str(delta_y_top) + "\n")
        print("Bottom dy:\n" + str(delta_y_bot) + "\n")


class MapTile:
    """Class for a map tile.

    N.B Corners are ordered clockwise from top left, i.e. top left, top right, bottom right, bottom
    left.
    """

    def __init__(self, map_image_path, map_data_path):
        Image.MAX_IMAGE_PIXELS = None

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

    def load_image(self):
        try:
            return Image.open(self.map_image_path)
        except FileNotFoundError:
            return None

    def transform_image(self, tile_image_size):
        def find_coeffs(source_coords, target_coords):
            matrix = []

            for s, t in zip(source_coords, target_coords):
                matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
                matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])

            A = np.matrix(matrix, dtype=np.float)
            B = np.array(source_coords).reshape(8)
            res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
            return np.array(res).reshape(8)

        im = self.load_image()

        source_coords = (
            (self.x_px[0], self.y_px[0]),
            (self.x_px[1], self.y_px[1]),
            (self.x_px[2], self.y_px[2]),
            (self.x_px[3], self.y_px[3])
        )
        target_coords = (
            (0, 0),
            (tile_image_size[0], 0),
            (tile_image_size[0], tile_image_size[1]),
            (0, tile_image_size[1])
        )
        coeffs = find_coeffs(source_coords, target_coords)

        return(im.transform(
            (tile_image_size[0], tile_image_size[1]), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
        )

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


class Route:
    def __init__(self, gpx_path, srtm=False):
        with open(gpx_path) as gpx_file:
            self.gpx = gpxpy.parse(gpx_file)

        if srtm:
            self.srtm_elevation()

    def calculate_length_2d(self):
        self.gpx.length_2d()

    def calculate_length_3d(self):
        self.gpx.length_3d()

    def elevation_chart_points(self):
        distance_points = []
        elevation_points = []
        previous_point = None
        length = 0

        for point in self.gpx.walk(only_points=True):
            if previous_point:
                length += previous_point.distance_2d(point)

            distance_points.append(length)
            elevation_points.append(point.elevation)
            previous_point = point

        return (distance_points, elevation_points)

    def srtm_elevation(self, smooth=True, gpx_smooth_no=3):
        elevation_data = srtm.get_data()
        elevation_data.add_elevations(self.gpx, smooth=smooth, gpx_smooth_no=gpx_smooth_no)

    def calculate_bounding_box(self):
        bounds = self.gpx.get_bounds()

        return (
            bounds.min_longitude,
            bounds.max_latitude,
            bounds.max_longitude,
            bounds.min_latitude
        )

    def calculate_uphill_downhill(self):
        uphill_downhill = self.gpx.get_uphill_downhill()

        return (uphill_downhill.uphill, uphill_downhill.downhill)

    def get_elevation_extremes(self):
        min_max_elevation = self.gpx.get_elevation_extremes()

        return (min_max_elevation.minimum, min_max_elevation.maximum)


def function_timer(text, function, *args):
    """Displays the message *text* and returns the time taken for a function, with arguments
    *args*, to execute. The value returned by the timed function is also returned.

    :param string text: Message to display
    :param function: Function to time and execute
    :type function: function
    :param args: Function arguments
    :return: Value returned from the function
    """

    start_time = time.time()

    if text != "":
        print(text)

    result = function(*args)

    if text != "":
        print("----completed in {0:.6f} seconds---".format(
            time.time() - start_time))

    return result
