import pymongo
import time
from math import sqrt

SPEED = 5
INTERVAL = 1

myclient = pymongo.MongoClient("mongodb://mongo:27017/")
mydb = myclient["groundstation"]
drones = mydb["drone"]

def meter2deg(meter):
    return meter/111111

time.sleep(1)
drone = drones.find_one({"_id":0})
mission = drone["mission"]
wp_index = 0
while 1:
    drone = drones.find_one({"_id":0})
    pos = drone["position"]
    lat = pos["latitude"]
    lng = pos["longitude"]
    last_mission = mission
    mission = drone["mission"]

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
            if distance < meter2deg(SPEED)*2:
                speed = SPEED/5
            scale_lat = dist_lat/distance
            scale_lng = dist_lng/distance

            lat += scale_lat*meter2deg(speed)*INTERVAL
            lng += scale_lng*meter2deg(speed)*INTERVAL

    print(lat,lng)


    drones.update_one({"_id":0},{"$set":{"position":{"latitude":lat, "longitude":lng}}})
    drones.update_one({"_id":0},{"$push":{"trail":{"position": {"latitude":lat, "longitude":lng}}}})
    time.sleep(INTERVAL)
