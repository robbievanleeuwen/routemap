from maps import Region


class BlueMountains(Region):
    """a"""

    def __init__(self):
        super().__init__()

        map_image_paths = []
        map_data_paths = []
        dir = 'maps/blue_mts/'
        map_list = [
            'hartley', 'mt_wilson', 'kurrajong',
            'hampton', 'katoomba', 'springwood',
            'jenolan', 'jamison', 'penrith'
        ]

        for map in map_list:
            map_image_paths.append(dir + map + '.jpg')
            map_data_paths.append(dir + map + '.json')

        self.load_map_tiles(map_image_paths=map_image_paths, map_data_paths=map_data_paths)
