from math import radians, sin, cos, sqrt, atan2

def calculate_distance(user_location, rest_location):
    if user_location is None or rest_location is None:
        return float('inf')
    lat1 = radians(user_location.y)
    lon1 = radians(user_location.x)
    lat2 = radians(rest_location.y)
    lon2 = radians(rest_location.x)
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c
    return round(distance, 3)