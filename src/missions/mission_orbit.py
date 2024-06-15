#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
from mavsdk.action import OrbitYawBehavior
#Latitude: 39.81945 | Longitude: -7.515364

mission_items_temp = []
mission_items = [MissionItem(39.819305,    # New latitude
            			     -7.514731,    # New longitude
           			     25,           # Altitude
		                     10,
		                     True,
		                     float('nan'),
		                     float('nan'),
		                     MissionItem.CameraAction.NONE,
		                     float('nan'),
		                     float('nan'),
		                     float('nan'),
		                     float('nan'),
		                     float('nan'),
		                     MissionItem.VehicleAction.NONE),
		   MissionItem(39.81945,    # New latitude
            			     -7.515364,    # New longitude
           			     25,           # Altitude
		                     10,
		                     True,
		                     float('nan'),
		                     float('nan'),
		                     MissionItem.CameraAction.NONE,
		                     float('nan'),
		                     float('nan'),
		                     float('nan'),
		                     float('nan'),
		                     float('nan'),
		                     MissionItem.VehicleAction.NONE)]

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking Off")
    await drone.action.takeoff()
    await asyncio.sleep(10)
    
    for i in range(len(mission_items)):
    	mission_items_temp.append(mission_items[i])
    	await move_to_waypoint(drone)
    	lat=mission_items_temp[0].latitude_deg
    	#print(lat)
    	lon=mission_items_temp[0].longitude_deg
    	#print(lon)
    	await perform_orbit(drone,lat,lon)
    	mission_items_temp.clear()

    await drone.action.return_to_launch()
    print("-- Landing")

async def move_to_waypoint(drone):
    mission_plan = MissionPlan(mission_items_temp)
    await drone.mission.upload_mission(mission_plan)
    print("-- Mission uploaded")

    mission_uploaded = False
    async for mission in drone.mission.mission_progress():
        if mission.total > 0:
            mission_uploaded = True
            break
    
    if not mission_uploaded:
        print("-- Mission upload failed")
        return

    await drone.mission.start_mission()
    print("-- Mission started")

    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: {mission_progress.current}/{mission_progress.total}")
        if mission_progress.current == mission_progress.total:
            print(f"Reached waypoint: {mission_progress.current}/{mission_progress.total}")
            break

async def perform_orbit(drone,lat,lon):
    position = await drone.telemetry.position().__aiter__().__anext__()
    orbit_height = position.absolute_altitude_m + 10
    yaw_behavior = OrbitYawBehavior.HOLD_FRONT_TO_CIRCLE_CENTER

    print('Do orbit at 10m height from the ground')
    await drone.action.do_orbit(radius_m=2,
                                velocity_ms=2,
                                yaw_behavior=yaw_behavior,
                                latitude_deg=lat,
                                longitude_deg=lon,
                                absolute_altitude_m=orbit_height)
                                
    #print(f"-- Performing orbit at waypoint ({mission_item.latitude_deg}, {mission_item.longitude_deg})")
    print(f"-- Performing orbit at waypoint")
    # Perform the orbit action here
    await asyncio.sleep(30)  # Placeholder for orbit action

if __name__ == "__main__":
    asyncio.run(run())

