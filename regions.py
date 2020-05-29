from maps import Region


class BlueMountains(Region):
    """a"""

    def __init__(self):
        super().__init__()

        self.tile_image_size = (10952, 6549)
        self.region_size = (6, 3)
        self.top_left_tile = (-1, 2)

        map_image_paths = []
        map_data_paths = []
        dir = 'maps/blue_mts/'
        map_list = [
            'lithgow', 'wollangambe', 'mountain_lagoon',
            'hartley', 'mt_wilson', 'kurrajong',
            'hampton', 'katoomba', 'springwood',
            'jenolan', 'jamison', 'penrith',
            'kanangra', 'bimlow', 'warragamba',
            'yerranderie', 'burragorang', 'camden'
        ]

        for map in map_list:
            map_image_paths.append(dir + map + '.jpg')
            map_data_paths.append(dir + map + '.json')

        self.load_map_tile_data(map_image_paths=map_image_paths, map_data_paths=map_data_paths)


class RoyalNationalPark(Region):
    def __init__(self):
        super().__init__()

        self.tile_image_size = (10899, 6547)
        self.region_size = (2, 2)
        self.top_left_tile = (0, 0)

        map_image_paths = []
        map_data_paths = []
        dir = 'maps/rnp/'
        map_list = [
            'campbelltown', 'port_hacking',
            'appin', 'otford'
        ]

        for map in map_list:
            map_image_paths.append(dir + map + '.jpg')
            map_data_paths.append(dir + map + '.json')

        self.load_map_tile_data(map_image_paths=map_image_paths, map_data_paths=map_data_paths)
