import math
import numba


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
