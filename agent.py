import numpy as np

class Qagent:
    def __init__(self, phases, env):
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.q_table = {}  # Initialize Q-table as a dictionary        
        self.phases = phases
        self.acc_reward = 0
        self.env = env
        self.create_action_space()

    def set_initial_state(self, state):
        self.state = state
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.phases)

    def create_action_space(self):
        self.action_space = list(range(self.phases))  # Action space is a list of indices [0, 1, 2, ...]
        self.action_map = {0:"GrGr",1:"yryr",2:"rGrG",3:"ryry"}

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            self.action = np.random.choice(self.action_space)
        else:
            self.action = np.argmax(self.q_table[state])
        print(f"Action: {self.action_map[self.action]}")
        return self.action_map[self.action]

    def learn(self, next_state, reward, done=False):
        """Update Q-table with new experience."""

        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(self.phases)

        s = self.state
        s1 = next_state
        a = self.action
        self.q_table[s][a] = self.q_table[s][a] + self.alpha * (
            reward + self.gamma * max(self.q_table[s1]) - self.q_table[s][a]
        )
        self.state = s1
        self.acc_reward += reward
        print(f"new state: {s1}, old state:{s}")
        print(f"Q(s, a): {self.q_table[s][a]}")
        print(f"Action: {a}, Reward: {reward}, Accumulated Reward: {self.acc_reward}")

    def save_q_table(self):
        np.save("q_table.npy", self.q_table)

    def choose_action_test(self, state):
        # Always choose the action with the highest Q-value (greedy)
        self.action = np.argmax(self.q_table[state])
        print(f"Chosen Action: {self.action_map[self.action]}")
        return self.action_map[self.action]

    def test(self, state):
        # In testing mode, select action greedily based on Q-table
        return self.choose_action_test(state)
