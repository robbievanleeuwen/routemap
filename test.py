from regions import BlueMountains, RoyalNationalPark
from maps import Route


def test():
    region = BlueMountains()
    # region = RoyalNationalPark()
    # region.print_tile_dimensions()
    gps = Route(gpx_path='routes/splendour_rock.gpx', srtm=True)
    region.generate_route_map(route=gps, filename='splendour_rock', output_folder='routes/out/')
    # (im, _) = region.generate_region_map(route=None, crop=None, entire_extent=True)
    # im.save('blue_mts_master.jpg')

if __name__ == "__main__":
    test()
