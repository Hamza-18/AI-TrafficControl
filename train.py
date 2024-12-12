import os
os.environ["SUMO_HOME"] = "venv/bin/lib/sumo"  # Update this path
os.environ["PYTHONPATH"] = f"{os.environ['SUMO_HOME']}/tools"
import traci
from env import Enviornment
from agent import Qagent
import numpy as np

traci.start(["venv/bin/sumo", "-n", "intersection.net.xml","-r", "intersection.rou.xml", "--start"])  # Use sumo-gui for GUI mode
step = 0
agent = Qagent(4)
min_episolon = 0.05
max_episolon = 1
env = Enviornment("clusterJ4_J6_J7")
decay_rate = 0.0005

for i in range(2):
    agent.epsilon = min_episolon + (max_episolon - min_episolon) * np.exp(-decay_rate * i)
    step = 0
    while step < 15000:
        print(f"step {step}")
        traci.simulationStep()
        state = env.get_state()
        agent.set_initial_state(state)
        action = agent.choose_action(state)
        new_state = env.perform_action(action)  
        agent.learn(new_state, env.get_reward(new_state, state))
        step +=1
    env.reset()
    print(f"Episode {i} completed.")
agent.save_q_table()