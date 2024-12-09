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
        traffic_flow_top_right = 0
        traffic_flow_bot_left = 0
        traffic_flow_bot = 0
        self.wait_traffic_flow_top_right = 0
        self.wait_traffic_flow_bot_left = 0
        self.wait_traffic_flow_bot = 0
        for veh_id in vehicles:
            lane_id = traci.vehicle.getRoadID(veh_id)
            vehicle_wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
            if lane_id == "-E0":
                traffic_flow_top_right += 1
                self.wait_traffic_flow_top_right += vehicle_wait_time
            elif lane_id == "E0":
                traffic_flow_bot_left += 1
                self.wait_traffic_flow_bot_left += vehicle_wait_time
            elif lane_id == "E1":
                traffic_flow_bot += 1
                self.wait_traffic_flow_bot += vehicle_wait_time
        
        if self.wait_traffic_flow_top_right > 50:
            traffic_flow_top_right = "high"
        elif self.wait_traffic_flow_top_right > 20 and self.wait_traffic_flow_top_right < 50:
            traffic_flow_top_right = "med"
        else:
            traffic_flow_top_right = "low"
        
        if self.wait_traffic_flow_bot_left > 50:
            traffic_flow_bot_left = "high"
        elif self.wait_traffic_flow_bot_left > 20 and self.wait_traffic_flow_bot_left < 50:
            traffic_flow_bot_left = "med"
        else:
            traffic_flow_bot_left = "low"

        if self.wait_traffic_flow_bot > 50:
            traffic_flow_bot = "high"
        elif self.wait_traffic_flow_bot > 20 and self.wait_traffic_flow_bot < 50:
            traffic_flow_bot = "med"
        else:
            traffic_flow_bot = "low"

        return state, traffic_flow_top_right, traffic_flow_bot_left, traffic_flow_bot

        
