import numpy as np

class Qagent:
    def __init__(self,  env, initial_state, phases):
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.q_table = {initial_state: np.zeros(phases)}  # Initialize Q-table as a dictionary        
        self.phases = phases
        self.acc_reward = 0

    def create_action_space(self):
        self.action_space = list(range(self.phases))  # Action space is a list of indices [0, 1, 2, ...]

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            self.action = np.random.choice(self.action_space)
        else:
            self.action = np.argmax(self.q_table[state])
        return self.action

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


