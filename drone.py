import time
import requests
import json
from math import sqrt

SPEED = 25
INTERVAL = 0.3

def meter2deg(meter):
    return meter/111111

time.sleep(1)
mission = json.loads(requests.get("http://app:5000/api/drones/0/mission").text)["mission"]
wp_index = 0
pos = json.loads(requests.get("http://app:5000/api/drones/0/position").text)["position"]
lat = pos["latitude"]
lng = pos["longitude"]
while 1:
    last_mission = mission
    mission = json.loads(requests.get("http://app:5000/api/drones/0/mission").text)["mission"]

    if mission == last_mission and len(mission)>0:
        wp = mission[wp_index]
        dist_lat = wp["latitude"] - lat
        dist_lng = wp["longitude"] - lng
        distance = sqrt(dist_lat**2 + dist_lng**2)
        speed = SPEED
        if distance < meter2deg(SPEED)/4:
            lat = mission[wp_index]["latitude"]
            lng = mission[wp_index]["longitude"]
            wp_index += 1
        else:
            if distance < meter2deg(SPEED):
                speed = SPEED/3
            scale_lat = dist_lat/distance
            scale_lng = dist_lng/distance

            lat += scale_lat*meter2deg(speed)*INTERVAL
            lng += scale_lng*meter2deg(speed)*INTERVAL

    requests.post("http://app:5000/api/drones/0/position", json={"latitude": lat, "longitude": lng})
    time.sleep(INTERVAL)
