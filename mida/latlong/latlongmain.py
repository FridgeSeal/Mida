import math
# import pandas
# import pandas_td as td
import numba
import timeit


@numba.jit(signature_or_function=(numba.types.UniTuple(numba.float64, 2))(numba.float64, numba.float64, numba.float64, numba.float64))
def haversine(lat: float, long: float, theta: float, dist: float) -> tuple:
    r = 6371008  # Average radius of Earth according to NASA Earth factsheet
    delta = dist / r
    phi1 = math.radians(lat)
    lambda1 = math.radians(long)
    theta = math.radians(theta)
    phi2 = math.asin(math.sin(phi1) * math.cos(delta) + math.cos(phi1) * math.sin(delta) * math.cos(theta))
    lambda2 = lambda1 + math.atan2(math.sin(theta) * math.sin(delta) * math.cos(phi1),
                                   math.cos(delta) - math.sin(phi1) * math.sin(phi2))
    return math.degrees(phi2), math.degrees(lambda2)


@numba.jit(signature_or_function=(numba.float64, numba.float64, numba.float64))
def square_coords_numba(src_lat: float, src_long: float, distance: float) -> tuple:
    """
    Returns a tuple of coordinates that form the boundary lines of a square whose sides are a specified distance
    away from the the source points (scr_lat, src_long)
    :param src_lat: latitude of the source point
    :param src_long: longitude of the source point
    :param distance: maximum distance from source point
    :return: tuple of points in the following order: North, East, South West
    """
    local_f = haversine
    r_val = (local_f(src_lat, src_long, 0, distance), local_f(src_lat, src_long, 90, distance),
             local_f(src_lat, src_long, 180, distance), local_f(src_lat, src_long, 270, distance))
    return r_val


@numba.jit(signature_or_function=(numba.float64, numba.float64, numba.float64, numba.float64, numba.float64))
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
    r: float = float(6371000.00)  # WGS-84 ellipsoid semi-major axis parameter used for Earth radius
    deltaphi = math.radians(0.5 * (cndt_lat - src_lat))
    deltalambda = math.radians(0.5 * (cndt_long - src_long))
    phi1 = math.radians(src_lat)
    phi2 = math.radians(cndt_lat)
    a = math.sin(deltaphi) * math.sin(deltaphi) + math.cos(phi1) * math.cos(phi2) *\
        math.sin(deltalambda) * math.sin(deltalambda)
    d = 2 * r * math.asin(math.sqrt(a))
    # print('d is ', d)
    if d < distance:
        isinregion = True
    else:
        isinregion = False
    # print(f'The point is in the region: {isinregion} - Numba')
    return isinregion


def timeexecution(func_name: str, test_func: object, **kwargs):
    time_list = []
    for i in range(100):
        # start = timeit.default_timer()
        res = test_func(**kwargs)
        # end = timeit.default_timer()
        # exec_time = end - start
        # time_list.append(exec_time)
    print(f'{func_name} took  on average {sum(time_list)/float(len(time_list))} to run')
    print(f'Best execution time was {min(time_list)} out of 1000 runs')


def main():
    base_lat = -36.92145616
    base_long = 174.66654809
    candidate1_lat = -36.954954955
    candidate1_long = 174.902135476
    candidate2_lat = -36.921149
    candidate2_long = 174.665469
    test_dist = 50
    timeexecution(func_name='square coords numba',
                  test_func=square_coords_numba,
                  src_lat=base_lat,
                  src_long=base_long,
                  distance=test_dist)
    timeexecution(func_name='within_numba',
                  test_func=within_numba,
                  src_lat=base_lat,
                  src_long=base_long,
                  cndt_lat=candidate2_lat,
                  cndt_long=candidate2_long,
                  distance=test_dist)


if __name__ == '__main__':
    main()
