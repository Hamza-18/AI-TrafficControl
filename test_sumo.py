import os
os.environ["SUMO_HOME"] = "venv/bin/lib/sumo"  # Update this path
os.environ["PYTHONPATH"] = f"{os.environ['SUMO_HOME']}/tools"
import traci

# Set SUMO environment variables


# Start SUMO
try:
    traci.start(["venv/bin/sumo-gui", "-n", "intersection.net.xml","-r", "intersection.rou.xml", "--start"])  # Use sumo-gui for GUI mode
    step = 0
    for i in range(10000):
        step=0
        while step < 300:
            print(f"Step {step}")
            traci.simulationStep()  # Advance simulation by one step
            traffic_lights = traci.trafficlight.getIDList()  # Get list of traffic lights
            for tl_id in traffic_lights:
                state = traci.trafficlight.getRedYellowGreenState(tl_id)
                print(f"Traffic light {tl_id} state: {state}")
            # traci.simulationStep()  # Advance simulation by one step
            vehicles = traci.vehicle.getIDList()  # Get list of vehicles
            # print(f"Step {step}: {len(vehicles)} vehicles, {len(traffic_lights)} traffic lights")

            for veh_id in vehicles:
                lane_id = traci.vehicle.getRoadID(veh_id)
                print(f"Vehicle {veh_id} lane: {lane_id}")
                vehicle_wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
                print(f"Vehicle {veh_id} wait time: {vehicle_wait_time}")
                speed = traci.vehicle.getSpeed(veh_id)  # Get speed of each vehicle
                print(f"Vehicle {veh_id} speed: {speed}")
            step += 1
        traci.load(["-n", "intersection.net.xml", "-r", "intersection.rou.xml", "--start"])
    print("Simulation completed.")
except Exception as e:
    print(f"Error: {e}")
