from regions import BlueMountains
# from regions import RoyalNationalPark


def region_map():
    """Test function."""

    region = BlueMountains()
    # region = RoyalNationalPark()
    # region.print_tile_dimensions()
    (im, _) = region.generate_region_map(route=None, crop=None, entire_extent=True)
    im.save('blue_mts_master.jpg')


if __name__ == "__main__":
    region_map()
