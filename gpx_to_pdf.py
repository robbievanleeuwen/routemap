from regions import BlueMountains
# from regions import RoyalNationalPark
from maps import Route
from pdfcreate import RouteMapPDF
from PIL import Image


def gpx_to_pdf():
    """Test function."""

    route_name = 'bell_to_wollangambe_crater'

    region = BlueMountains()
    # region = RoyalNationalPark()
    gps = Route(gpx_path='routes/{0}.gpx'.format(route_name), srtm=True)
    print(gps.calculate_length_2d())
    print(gps.calculate_length_3d())
    print(gps.calculate_uphill_downhill())
    print(gps.get_elevation_extremes())
    route_map = region.generate_route_map(route=gps)
    # region.generate_route_map(route=gps, filename=route_name, output_folder='routes/out/')

    pdf = RouteMapPDF(image=route_map, scale=0.8)
    pdf.create_pdf('route.pdf', portrait=False)


if __name__ == "__main__":
    gpx_to_pdf()
