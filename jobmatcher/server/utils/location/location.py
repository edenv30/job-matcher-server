import json
import urllib

import requests
import sys

from jobmatcher.server.modules.job.job import Job
from jobmatcher.server.utils.nltk.extract_details import extract_location

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
    except Exception:  # TODO: in case it doesnt recognize the city - take care!!!
        return -1

    distance = get_distance(origin_point, dest_point)
    return distance


# def calculateDistance():
#     api_key = 'AIzaSyB9P-1lxbSHgoXckhambqAj82khKGMK36s'
#
#     url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
#
#     origins = ['Vancouver, BC', 'Seattle']
#     destinations = ['San Francisco', 'Victoria, BC']
#
#
#     payload = {
#         'origins': '|'.join(origins),
#         'destinations': '|'.join(destinations),
#         'mode': 'driving',
#         'key': api_key
#     }
#
#
#     r = requests.get(url, params=payload)
#     print("r.url: " + r.url)
#
#
#     if r.status_code != 200:
#         print('HTTP status code {} received, program terminated.'.format(r.status_code))
#     else:
#         try:
#             print("locationnnnnnnn")
#             x = json.loads(r.text)
#             print("r.text = " + r.text)
#             for isrc, src in enumerate(x['origin_addresses']):
#                 for idst, dst in enumerate(x['destination_addresses']):
#                     row = x['rows'][isrc]
#                     cell = row['elements'][idst]
#                     if cell['status'] == 'OK':
#                         print('{} to {}: {}, {}.'.format(src, dst, cell['distance']['text'], cell['duration']['text']))
#                     else:
#                         print('{} to {}: status = {}'.format(src, dst, cell['status']))
#
#             with open('C:\\Users\\Tal\\PycharmProjects\\server\\jobmatcher\\server\\utils\\location\\gdmpydemo.json',
#                       'w') as f:
#                 f.write(r.text)
#
#         except:
#             print('Error while parsing JSON response, program terminated.')


# getting job id object & user location. find location's match - return score
def matchHandler(job_id, user_location):
    # print("matchHandler FUNCTION")

    # TODO: add validity checks: if all fields exist, if score = -1 then put error

    total_distance = []
    min_distance = 0
    score = -1
    job_location = []

    job = Job.objects.get(identifier=job_id)
    job_location = extract_location(job.location)

    for x in user_location:
        for y in job_location:
            total_distance.append(calculate_distance_bing(x, y))

    if len(total_distance) != 0:
        min_distance = total_distance[0]
        for n in total_distance:
            if n < min_distance:
                min_distance = n
    else:
        min_distance =1000
    # TODO: do CONSTANT variables for each degree of distance
    if min_distance >= 0 and min_distance <= 20:
        score = 0.99
    elif min_distance >= 20 and min_distance <= 40:
        score = 0.85
    elif min_distance >= 40 and min_distance <= 100:
        score = 0.60
    elif min_distance >= 100 and min_distance <= 200:
        score = 0.20
    elif min_distance >= 200:
        score = 0.1

    # print("score: ")
    # print(score)
    return score

# getting job id object & user location. find location's match - return city
def one_city(job_id, user_location):
    # print("matchHandler FUNCTION")
    # TODO: add validity checks: if all fields exist, if score = -1 then put error
    total_distance = []
    min_distance = 0
    score = -1
    job_location = []

    job = Job.objects.get(identifier=job_id)
    job_location = extract_location(job.location)
    list_dest = []
    for x in user_location:
        for y in job_location:
            dis = calculate_distance_bing(x, y)
            total_distance.append(dis)
            list_dest.append((dis,y))

    if len(total_distance) != 0:
        min_distance = total_distance[0]
        for n in total_distance:
            if n < min_distance:
                min_distance = n
    else:
        min_distance =1000

    for d in list_dest:
        # print('min_distance')
        # print(min_distance)
        # print(d)
        if min_distance==d[0]:
            return d[1]