import math
# import pandas
# import pandas_td as td
import numba
import timeit


@numba.jit(signature_or_function=(numba.types.UniTuple(numba.float64, 2))(numba.float64, numba.float64, numba.float64,
                                                                          numba.float64))
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
def generate_square(src_lat: float, src_long: float, distance: float) -> tuple:
    """
    Returns a tuple of coordinates that form the boundary lines of a square whose sides are a specified distance
    away from the the source points (scr_lat, src_long)
    :param src_lat: latitude of the source point
    :param src_long: longitude of the source point
    :param distance: maximum distance from source point
    :return: tuple of points in the following order: North, East, South West
    """
    local_f = haversine
    r_val = (local_f(src_lat, src_long, 0, distance)[0], local_f(src_lat, src_long, 90, distance)[1],
             local_f(src_lat, src_long, 180, distance)[0], local_f(src_lat, src_long, 270, distance)[1])
    # We are specifying the index for each one because we only want the latitude (index 0) on the North and South
    # coordinates and the longitude (index 1) on the East and West coordinates because we are only interested in the
    # boundary values so that we can test membership by simply going 'is point x in a < x_lat < b and c < x_long < d
    return r_val


def within_square(candidate_lat: float, candidate_long: float, bndry_lat1: float, bndry_lat2: float,
                        bndry_long1: float, bndry_long2: float) -> bool:
    """
    Takes a left + right boundary longitudes and top + bottom boundary latitudes, and returns True if the candidate
    point is contained within. Strangely enough, numba.@jit version is slower than plain python version...
    :param candidate_lat: latitude of the point whose membership is being tested
    :param candidate_long: longitude of the point whose membership is being tested
    :param bndry_lat1: left side latitude boundary
    :param bndry_lat2: right side latitude boundary
    :param bndry_long1: top side longitude boundary
    :param bndry_long2: bottom side longitude boundary
    :return: a boolean value indicating whether the point is within the region
    """
    if bndry_lat1 > bndry_lat2:
        bndry_lat1, bndry_lat2 = bndry_lat2, bndry_lat1
    if bndry_long1 > bndry_long2:  # We don't need an explicit else case for these as we don't want to do anything
        bndry_long1, bndry_long2 = bndry_long2, bndry_long1  # in the <= case and it's handled implicitly
    if (bndry_lat1 < candidate_lat < bndry_lat2) and (bndry_long1 < candidate_long < bndry_long2):
        isinregion = True
    else:
        isinregion = False
    return isinregion


@numba.jit(signature_or_function=(numba.float64, numba.float64, numba.float64, numba.float64, numba.float64))
def within_radius(src_lat: float, src_long: float, cndt_lat: float, cndt_long: float, distance: float) -> bool:
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
    a = math.sin(deltaphi) * math.sin(deltaphi) + math.cos(phi1) * math.cos(phi2) * \
                                                  math.sin(deltalambda) * math.sin(deltalambda)
    d = 2 * r * math.asin(math.sqrt(a))
    # print('d is ', d)
    if d < distance:
        isinregion = True
    else:
        isinregion = False
    # print(f'The point is in the region: {isinregion} - Numba')
    return isinregion


def main():
    base_lat = -36.92145616
    base_long = 174.66654809
    candidate1_lat = -36.954954955
    candidate1_long = 174.902135476
    candidate2_lat = -36.921149
    candidate2_long = 174.665469
    test_dist = 50

if __name__ == '__main__':
    main()
