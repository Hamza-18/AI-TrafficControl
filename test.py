import traci
from env import Enviornment
from agent import Qagent
import numpy as np

traci.start(["venv/bin/sumo-gui", "-n", "intersection.net.xml","-r", "intersection.rou.xml", "--start", "--delay", "200"])  # Use sumo-gui for GUI mode

# Load Q-table from the saved file (use the appropriate loading method)
q_table = np.load('q_table.npy', allow_pickle=True).item()
print("Q-table loaded from q_table.npy")

# Set up the environment and agent
env = Enviornment("clusterJ4_J6_J7")  # Modify this according to your environment
state = env.get_state()
agent = Qagent(4)
agent.state = state
agent.q_table = q_table  # Load the saved Q-table into the agent

# Run the agent in the environment
step = 0
total_reward = 0

while step < 15000:  # Set an appropriate number of test steps
    print(f"Testing step {step}")
    traci.simulationStep()
    # Choose the action based on the learned Q-table
    action = agent.test(state)
    # Perform the action in the environment
    new_state = env.perform_action(action)
    # Get the reward based on the new state
    reward = env.get_reward(new_state, state)
    # Accumulate reward for evaluation
    total_reward += reward
    # Update the state for the next step
    state = new_state
    step += 1

print(f"Total accumulated reward during testing: {total_reward}")
traci.close()
