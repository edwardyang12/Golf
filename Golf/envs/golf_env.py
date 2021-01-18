import gym
from gym import spaces
import math
import random
import numpy as np
from Golf.envs.visualizer import Viewer

# 2D golf where objective is for player to put the ball into the hole
# farthest can launch ball is shorter than distance to hole
# Wind changes per hit
# hilly terrain so height changes
# Different clubs with different amounts of "power" and different preset angles
# intuition is that with these different angles, wind will affect them by different amounts
# Input: which club to use and how far to launch
# Outputs: distance to hole, current height, wind


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
        self.clubs = {0:10,1:27,2:42,3:60}
        self.reached = 5 # within 5 meters means u got it
        self.steps = 10 # only get 10 golf swings
        self.dist = 1250
        self.target_height = self.func(1250)

        self.action_space = spaces.Box(low=np.array([-25,0]),high=np.array([50,3]))
        high = np.array([self.dist+200,230,5])
        low = np.array([0,-185,-5])

        self.observation_space = spaces.Box(
            low = low,
            high = high,
            dtype=np.float32
        )

        self.viewer = None

        self.reset()

    def step(self,action):
        
        club = int(round(action[1]))
        velocity = action[0]

        self.vel_list.append(velocity)
        self.club_list.append(club)
        self.wind_list.append(self.wind)

        angle = self.clubs[club]
        distance,height = self.calcLocation(velocity, angle)

        self.height = height
        self.curr = distance
        self.path.append(self.curr)

        #distance = math.sqrt((self.dist-self.curr)**2 + (self.height-self.target_height)**2)
        distance = abs(self.dist-self.curr)
        if distance < self.reached:
            return self._get_obs(), 1, True, {}
        else:
            self.runtime +=1

            # exceeded max steps
            if self.runtime>=self.steps:
                return self._get_obs(), -1, True, {}

            # exceeded bounds
            elif self.curr>self.dist+200:
                
                output = np.array([self.dist+200,0,self.wind])
                return output, -1, True, {}
            
            elif self.curr<0:
                output = np.array([0,0,self.wind])
                return output, -1, True, {}

            obs = self._get_obs()
            self.wind = random.uniform(-5, 5)
            penalty = 0.95 # 0.95 is good
            # 1255 is max euclidian distance
            return obs, (1-distance/self.dist)-penalty, False, {}

    def _get_obs(self):
        # temp = np.array([self.dist-self.curr,self.target_height-self.height,self.wind])
        temp = np.array([self.curr,self.height,self.wind])
        return temp

    def wind_effect(self, wind, vertical_dist):
        if(vertical_dist>100):
            return wind* 2.5
        elif(vertical_dist>75):
            return wind*2
        elif(vertical_dist>50):
            return wind*1.5
        elif(vertical_dist>25):
            return wind*1
        elif(vertical_dist>0):
            return wind*0.5
        else:
            return 0    

    def func(self,x):
        #return (0.8*x-175)*(x-400)*(x+300)*(x-1400)*(x-1210)*(x+400)*(x-800)*(x-1100)*x/(10**22)+50
        return 0

    def calcLocation(self, velocity, angle):

        horizontal_vel = velocity * math.cos(angle * math.pi / 180)
        vertical_vel = velocity * math.sin(angle * math.pi / 180)
        horizontal_dist = self.curr
        vertical_dist = self.height

        while((vertical_dist-self.func(horizontal_dist))>=0 or (vertical_vel>0)):
            
            wind = self.wind_effect(self.wind * time, vertical_dist)
            horizontal_dist = horizontal_vel * time + horizontal_dist
            vertical_dist = vertical_vel * time + vertical_dist
            vertical_vel = vertical_vel + gravity * time
            if((horizontal_vel>0 and wind>0) or (horizontal_vel<0 and wind<0) ):
                if(abs(horizontal_vel)<abs((wind)/time)):
                    horizontal_vel = horizontal_vel + wind
            else:
                horizontal_vel = horizontal_vel + wind

        horizontal_dist, vertical_dist = (horizontal_dist, self.func(horizontal_dist))
        return horizontal_dist,vertical_dist

    def reset(self):
        self.wind = random.uniform(-5, 5)
        self.runtime = 0
        self.curr = 0
        self.height = 0
        self.path = []
        self.vel_list = []
        self.club_list = []
        self.wind_list = []
        self.close()
        return self._get_obs()

    def close(self):
        if self.viewer:
            self.viewer.clear()
            self.viewer = None

    def render(self, mode='human', close=False):
        if not close:
            if self.viewer is None:
                self.viewer = Viewer(self.dist)
            self.viewer.sim(self.vel_list, self.club_list, self.wind_list)

if __name__ == "__main__":
    env = GolfEnv()
    print(env._get_obs())
    for i in range(20):
        obs,reward, bool, _ = env.step([70,1])
        if(bool and reward ==-1):
            print("backwards or exceeded")
            print(obs, reward)
            break
        elif(bool and reward==1):
            print("success")
            print(obs,reward)
            break
    print(env.path)
