import numpy as np

class Qagent:
    def __init__(self, env, num_states, phases):
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.q_table = np.zeros((self.num_states, self.phases))
        self.num_states = num_states
        self.phases = phases

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(self.phases)
        else:
            action = np.argmax(self.q_table[state])
        return action