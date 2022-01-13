#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Sumedh Salvi

# !/usr/bin/env python3
import sys
import heapq
import collections
from decimal import getcontext

import numpy as np
import math


def road_seg():
    file = open('road-segments.txt', 'r')
    lines = file.read().splitlines()
    roads = collections.defaultdict(list)
    for i in lines:
        k = i.split(" ")

        city_start = k[0].strip()
        city_end = k[1].strip()
        distance = (k[2].strip())
        speed_limit = (k[3].strip())
        time = int(distance) / int(speed_limit)
        highway_name = k[4].strip()

        roads[city_start].append(
            city_end + ":" + distance + ":" + speed_limit + ":" + highway_name + ":" + str.format('{0:.5f}',
                                                                                                  time))
        roads[city_end].append(
            city_start + ":" + distance + ":" + speed_limit + ":" + highway_name + ":" + str.format('{0:.5f}',
                                                                                                    time))
    return roads


def city_gps(city):
    location = {}
    with open('city-gps.txt', 'r') as f:
        for line in f.readlines():
            data_gps = line.split()
            city1 = data_gps[0]
            if data_gps[0] != "":
                if data_gps[1] != "" and data_gps[2] != "":
                    latitude = float(data_gps[1])
                    longitude = float(data_gps[2])
                    location[city1] = (latitude, longitude)
                else:
                    location[city1] = (0, 0)
    if city in location:
        return location[city]
    else:
        return 0, 0


