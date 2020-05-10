import os
import time
import requests
import json
from math import sqrt

SPEED = 25
INTERVAL = 0.3

drone_id = os.environ["DRONE_ID"] or 0
print(drone_id)

def meter2deg(meter):
    return meter/111111

def get_pos():
    return json.loads(requests.get(f"http://app:5000/api/drones/{drone_id}/position").text)["position"]

def get_mission():
    try:
        return json.loads(requests.get(f"http://app:5000/api/drones/{drone_id}/area").text)
    except:
        return []

time.sleep(1)

wp_index = 0
mission = get_mission()
pos = get_pos()
lat = pos["latitude"]
lng = pos["longitude"]
while 1:
    last_mission = mission
    mission = get_mission()
    waypoints = mission["waypoints"]

    if mission == last_mission and len(waypoints)>0:
        wp = waypoints[wp_index]
        dist_lat = wp[0] - lat
        dist_lng = wp[1] - lng
        distance = sqrt(dist_lat**2 + dist_lng**2)
        speed = SPEED
        if distance < meter2deg(SPEED)/4:
            lat = waypoints[wp_index][0]
            lng = waypoints[wp_index][1]
            wp_index += 1
            requests.post(f"http://app:5000/api/areas/{mission['_id']}/reached", json={"index":wp_index})
        else:
            if distance < meter2deg(SPEED):
                speed = SPEED/3
            scale_lat = dist_lat/distance
            scale_lng = dist_lng/distance

            lat += scale_lat*meter2deg(speed)*INTERVAL
            lng += scale_lng*meter2deg(speed)*INTERVAL
    else:
        wp_index = 0

    requests.post(f"http://app:5000/api/drones/{drone_id}/position", json={"latitude": lat, "longitude": lng})
    time.sleep(INTERVAL)
