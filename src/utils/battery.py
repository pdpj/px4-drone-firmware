import asyncio
from mavsdk import System
from mavsdk.telemetry import Position
import math

async def get_battery_percentage(drone):
    async for battery in drone.telemetry.battery():
        return battery.remaining_percent * 1

#battery_percentage = 80

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # output distance in meters

async def get_drone_position(drone):
    async for position in drone.telemetry.position():
        return position

def calculate_total_distance(waypoints):
    total_distance = 0.0
    for i in range(len(waypoints) - 1):
        total_distance += haversine_distance(waypoints[i][0], waypoints[i][1], waypoints[i + 1][0], waypoints[i + 1][1])
    return total_distance

async def can_complete_mission(drone, waypoints, consumption_rate):
    # Get current battery percentage
    print(await get_battery_percentage(drone))
    battery_percentage = await get_battery_percentage(drone)
    
    # Get current drone position (launch point)
    current_position = await get_drone_position(drone)
    launch_lat = current_position.latitude_deg
    launch_lon = current_position.longitude_deg
    #launch_lat = 39.818569
    #launch_lon = -7.51559
    
    # Add launch point as the first and last waypoint
    waypoints.insert(0, (launch_lat, launch_lon))
    waypoints.append((launch_lat, launch_lon))
    
    # Calculate total distance for the mission
    total_distance = calculate_total_distance(waypoints)
    
    # Check if the battery is enough for the total distance
    if battery_percentage > (total_distance * consumption_rate):
        return True, battery_percentage, total_distance
    else:
        return False, battery_percentage, total_distance

async def main():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    # Define your waypoints (latitude, longitude)
    waypoints = [
        (39.819433, -7.51534),
        (39.819354, -7.514699),
        (39.819052, -7.515)
    ]

    # Define the consumption rate (battery percentage per meter)
    consumption_rate = 0.0083  # based on the rough estimation

    # Check if the drone can complete the mission
    can_reach, battery_percentage, total_distance = await can_complete_mission(drone, waypoints, consumption_rate)
    
    if can_reach:
        print(f"Drone can complete the mission. Battery remaining: {battery_percentage:.2f}%. Total distance: {total_distance:.2f} meters.")
    else:
        print(f"Drone cannot complete the mission. Battery remaining: {battery_percentage:.2f}%. Total distance: {total_distance:.2f} meters.")

if __name__ == "__main__":
    asyncio.run(main())

