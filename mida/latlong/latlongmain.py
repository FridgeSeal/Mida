import math
import pandas
import pandas_td as td


def square_coords(src_lat: float, src_long: float, distance: float, bearing: float) -> tuple:
    def f(theta: float):
        r = 6378137  # Equatorial radius of earth according to the WGS84 Standard (Used for GPS)
        delta = distance / r
        phi2 = math.asin(math.sin(src_lat) * math.cos(delta) + math.cos(src_lat) * math.sin(delta) * math.cos(theta))
        lambda2 = src_long + math.atan2(math.sin(theta) * math.sin(delta) * math.cos(src_lat),
                                        math.cos(delta) - math.sin(src_lat) * math.sin(phi2))
        return phi2, lambda2
    return f(bearing), f(bearing + 90 % 360), f(bearing + 180 % 360), f(bearing + 270 % 360)


def main():
    print('Under construction for now')


if __name__ == '__main__':
    main()
