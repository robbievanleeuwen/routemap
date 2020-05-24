from regions import BlueMountains
from maps import Route


def test():
    blue_mts = BlueMountains()
    gps = Route(gpx_path='routes/upper_grose.gpx', srtm=True)
    blue_mts.generate_route_map(route=gps, filename='upper_grose')


if __name__ == "__main__":
    test()
