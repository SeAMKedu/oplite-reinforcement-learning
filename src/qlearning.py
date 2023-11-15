import gymnasium as gym
import numpy as np

import config


class QLearning:
    """
    Q-learning with the gymnasium's Frozen Lake environment.

    Usage example:
    >>> qlearn = QLearning(mapdata="SFFFFHHFFHFFFFFG", mapsize=4)
    >>> qlearn.find_actions()

    To see more information about the Q-learning, please visit:
    https://en.wikipedia.org/wiki/Q-learning.
    
    Frozen Lake documentation:
    https://gymnasium.farama.org/environments/toy_text/frozen_lake/.

    :param str mapdata: String that contains letters S (start), F (frozen),
        H (hole), and G (goal).

    """
    def __init__(self, desc: str) -> None:
        # Actions defined in the FrozenLake environment.
        self.action_left = config.get("environment.action_left")
        self.action_down = config.get("environment.action_down")
        self.action_right = config.get("environment.action_right")
        self.action_up = config.get("environment.action_up")

        self.max_episodes = config.get("qlearning.max_episodes")
        self.max_steps = config.get("qlearning.max_steps")

        # Actions of the route from start point to end point.
        self.actions = []
        self.actions_found = True

        # Convert the map data into a format used by the Frozen Lake env,
        # e.g. "SFFFFHHFFHFFFFFG" -> ["SFFF", "FHHF", "FHFF", "FFFG"].
        self.size = int(np.sqrt(len(desc)))
        self.desc = [desc[i:i+self.size] for i in range(0, len(desc), self.size)]

        # Q-table keeps track of the reward of each action on each state.
        self.state_count = len(desc)
        self.action_count = 4
        self.alpha = config.get("qlearning.learning_rate")
        self.gamma = config.get("qlearning.discount_factor")
        self.Q = np.zeros((self.state_count, self.action_count))


    def _get_actions(self):
        """Get the actions."""
        # The most rewarding action on each state.
        actions = []
        for state in range(self.state_count):
            most_rewarding_action = np.argmax(self.Q[state])
            actions.append(most_rewarding_action)
        
        # Convert list to matrix.
        actions = np.reshape(actions, newshape=(self.size, self.size))
        print("\nThe most rewarding actions:")
        print(actions)

        row = 0
        col = 0
        for i in range(self.state_count):
            try:
                action = actions[row,col]
            except IndexError:
                self.actions_found = False
                print("Could not find actions...")
                break
            self.actions.append(action)
            if action == self.action_left:
                col -= 1
            elif action == self.action_down:
                row += 1
            elif action == self.action_right:
                col += 1
            elif action == self.action_up:
                row -= 1
            # The goal is reached.
            if row == self.size - 1 and col == self.size - 1:
                break

        print(f"\nActions to goal: {self.actions}")


    def _print_map(self):
        """Print the map data."""
        print("\nCustom map:")
        for row in self.desc:
            chars = ""
            for i in range(len(row)):
                chars = chars + row[i] + " "
            print(chars)


    def _update_q_table(self):
        """
        Use Q-learning to find a route from start point to end point.
        
        The Q-table is updated by using the formula below

        Q(s,a) = (1 - alpha) * Q(s,a) + alpha * (reward + gamma * max(Q(s,a))),
        
        where s is state, a is action, alpha is learning rate, and
        gamma is discount factor.

        """
        # Create an environment.
        env = gym.make(id="FrozenLake-v1", desc=self.desc, is_slippery=False)

        for episode in range(self.max_episodes):
            state, info = env.reset()
            for step in range(self.max_steps):
                # Pick a random action.
                action = env.action_space.sample()
                # Run one time step.
                newstate, reward, terminated, truncated, info = env.step(action)
                # Current value weighted by one minus the learning rate.
                factor1 = (1 - self.alpha) * self.Q[state, action]
                # Reward weighted by the learning rate.
                factor2 = self.alpha * reward
                # Maximum reward weighted by learning rate and discount factor.
                factor3 = self.alpha * self.gamma * np.max(self.Q[newstate, :])
                # Update Q-table.
                self.Q[state, action] = factor1 + factor2 + factor3
                # Update state.
                state = newstate
                # The goal or hole was reached.
                if terminated:
                    break


    def find_actions(self) -> list:
        """
        Use Q-learning to find a series of actions that lead the AGV
        from start to goal by avoiding the obstacles on the map area.

        :returns: Actions from start to goal.
        :rtype: list.

        """
        self._print_map()
        self._update_q_table()
        self._get_actions()
        return self.actions
