import traci
import numpy as np

class Enviornment:

    def __init__(self, config_file, tl_id):
        self.config_file = config_file
        self.tl_id = tl_id
        self.phases = 4
        self.lanes = 3
        self.traffic_flow = 3 # (low, med, high)
        self.num_states = self.traffic_flow ** self.lanes * self.phases    
        # lanes from right -E0 after -E0.74
        # lanes from left E0 E0.29
        # E1 E0.29 
        
    def get_intial_state(self):
        '''get current phase from traci and traffic flow from each lane'''
        state = traci.trafficlight.getRedYellowGreenState(self.tl_id)
        vehicles = traci.vehicle.getIDList()  # Get list of vehicles
        traffic_flow_level1 = 0
        traffic_flow_level2 = 0
        traffic_flow_level3 = 0
        self.wait_time_level1 = 0
        self.wait_time_level2 = 0
        self.wait_time_level3 = 0
        for veh_id in vehicles:
            lane_id = traci.vehicle.getRoadID(veh_id)
            vehicle_wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
            if lane_id == "-E0":
                traffic_flow_level1 += 1
                self.wait_time_level1 += vehicle_wait_time
            elif lane_id == "E0":
                traffic_flow_level2 += 1
                self.wait_time_level2 += vehicle_wait_time
            elif lane_id == "E1":
                traffic_flow_level3 += 1
                self.wait_time_level3 += vehicle_wait_time

        
