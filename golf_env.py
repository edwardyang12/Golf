import gym
from gym import spaces
import math
import random
import numpy as np

# 2D golf where objective is for player to put the ball into the hole
# farthest can launch ball is shorter than distance to hole
# Start and end height constant
# Wind held constant per map
# Different clubs with different amounts of "power" and different preset angles
# intuition is that with these different angles, wind will affect them by different amounts
# Outputs: distance to hole
# Input: which club to use and how far to launch

# next iteration will add these:
# Must avoid traps held constant per map
# map of where ball is (including traps),

'''
driver = 10 -> 0
5- iron = 27 -> 1
9- iron = 42 -> 2
lofting wedge = 60 -> 3
'''

time = 0.01
gravity = -9.81

class GolfEnv(gym.Env):

    def __init__(self):
        super(GolfEnv,self).__init__()

        ''' for golf course initialization stuff '''
        self.max_dist = 2000 # meters of longest track
        self.clubs = {0:10,1:27,2:42,3:60}
        self.min_dist = 400
        self.reached = 5 # within 5 meters means u got it
        self.obstacles = 3 # traps
        self.max_obstacle_size = 100 # size of trap
        self.steps = 10 # only get 10 golf swings

        self.reset()

    def generate_track(self):
        self.dist = random.randint(self.min_dist,self.max_dist)
        size_array = [random.randint(0,self.max_obstacle_size/2) for _ in range(self.obstacles)]
        start = 0
        for size in size_array:
            end = random.randint(start,start+size)
            self.obstacles_array.append([start,end])
            start = 2*end
        self.obstacles_array.append([start,self.dist])

    def step(self,action):
        exceeded = False
        club, velocity = action
        angle = self.clubs[club]
        distance = self.calcLocation(velocity, angle)

        self.curr += distance
        if self.curr > self.dist:
            exceeded = True

        trapped = True
        for tuple in self.obstacles_array:
            if self.curr>tuple[0] and self.curr<tuple[1]:
                trapped = False
                break
        if trapped:
            exceeded = True
        self.runtime +=1

        if self.runtime>self.steps:
            exceeded = True
        if exceeded:
            return self._get_obs(), -1, True, {}

        distance = abs(self.dist-self.curr)
        if distance < self.reached:
            return self._get_obs(), 1, True, {}
        else:
            obs = self._get_obs()
            self.wind = random.randint(-15, 15)
            return obs, distance/self.dist, False, {}

    def _get_obs(self):
        temp = np.array(self.obstacles_array)-self.curr
        temp = np.append(temp,self.wind)
        return temp

    def calcLocation(self, velocity, angle):

        horizontal_vel = velocity * math.cos(angle * math.pi / 180)
        vertical_vel = velocity * math.sin(angle * math.pi / 180)
        horizontal_dist = 0
        vertical_dist = 0

        while((vertical_dist> 0) or (vertical_vel>0)):
            horizontal_dist = horizontal_vel * time + horizontal_dist
            vertical_dist = vertical_vel * time + vertical_dist
            vertical_vel = vertical_vel + gravity * time
            horizontal_vel = horizontal_vel + self.wind

        return horizontal_dist

    def reset(self):
        self.wind = random.randint(-15, 15)
        self.runtime = 0
        self.dist = 0
        self.curr = 0
        self.obstacles_array = []
        self.generate_track()
        return self._get_obs()

if __name__ == "__main__":
    env = GolfEnv()
    for i in range(20):
        env.step([1,10])
