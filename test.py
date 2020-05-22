import matplotlib.pyplot as plt
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

    gps_route = Route(gpx_path=1)
    blue_mts.generate_region_map(route=gps_route)

    # plt.imshow(map.combine_images())
    # plt.show()


if __name__ == "__main__":
    # convert_pdf(path='maps/blue_mts/springwood.pdf')
    test()
