# test agent
import random
import gym
import Golf

env = gym.make('Golf-v0')


class Agent:
    def __init__(self):
        self.network = None
        # idk what you want to initialize
        # not allowed to store position or any data about the agent here
        # can store something like your network or something

    # takes observations as input (position, height, wind)
    # outputs velocity, club number (see golf_env.py for more details)
    def step(self, observations):
        position = observations[0]
        height = observations[1]
        wind = observations[2]

        return [0,0]

urAgent = Agent()
total_reward = 0
for i in range(5):
    episode_reward = 0
    observation = env.reset()
    for t in range(10):

        # agent should determine action based on observation
        action = urAgent.step(observation)
        observation, reward, done, info = env.step(action)
        print("Observations: {} ".format(observation))
        print("Reward: {} ".format(reward))
        print("Action: {} ".format(action))
        
        episode_reward += reward
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
    total_reward += episode_reward

print("Simulation finished with reward: {} ".format(total_reward/5))

    
