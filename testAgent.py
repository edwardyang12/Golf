# test agent
import random
import gym
import Golf
from agent import Agent

env = gym.make('Golf-v0')
urAgent = Agent()
total_reward = 0
episodes = 5

for i in range(episodes):
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
            env.render()
            env.close()
            print("Episode finished after {} timesteps".format(t+1))
            break
    total_reward += episode_reward

print("Simulation finished with reward: {} ".format(total_reward/episodes))

    
