import json
import urllib

import requests
import sys

def get_distance(coordinate_1, coordinate_2):
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(coordinate_1[0])
    lon1 = radians(coordinate_1[1])
    lat2 = radians(coordinate_2[0])
    lon2 = radians(coordinate_2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def calculate_distance_bing(origin, dest):
    api_key = 'Ag6Jfvb-Iz6dhUhuwHpkhx0hLs575XpV8viFXuJbJRoXbrfIYc3MBXvMZICS1fjJ'

    origin_url = 'http://dev.virtualearth.net/REST/v1/Locations?q=%s&key=%s' % (origin, api_key)
    dest_url = 'http://dev.virtualearth.net/REST/v1/Locations?q=%s&key=%s' % (dest, api_key)

    origin_req = requests.get(origin_url)
    dest_req = requests.get(dest_url)

    try:
        origin_point = origin_req.json()['resourceSets'][0]['resources'][0]['point']['coordinates']
        dest_point = dest_req.json()['resourceSets'][0]['resources'][0]['point']['coordinates']
    except Exception: # TODO: in case it doesnt recognize the city - take care!!!
        return -1

    distance = get_distance(origin_point, dest_point)
    return distance


def calculateDistance():
    api_key = 'AIzaSyB9P-1lxbSHgoXckhambqAj82khKGMK36s'

    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

    origins = ['Vancouver, BC', 'Seattle']
    destinations = ['San Francisco', 'Victoria, BC']


    payload = {
        'origins': '|'.join(origins),
        'destinations': '|'.join(destinations),
        'mode': 'driving',
        'key': api_key
    }


    r = requests.get(url, params=payload)
    print("r.url: " + r.url)


    if r.status_code != 200:
        print('HTTP status code {} received, program terminated.'.format(r.status_code))
    else:
        try:
            print("locationnnnnnnn")
            x = json.loads(r.text)
            print("r.text = " + r.text)
            for isrc, src in enumerate(x['origin_addresses']):
                for idst, dst in enumerate(x['destination_addresses']):
                    row = x['rows'][isrc]
                    cell = row['elements'][idst]
                    if cell['status'] == 'OK':
                        print('{} to {}: {}, {}.'.format(src, dst, cell['distance']['text'], cell['duration']['text']))
                    else:
                        print('{} to {}: status = {}'.format(src, dst, cell['status']))

            with open('C:\\Users\\Tal\\PycharmProjects\\server\\jobmatcher\\server\\utils\\location\\gdmpydemo.json',
                      'w') as f:
                f.write(r.text)

        except:
            print('Error while parsing JSON response, program terminated.')




