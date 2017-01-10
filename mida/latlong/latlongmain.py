import math
# import pandas
# import pandas_td as td
import numba
import timeit


@numba.jit(signature=(numba.float64, numba.float64, numba.float64), nopython=True)
def square_coords_numba(src_lat: float, src_long: float, distance: float) -> tuple:
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


def square_coords_plain(src_lat: float, src_long: float, distance: float) -> tuple:
    """
    Returns a tuple of coordinates that form the boundary lines of a square whose sides are a specified distance
    away from the the source points (scr_lat, src_long)
    :param src_lat: latitude of the source point
    :param src_long: longitude of the source point
    :param distance: maximum distance from source point
    :return: tuple of points in the following order: North, East, South West
    """
    def f(theta: float):
        r = 6378137  # Equatorial radius of earth according to the WGS84 Standard (Used for GPS)
        delta = distance / r
        phi2 = math.asin(math.sin(src_lat) * math.cos(delta) + math.cos(src_lat) * math.sin(delta) * math.cos(theta))
        lambda2 = src_long + math.atan2(math.sin(theta) * math.sin(delta) * math.cos(src_lat),
                                        math.cos(delta) - math.sin(src_lat) * math.sin(phi2))
        return phi2, lambda2
    return f(0), f(90), f(180), f(270)


@numba.jit(signature=(numba.float64, numba.float64, numba.float64, numba.float64, numba.float64))
def within_numba(src_lat: float, src_long: float, cndt_lat: float, cndt_long: float, distance: float) -> bool:
    """
    Takes a source point, a candidate point and a distance and returns True if the candidate point is within a radius
    of distance of the source point. Uses the Haversine formula for balance between acccuracy and simplicity
    :param src_lat: latitude of source point
    :param src_long: longitude of source point
    :param distance: test radius around source point
    :param cndt_lat: latitude of candidate point
    :param cndt_long: longitude of candidate point
    :return: a bool designating whether the the candidate point is within radius 'distance' of source point
    """
    # TODO maybe vectorise this to handle being passed a source point and a list/pandas Series of candidate points?
    r: float = 6378137.0  # WGS-84 ellipsoid semi-major axis parameter used for Earth radius
    d = 2 * r * math.asin(math.sqrt((0.5 * (1 - math.cos(cndt_lat - src_lat))) +
                                    (math.cos(src_lat) * math.cos(cndt_lat) *
                                     0.5 * (1 - math.cos(cndt_long - src_long)))))  # Haversine formula
    if d < distance:
        isinregion = True
    else:
        isinregion = False
    return isinregion


def within_plain(src_lat: float, src_long: float, cndt_lat: float, cndt_long: float, distance: float) -> bool:
    """
    Takes a source point, a candidate point and a distance and returns True if the candidate point is within a radius
    of distance of the source point. Uses the Haversine formula for balance between acccuracy and simplicity
    :param src_lat: latitude of source point
    :param src_long: longitude of source point
    :param distance: test radius around source point
    :param cndt_lat: latitude of candidate point
    :param cndt_long: longitude of candidate point
    :return: a bool designating whether the the candidate point is within radius 'distance' of source point
    """
    # TODO maybe vectorise this to handle being passed a source point and a list/pandas Series of candidate points?
    r: float = 6378137.0  # WGS-84 ellipsoid semi-major axis parameter used for Earth radius
    d = 2 * r * math.asin(math.sqrt((0.5 * (1 - math.cos(cndt_lat - src_lat))) +
                                    (math.cos(src_lat) * math.cos(cndt_lat) *
                                     0.5 * (1 - math.cos(cndt_long - src_long)))))  # Haversine formula
    if d < distance:
        isinregion = True
    else:
        isinregion = False
    return isinregion


def timeexecution(func_name: str, test_func: object, **kwargs):
    time_list = []
    for i in range(1000):
        start = timeit.default_timer()
        test_func(kwargs)
        end = timeit.default_timer()
        exec_time = end - start
        time_list.append(exec_time)
    print(f'{func_name} took  on average {exec_time} to run')


def main():
    print('Under construction for now')
    data = {'base_lat': -36.92145616,
            'base_long': 174.66654809,
            'candidate1_lat': -36.954954955,
            'candidate1_long': 174.902135476,
            'candidate2_lat': -36.55154,
            'candidate2_long': 174.39573,
            'test_dist': 64
            }
    timeexecution()
    return None

if __name__ == '__main__':
    main()
