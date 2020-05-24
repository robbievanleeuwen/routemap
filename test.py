from PIL import Image
from pdf2image import convert_from_path
from regions import BlueMountains
from maps import Route


def convert_pdf(path):
    Image.MAX_IMAGE_PIXELS = None

    return convert_from_path(
        path,
        dpi=300,
        fmt='jpeg',
        output_folder='temp'
    )


def test():
    blue_mts = BlueMountains()
    # blue_mts.print_tile_dimensions()

    gps_route = Route(gpx_path=1)
    im = blue_mts.generate_region_map(route=gps_route)

    im.save('img.jpg')


if __name__ == "__main__":
    # convert_pdf(path='maps/blue_mts/springwood.pdf')
    test()
