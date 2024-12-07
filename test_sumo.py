import os
os.environ["SUMO_HOME"] = "venv/bin/lib/sumo"  # Update this path
os.environ["PYTHONPATH"] = f"{os.environ['SUMO_HOME']}/tools"
import traci

# Set SUMO environment variables


# Start SUMO
try:
    traci.start(["venv/bin/sumo", "-c", "intersection.sumocfg"])  # Use sumo-gui for GUI mode
    step = 0
    while step < 100:
        traffic_lights = traci.trafficlight.getIDList()  # Get list of traffic lights
        for tl_id in traffic_lights:
            state = traci.trafficlight.getRedYellowGreenState(tl_id)
            print(f"Traffic light {tl_id} state: {state}")
        traci.simulationStep()  # Advance simulation by one step
        vehicles = traci.vehicle.getIDList()  # Get list of vehicles
        # print(f"Step {step}: {len(vehicles)} vehicles, {len(traffic_lights)} traffic lights")

        for veh_id in vehicles:
            lane_id = traci.vehicle.getLaneID(veh_id)
            print(f"Vehicle {veh_id} lane: {lane_id}")
            vehicle_wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
            print(f"Vehicle {veh_id} wait time: {vehicle_wait_time}")
            speed = traci.vehicle.getSpeed(veh_id)  # Get speed of each vehicle
            print(f"Vehicle {veh_id} speed: {speed}")
        step += 1
    traci.close()  # Close simulation
    print("Simulation completed.")
except Exception as e:
    print(f"Error: {e}")
