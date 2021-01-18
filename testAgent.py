# test agent
import random
import gym
import Golf
import numpy as np
from agent import Agent

env = gym.make('Golf-v0')
urAgent = Agent('./checkpoints/tester')
total_reward = 0
episodes = 5

for i in range(episodes):
    episode_reward = 0
    observation = env.reset()
    for t in range(10):
        observation = np.array(observation)
        observation = np.expand_dims(observation, axis=0)
        # agent should determine action based on observation
        action = urAgent.step(observation)
        np.clip(action,env.action_space.low,env.action_space.high)
        observation, reward, done, info = env.step(action)
        print("Observations: {} ".format(observation))
        print("Reward: {} ".format(reward))
        print("Action: {} ".format(action))
        
        episode_reward += reward
        if done:
            env.render()
            env.close()
            print("Episode finished after {} timesteps".format(t+1))
            break
    total_reward += episode_reward

print("Simulation finished with reward: {} ".format(total_reward/episodes))

    
