from regions import BlueMountains, RoyalNationalPark
from maps import Route
from pdfcreate import RouteMapPDF


def test():
    region = BlueMountains()
    # region = RoyalNationalPark()
    # region.print_tile_dimensions()
    gps = Route(gpx_path='routes/mittagong_to_blackheath.gpx', srtm=True)
    print(gps.calculate_length_2d())
    print(gps.calculate_length_3d())
    print(gps.calculate_uphill_downhill())
    print(gps.get_elevation_extremes())
    region.generate_route_map(
        route=gps, filename='mittagong_to_blackheath', output_folder='routes/out/'
    )
    # (im, _) = region.generate_region_map(route=None, crop=None, entire_extent=True)
    # im.save('blue_mts_master.jpg')

    # pdf = RouteMapPDF()
    # pdf.create_pdf('test.pdf')


if __name__ == "__main__":
    test()
