import math
import pandas
import pandas_td as td
import numba

@numba.jit(signature=(numba.float64, numba.float64, numba.float64), nopython=True)
def square_coords(src_lat: float, src_long: float, distance: float) -> tuple:
    """
    Returns a tuple of coordinates that form the boundary lines of a square whose sides are a specified distance
    away from the the source points (scr_lat, src_long)
    :param src_lat: latitude of the source point
    :param src_long: longitude of the source point
    :param distance: maximum distance from source point
    :return: tuple of points in the following order: North, East, South West
    """
    @numba.jit(signature=numba.float64, nopython=True)
    def f(theta: float):
        r = 6378137  # Equatorial radius of earth according to the WGS84 Standard (Used for GPS)
        delta = distance / r
        phi2 = math.asin(math.sin(src_lat) * math.cos(delta) + math.cos(src_lat) * math.sin(delta) * math.cos(theta))
        lambda2 = src_long + math.atan2(math.sin(theta) * math.sin(delta) * math.cos(src_lat),
                                        math.cos(delta) - math.sin(src_lat) * math.sin(phi2))
        return phi2, lambda2
    return f(0), f(90), f(180), f(270)


@numba.jit(signature=(numba.float64, numba.float64, numba.float64))
def within(src_lat: float, src_long: float, distance: float) -> bool:



def main():
    print('Under construction for now')


if __name__ == '__main__':
    main()
