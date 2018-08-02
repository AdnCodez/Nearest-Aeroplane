"""
    File name: test.py
    Author: AdnHt
    Date created: 4/20/2018
    Date last modified: 25/05/2018
    Python Version: 3.6
"""

# Challenge link: https://www.reddit.com/r/dailyprogrammer/comments/8i5zc3/20180509_challenge_360_intermediate_find_the/
# Used links:
#   https://opensky-network.org/apidoc/rest.html#own-states
#   https://en.wikipedia.org/wiki/Haversine_formula
#   https://en.wikipedia.org/wiki/Great-circle_distance


import json
import subprocess
import sys
from math import cos, asin, sqrt, pi

# Checking if the requests package exit and install it

package = 'requests'

try:
    __import__(package)
except ImportError:
    try:
        subprocess.call([sys.executable, '-m', 'pip', 'install', '{}'.format(package)])
    except SystemExit as e:
        pass

import requests

# Global vars
API_LINK = 'https://opensky-network.org/api/states/all'
lat = float(input('Enter here lat: '))
lon = float(input('Enter here lon: '))
# Radius of earth is R = 6371 km R*2 = 12742
RADIUS = 12742


def distance(p, v):
    # The Haversine formula
    a = (1 - cos((p['lat'] - v['lat']) * pi)) / 2 + cos(v['lat'] * pi) * cos(p['lat'] * pi) * (
                1 - cos((p['lon'] - v['lon']) * pi)) / 2
    return RADIUS * asin(sqrt(a))


def nearest_aeroplane(result, lat, lon):
    v = {'lat': lat, 'lon': lon}
    return min(result, key=lambda p: distance(p, v))


def load_data():
    global data
    tempDataList = {}
    try:
        data = requests.get(API_LINK)
    except requests.exceptions.HTTPError as e:
        print(' HTTP error: {}'.format(e))

    # checking the status of the link above
    # print(data.status_code)
    if data is not None:
        tempDataList['content'] = json.loads(data.content)
        result = []
        for i in tempDataList['content']['states']:
            if type(i[5]) is float and type(i[6]) is float:
                dc = {'lat': i[6], 'lon': i[5]}
                result.append(dc)
        tempDataList['result'] = result
        return tempDataList


def result(lat, lon):
    data = load_data()
    var = nearest_aeroplane(data['result'], lat, lon)
    res = ''
    for i in data['content']['states']:
        if var['lat'] == i[6] and var['lon'] == i[5]:
            res += 'Callsign: {}\n'.format(i[1])
            res += 'Lattitude: {}\n'.format(i[6])
            res += 'Longitude: {}\n'.format(i[5])
            res += 'Geometric Altitude: {}\n'.format(i[7])
            res += 'Country of origin: {}\n'.format(i[2])
            res += 'ICAO24 ID: {}\n'.format(i[0])

    return res


def main():
    print(result(lat, lon))


if __name__ == "__main__":
    main()
