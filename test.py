import traci
from env import Enviornment
from agent import Qagent
import numpy as np

traci.start(["venv/bin/sumo-gui", "-n", "intersection.net.xml","-r", "intersection.rou.xml", "--start", "--delay", "1"])  # Use sumo-gui for GUI mode

# Load Q-table from the saved file (use the appropriate loading method)
q_table = np.load('q_table.npy', allow_pickle=True).item()
print("Q-table loaded from q_table.npy")

# Set up the environment and agent
env = Enviornment("clusterJ4_J6_J7") 
state = env.get_state()
agent = Qagent(4)
agent.state = state
agent.q_table = q_table

step = 0
total_reward = 0
while step < 15000:  # Set an appropriate number of test steps
    print(f"Testing step {step}")
    traci.simulationStep()
    # Choose the action based on the learned Q-table
    action = agent.test(state)
    new_state = env.perform_action(action)
    reward = env.get_reward(new_state, state)
    total_reward += reward
    state = new_state
    step += 1

print(f"Total accumulated reward during testing: {total_reward}")
traci.close()
