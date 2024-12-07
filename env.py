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
        for veh_id in vehicles:
            lane_id = traci.vehicle.getLaneID(veh_id)
            if lane_id == "-E0_0":
                traffic_flow_level1 += 1
            elif lane_id == "-E0.74_0":
                traffic_flow_level2 += 1
            elif lane_id == "gneE0_2":
                traffic_flow_level3 += 1

    def intialise_q_table(self):
        self.q_table = np.zeros((self.num_states, self.phases))

    def state_to_index(phase, traffic_flow_level1, traffic_flow_level2, traffic_flow_level3):
        phase_map = {"GRY": 0, "YEL": 1, "RED": 2}  # Phase to integer mapping
        # Get phase index
        phase_index = phase_map[phase]
        # Calculate state index
        state_index = (phase_index * (3**3) + traffic_flow_level1 * (3**2) + traffic_flow_level2 * 3 + traffic_flow_level3)
        return state_index