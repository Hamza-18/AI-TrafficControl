import traci
import numpy as np

class Enviornment:

    def __init__(self, tl_id):
        self.tl_id = tl_id
        self.phases = 6
        self.lanes = 4
        self.traffic_flow = 3 # (low, med, high)
        self.num_states = self.traffic_flow ** self.lanes * self.phases    
        self.reward = 0

    def get_state(self):
        '''get current phase from traci and traffic flow from each lane'''
        state = traci.trafficlight.getRedYellowGreenState(self.tl_id)
        vehicles = traci.vehicle.getIDList()  # Get list of vehicles
        traffic_flow_top_right = 0
        traffic_flow_bot_left = 0
        traffic_flow_bot = 0
        traffic_flow_top = 0
        self.wait_traffic_flow_top_right = 0
        self.wait_traffic_flow_bot_left = 0
        self.wait_traffic_flow_bot = 0
        self.wait_traffic_flow_top = 0
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
            elif lane_id == "E2":
                traffic_flow_top += 1
                self.wait_traffic_flow_top += vehicle_wait_time
        
        if self.wait_traffic_flow_top_right > 50:
            traffic_flow_top_right = "high"
        elif self.wait_traffic_flow_top_right > 25 and self.wait_traffic_flow_top_right < 50:
            traffic_flow_top_right = "med"
        else:
            traffic_flow_top_right = "low"
        
        if self.wait_traffic_flow_bot_left > 50:
            traffic_flow_bot_left = "high"
        elif self.wait_traffic_flow_bot_left > 25 and self.wait_traffic_flow_bot_left < 50:
            traffic_flow_bot_left = "med"
        else:
            traffic_flow_bot_left = "low"

        if self.wait_traffic_flow_bot > 50:
            traffic_flow_bot = "high"
        elif self.wait_traffic_flow_bot > 25 and self.wait_traffic_flow_bot < 50:
            traffic_flow_bot = "med"
        else:
            traffic_flow_bot = "low"
        
        if self.wait_traffic_flow_top > 50: 
            traffic_flow_top = "high"           
        elif self.wait_traffic_flow_top > 25 and self.wait_traffic_flow_top < 50:
            traffic_flow_top = "med"
        else:
            traffic_flow_top = "low"

        return state, traffic_flow_top_right, traffic_flow_bot, traffic_flow_bot_left, traffic_flow_top 
    
    def get_reward(self, new_state, old_state):
        state_map = {"low": 0, "med": 1, "high": 2}
        _, traffic_flow_top_right, traffic_flow_bot, traffic_flow_bot_left, traffic_flow_top = new_state
        _, traffic_flow_top_right_old, traffic_flow_bot_old, traffic_flow_bot_left_old, traffic_flow_top_old = old_state
        # top right lane
        if state_map[traffic_flow_top_right] > state_map[traffic_flow_top_right_old]:
            self.reward -= 25 *  state_map[traffic_flow_top_right]
        elif state_map[traffic_flow_top_right] < state_map[traffic_flow_top_right_old]:
            self.reward += 50 *  state_map[traffic_flow_top_right]
        elif state_map[traffic_flow_top_right]== state_map[traffic_flow_top_right]:
            if state_map[traffic_flow_top_right] == 0:
                self.reward += 10
            else:
                self.reward -= 5
        
        # bottom lane
        if state_map[traffic_flow_bot] > state_map[traffic_flow_bot_old]:
            self.reward -= 25 * state_map[traffic_flow_bot]
        elif state_map[traffic_flow_bot] < state_map[traffic_flow_bot_old]:
            self.reward += 50 * state_map[traffic_flow_bot]
        elif state_map[traffic_flow_bot] == state_map[traffic_flow_bot_old]:
            if state_map[traffic_flow_bot] == 0:
                self.reward += 10
            else:
                self.reward -= 5
        # bottom left lane
        if state_map[traffic_flow_bot_left] > state_map[traffic_flow_bot_left_old]:
            self.reward -= 25 * state_map[traffic_flow_bot_left]
        elif state_map[traffic_flow_bot_left] < state_map[traffic_flow_bot_left_old]:
            self.reward += 50 * state_map[traffic_flow_bot_left]
        elif state_map[traffic_flow_bot_left] == state_map[traffic_flow_bot_left_old]:
            if state_map[traffic_flow_bot_left] == 0:
                self.reward += 10
            else:
                self.reward -= 5
        # top lane
        if state_map[traffic_flow_top] > state_map[traffic_flow_top_old]:
            self.reward -= 25 * state_map[traffic_flow_top]
        elif state_map[traffic_flow_top] < state_map[traffic_flow_top_old]:
            self.reward += 50 * state_map[traffic_flow_top]
        elif state_map[traffic_flow_top] == state_map[traffic_flow_top_old]:
            if state_map[traffic_flow_top] == 0:
                self.reward += 10
            else:
                self.reward -= 5    
        return self.reward
    
    
    def perform_action(self, action):
        """
        Apply the chosen action and ensure valid traffic light state transitions.
        """
        current_state = traci.trafficlight.getRedYellowGreenState(self.tl_id)
        print(f"Current State: {current_state}, Action: {action}")
    

        valid_transitions = {
            "GrGr": "yryr",
            "yryr": "rGrG",
            "rGrG": "ryry",
            "ryry": "GrGr"}
        # Get the expected next state
        expected_next_state = valid_transitions.get(current_state)

        if action == expected_next_state:
            # Transition to the expected state
            traci.trafficlight.setRedYellowGreenState(self.tl_id, action)
            print(f"Transitioned to: {action}")
        else:
            # Skip invalid transitions and log
            print(f"Invalid action: {action}. Expected: {expected_next_state}. Keeping current state.")

        # Step the simulation
        traci.simulationStep()

        # Return the new state
        return self.get_state()
    
    def reset(self):
        traci.load(["-n", "intersection.net.xml", "-r", "intersection.rou.xml", "--start"])
        self.reward = 0
        self.wait_traffic_flow_bot = 0
        self.wait_traffic_flow_bot_left = 0
        self.wait_traffic_flow_top_right = 0
        return self.get_state()