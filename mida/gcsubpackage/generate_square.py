import numba
import greatcircledistance


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
    local_f = greatcircledistance.haversine
    r_val = (local_f(src_lat, src_long, 0, distance)[0], local_f(src_lat, src_long, 90, distance)[1],
             local_f(src_lat, src_long, 180, distance)[0], local_f(src_lat, src_long, 270, distance)[1])
    # We are specifying the index for each one because we only want the latitude (index 0) on the North and South
    # coordinates and the longitude (index 1) on the East and West coordinates because we are only interested in the
    # boundary values so that we can test membership by simply going 'is point x in a < x_lat < b and c < x_long < d
    return r_val