def get_edited_list_of_us_states():
    list_of_us_states = ['Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                         'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                         'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
                         'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
                         'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
                         'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
                         'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
    edited_list_of_us_states = ['_' + state.replace(" ", "_") for state in list_of_us_states]
    return edited_list_of_us_states


def get_states_visited_count(roads_visited):
    edited_list_of_us_states = get_edited_list_of_us_states()
    states_in_visited = [city.split(',')[1] for city in roads_visited]
    cleaned_states_in_visited = set(
        [state for state in states_in_visited if '&' not in states_in_visited and state in edited_list_of_us_states])
    states_visited_count = len(cleaned_states_in_visited)
    print("STATES_VISITED:", states_visited_count)
    return states_visited_count


def get_states_not_visited_count(roads_visited):
    total_state_count = 48
    return total_state_count - get_states_visited_count(roads_visited)


def successor(roads, city):
    successor_data = []
    for i in roads[city]:
        i = i.split(":")
        successor_data.append((1, i[1], i[4], i[3], i[2], i[0]))
    return successor_data


def get_route(start, end, cost):
    fringe = []
    visited = []
    heapq.heapify(fringe)
    roads = road_seg()

    visited.append(start)
    if not cost == 'statetour':
        heapq.heappush(fringe, (0, 0, 0, 0, 0, "", "", 0, start))
        # Priority,segments,distance,time,delivery,highway-name,path,speed,current_city
    else:
        heapq.heappush(fringe, (get_states_not_visited_count(visited), 0, 0, 0, 0, "", "", 0, start))

    if cost == "segments":
        route_taken = []
        p = 0
        while fringe:
            (priority, total_segment, total_distance, total_time, total_delivery_time, full_path, total_highway,
             total_speed, current_city) = heapq.heappop(fringe)

            (lat1, long1) = city_gps(current_city)
            (lat2, long2) = city_gps(end)
            dist_between_cities = math.sqrt(((lat1 - lat2)**2)+((long1-long2)**2))

            for (seg, distance, time, highway, speed, city) in successor(roads, current_city):

                if current_city == end:
                    path_temporary = full_path.split(' ')
                    length_path_temporary = len(path_temporary)
                    highway_temporary = total_highway.split(' ')
                    for m in range(1, length_path_temporary):
                        for k in roads[path_temporary[m]]:
                            k = k.split(':')
                            if start in k:
                                d = k[1]
                                start = path_temporary[m]
                        if (path_temporary[m] != '') or highway_temporary[m] != '':
                            route_taken.append((path_temporary[m], highway_temporary[m] + " for " + str(d) + " miles"))

                    return {"total-segments": int(total_segment), "total-miles": float(total_distance),
                            "total-hours": float(total_time), "total-delivery-hours": float(total_delivery_time),
                            "route-taken": route_taken}

                if city not in visited:
                    current_distance = float(total_distance) + float(distance)
                    current_segment = float(total_segment) + float(seg)
                    current_time = float(total_time) + float(time)

                    extra_time = 2 * (float(total_time) + float(time))
                    if float(speed) >= 50:
                        probability_of_mistake = math.tanh(float(distance)/1000)
                    else:
                        probability_of_mistake = 0
                    current_delivery = float(total_delivery_time) + float(time) + probability_of_mistake * extra_time

                    current_speed = float(total_speed) + float(speed)
                    p = float(current_segment) + dist_between_cities

                    heapq.heappush(fringe, (p, current_segment, current_distance, current_time, current_delivery,
                                            str(full_path) + str(' ') + str(city), str(total_highway) + str(' ')
                                            + str(highway), current_speed, city))
                    visited.append(city)

    elif cost == "distance":
        route_taken = []
        p = 0
        while fringe:
            (priority, total_segment, total_distance, total_time, total_delivery_time, full_path, total_highway,
             total_speed, current_city) = heapq.heappop(fringe)

            (lat1, long1) = city_gps(current_city)
            (lat2, long2) = city_gps(end)
            dist_between_cities = math.sqrt(((lat1 - lat2)**2)+((long1-long2)**2))

            for (seg, distance, time, highway, speed, city) in successor(roads, current_city):

                if current_city == end:
                    path_temporary = full_path.split(' ')
                    length_path_temporary = len(path_temporary)
                    highway_temporary = total_highway.split(' ')
                    for m in range(1, length_path_temporary):
                        for k in roads[path_temporary[m]]:
                            k = k.split(':')
                            if start in k:
                                d = k[1]
                                start = path_temporary[m]
                        if (path_temporary[m] != '') or highway_temporary[m] != '':
                            route_taken.append((path_temporary[m], highway_temporary[m] + " for " + str(d) + " miles"))

                    return {"total-segments": int(total_segment), "total-miles": float(format((total_distance))),
                            "total-hours": float(format((total_time))),
                            "total-delivery-hours": float(total_delivery_time), "route-taken": route_taken}

                if city not in visited:
                    current_distance = float(total_distance) + float(distance)
                    current_segment = float(total_segment) + float(seg)
                    current_time = float(total_time) + float(time)

                    extra_time = 2 * (float(total_time) + float(time))
                    if float(speed) >= 50:
                        probability_of_mistake = math.tanh(float(distance)/1000)
                    else:
                        probability_of_mistake = 0
                    current_delivery = float(total_delivery_time) + float(time) + probability_of_mistake * extra_time

                    current_speed = float(total_speed) + float(speed)
                    p = float(distance) + float(total_distance) + dist_between_cities

                    heapq.heappush(fringe, (p, current_segment, current_distance, current_time, current_delivery,
                                            str(full_path) + str(' ') + str(city), str(total_highway) + str(' ')
                                            + str(highway), current_speed, city))

                    visited.append(city)

    elif cost == "time":
        route_taken = []
        p = 0
        while fringe:
            (priority, total_segment, total_distance, total_time, total_delivery_time, full_path, total_highway,
             total_speed, current_city) = heapq.heappop(fringe)

            (lat1, long1) = city_gps(current_city)
            (lat2, long2) = city_gps(end)
            dist_between_cities = math.sqrt(((lat1 - lat2)**2)+((long1-long2)**2))

            for (seg, distance, time, highway, speed, city) in successor(roads, current_city):

                if current_city == end:
                    path_temporary = full_path.split(' ')
                    length_path_temporary = len(path_temporary)
                    highway_temporary = total_highway.split(' ')
                    for m in range(1, length_path_temporary):
                        for k in roads[path_temporary[m]]:
                            k = k.split(':')
                            if start in k:
                                d = k[1]
                                start = path_temporary[m]
                        if (path_temporary[m] != '') or highway_temporary[m] != '':
                            route_taken.append((path_temporary[m], highway_temporary[m] + " for " + str(d) + " miles"))

                    return {"total-segments": int(total_segment), "total-miles": float(total_distance),
                            "total-hours": float(total_time), "total-delivery-hours": float(total_delivery_time),
                            "route-taken": route_taken}

                if city not in visited:
                    current_distance = float(total_distance) + float(distance)
                    current_segment = float(total_segment) + float(seg)
                    current_time = float(total_time) + float(time)

                    extra_time = 2 * (float(total_time) + float(time))
                    if float(speed) >= 50:
                        probability_of_mistake = math.tanh(float(distance)/1000)
                    else:
                        probability_of_mistake = 0
                    current_delivery = float(total_delivery_time) + float(time) + probability_of_mistake * extra_time

                    current_speed = float(total_speed) + float(speed)
                    p = current_time * float(speed) + dist_between_cities

                    heapq.heappush(fringe, (p, current_segment, current_distance, current_time, current_delivery,
                                            str(full_path) + str(' ') + str(city), str(total_highway) + str(' ')
                                            + str(highway), current_speed, city))
                    visited.append(city)

    elif cost == "delivery":
        route_taken = []
        p = 0
        while fringe:
            (priority, total_segment, total_distance, total_time, total_delivery_time, full_path, total_highway,
             total_speed, current_city) = heapq.heappop(fringe)

            (lat1, long1) = city_gps(current_city)
            (lat2, long2) = city_gps(end)
            dist_between_cities = math.sqrt(((lat1 - lat2)**2)+((long1-long2)**2))

            for (seg, distance, time, highway, speed, city) in successor(roads, current_city):

                if current_city == end:
                    path_temporary = full_path.split(' ')
                    length_path_temporary = len(path_temporary)
                    highway_temporary = total_highway.split(' ')
                    for m in range(1, length_path_temporary):
                        for k in roads[path_temporary[m]]:
                            k = k.split(':')
                            if start in k:
                                d = k[1]
                                start = path_temporary[m]
                        if (path_temporary[m] != '') or highway_temporary[m] != '':
                            route_taken.append((path_temporary[m], highway_temporary[m] + " for " + str(d) + " miles"))

                    return {"total-segments": int(total_segment), "total-miles": float(total_distance),
                            "total-hours": float(total_time), "total-delivery-hours": float(total_delivery_time),
                            "route-taken": route_taken}

                if city not in visited:
                    current_distance = float(total_distance) + float(distance)
                    current_segment = float(total_segment) + float(seg)
                    current_time = float(total_time) + float(time)

                    extra_time = 2 * (float(total_time) + float(time))
                    if float(speed) >= 50:
                        probability_of_mistake = math.tanh(float(distance)/1000)
                    else:
                        probability_of_mistake = 0
                    current_delivery = float(total_delivery_time) + float(time) + probability_of_mistake * extra_time

                    current_speed = float(total_speed) + float(speed)
                    p = current_delivery * float(speed) + dist_between_cities

                    heapq.heappush(fringe, (p, current_segment, current_distance, current_time, current_delivery,
                                            str(full_path) + str(' ') + str(city), str(total_highway) + str(' ')
                                            + str(highway), current_speed, city))
                    visited.append(city)

    elif cost == "statetour":
        route_taken = []
        p = 0
        edited_list_of_us_states = get_edited_list_of_us_states()
        while fringe:
            (priority, total_segment, total_distance, total_time, total_delivery_time, full_path, total_highway,
             total_speed, current_city) = heapq.heappop(fringe)

            (lat1, long1) = city_gps(current_city)
            (lat2, long2) = city_gps(end)
            dist_between_cities = math.sqrt(((lat1 - lat2) ** 2) + ((long1 - long2) ** 2))

            for (seg, distance, time, highway, speed, city) in successor(roads, current_city):
                if city.split(',')[1] in edited_list_of_us_states:
                    full_path_cities_list = full_path.split(" ")
                    full_path_cities_list.remove('')
                    if current_city == end and get_states_not_visited_count(full_path_cities_list) <= 1:
                        path_temporary = full_path.split(' ')
                        length_path_temporary = len(path_temporary)
                        highway_temporary = total_highway.split(' ')
                        for m in range(1, length_path_temporary):
                            for k in roads[path_temporary[m]]:
                                k = k.split(':')
                                if start in k:
                                    d = k[1]
                                    start = path_temporary[m]
                            if (path_temporary[m] != '') or highway_temporary[m] != '':
                                route_taken.append((path_temporary[m], highway_temporary[m] + " for " + str(d)
                                                    + " miles"))

                            return {"total-segments": int(total_segment), "total-miles": float(total_distance),
                                    "total-hours": float(total_time),
                                    "total-delivery-hours": float(total_delivery_time), "route-taken": route_taken}

                    if city not in visited:
                        current_distance = float(total_distance) + float(distance)
                        current_segment = float(total_segment) + float(seg)
                        current_time = float(total_time) + float(time)

                        extra_time = 2 * (float(total_time) + float(time))
                        if float(speed) >= 50:
                            probability_of_mistake = math.tanh(float(distance) / 1000)
                        else:
                            probability_of_mistake = 0
                        current_delivery = float(total_delivery_time) + float(
                            time) + probability_of_mistake * extra_time

                        current_speed = float(total_speed) + float(speed)
                        full_path_cities_list = full_path.split(" ")
                        full_path_cities_list.remove('')

                        p = get_states_not_visited_count(full_path_cities_list) + float(
                            current_segment) + dist_between_cities

                        heapq.heappush(fringe, (p, current_segment, current_distance, current_time, current_delivery,
                                                str(full_path) + str(' ') + str(city),
                                                str(total_highway) + str(' ') + str(highway),
                                                current_speed, city))
                        visited.append(city)


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery", "statetour"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])