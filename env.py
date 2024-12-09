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
        
    def get_state(self):
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

        return state, traffic_flow_top_right, traffic_flow_bot, traffic_flow_bot_left 
    
    def get_reward(self, new_state, old_state):
        state_map = {"low": 0, "med": 1, "high": 2}
        _, traffic_flow_top_right, traffic_flow_bot, traffic_flow_bot_left = new_state
        _, traffic_flow_top_right_old, traffic_flow_bot_old, traffic_flow_bot_left_old = old_state
        reward = 0
        # top right lane
        if traffic_flow_top_right[state_map] > traffic_flow_top_right_old[state_map]:
            reward -= 50 * traffic_flow_top_right[state_map]
        elif traffic_flow_top_right[state_map] < traffic_flow_top_right_old[state_map]:
            reward += 50 * traffic_flow_top_right[state_map]
        elif traffic_flow_top_right[state_map] == traffic_flow_top_right_old[state_map]:
            if traffic_flow_top_right[state_map] == 0:
                reward += 10
            else:
                reward -= 20
        
        # bottom lane
        if traffic_flow_bot[state_map] > traffic_flow_bot_old[state_map]:
            reward -= 50 * traffic_flow_bot[state_map]
        elif traffic_flow_bot[state_map] < traffic_flow_bot_old[state_map]:
            reward += 50 * traffic_flow_bot[state_map]
        elif traffic_flow_bot[state_map] == traffic_flow_bot_old[state_map]:
            if traffic_flow_bot[state_map] == 0:
                reward += 10
            else:
                reward -= 20
        # bottom left lane
        if traffic_flow_bot_left[state_map] > traffic_flow_bot_left_old[state_map]:
            reward -= 50 * traffic_flow_bot_left[state_map]
        elif traffic_flow_bot_left[state_map] < traffic_flow_bot_left_old[state_map]:
            reward += 50 * traffic_flow_bot_left[state_map]
        elif traffic_flow_bot_left[state_map] == traffic_flow_bot_left_old[state_map]:
            if traffic_flow_bot_left[state_map] == 0:
                reward += 10
            else:
                reward -= 20
        return reward
    
    def perform_action(self, action):
        traci.trafficlight.setRedYellowGreenState(self.tl_id, action)
        traci.simulationStep()
        new_state = self.get_state()
        return new_state