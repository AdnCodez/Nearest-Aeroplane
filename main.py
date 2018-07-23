import requests
import json
from math import cos, asin, sqrt

lat = float(input('Enter here lat: '))
lon = float(input('Enter here lon: '))


def main(lat, lon):
    tempDataList = []
    v = {'lat': lat, 'lon': lon}

    data = requests.get("https://opensky-network.org/api/states/all")
    # checking the status of the link above
    # print(data.status_code)

    data = json.loads(data.content)
    # print(data)
    states = data['states']

    for i in states:
        if type(i[5]) is float and type(i[6]) is float:
            dc = {'lat': i[6], 'lon': i[5]}
            tempDataList.append(dc)

    def distance(lat1, lon1, lat2, lon2):
        p = 0.017453292519943295  # pi / 180
        # The Haversine formula
        a = (1 - cos((lat2 - lat1) * p)) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a))  # Radius of earth is R = 6371 km R*2 = 12742

    def closest(data, v):
        return min(data, key=lambda p: distance(v['lat'], v['lon'], p['lat'], p['lon']))

    var = closest(tempDataList, v)
    # print(var)
    res = ''
    for i in states:
        if var['lat'] == i[6] and var['lon'] == i[5]:
            res += 'Callsign: {}\n'.format(i[1])
            res += 'Lattitude: {}\n'.format(i[6])
            res += 'Longitude: {}\n'.format(i[5])
            res += 'Geometric Altitude: {}\n'.format(i[7])
            res += 'Country of origin: {}\n'.format(i[2])
            res += 'ICAO24 ID: {}\n'.format(i[0])

    return res


print(main(lat, lon))

# Challenge link: https://www.reddit.com/r/dailyprogrammer/comments/8i5zc3/20180509_challenge_360_intermediate_find_the/
# Used links:
#   https://opensky-network.org/apidoc/rest.html#own-states
#   https://en.wikipedia.org/wiki/Haversine_formula
#   https://en.wikipedia.org/wiki/Great-circle_distance
# To look at later:
#   https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude

