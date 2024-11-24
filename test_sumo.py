import os
import traci

# Set SUMO environment variables
os.environ["SUMO_HOME"] = "/home/hamza/Documents/master's/AI/AI-TrafficControl/venv/lib/python3.10/site-packages/sumo"  # Update this path
os.environ["PYTHONPATH"] = f"{os.environ['SUMO_HOME']}/tools"

# Start SUMO
try:
    traci.start(["venv/bin/sumo", "-c", "test.sumocfg"])  # Use sumo-gui for GUI mode
    step = 0
    while step < 100:
        traci.simulationStep()  # Advance simulation by one step
        vehicles = traci.vehicle.getIDList()  # Get list of vehicles
        for veh_id in vehicles:
            speed = traci.vehicle.getSpeed(veh_id)  # Get speed of each vehicle
            print(f"Vehicle {veh_id} speed: {speed}")
        step += 1
    traci.close()  # Close simulation
    print("Simulation completed.")
except Exception as e:
    print(f"Error: {e}")
