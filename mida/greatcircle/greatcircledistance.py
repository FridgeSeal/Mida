import math
import numba


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
