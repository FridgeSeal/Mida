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
