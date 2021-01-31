import gym
import turtle
import math
import cv2

def resizer(image, dimensions):
    src = cv2.imread(image)
    output = cv2.resize(src, dimensions)
    cv2.imwrite(image,output)


class Viewer:
    def __init__(self, target, horizontal_dist = -1000, time = 0.01):
        turtle.screensize(2500, 350, 'white')
        self.screen = turtle.Screen()
        self.theTurtle = turtle.Turtle()
        self.initial = (horizontal_dist, self.func(0))
        self.gravity = -9.81
        self.time = time
        self.clubs = {0:10,1:27,2:42,3:60}
        self.curr = self.initial
        self.target = target
        self.drawBg(target)

    def drawBg(self, target, ball = 'ball.gif', bg = 'bg.png'):
        self.screen.bgpic("Golf/envs/bg.png")
        self.screen.update()
        self.screen.addshape("Golf/envs/ball.gif")
        self.theTurtle.shape("Golf/envs/ball.gif")
        self.theTurtle.penup()
        self.theTurtle.setpos(self.initial)
        self.theTurtle.pendown()
        targetTurtle = turtle.Turtle()
        self.screen.addshape("Golf/envs/flag.gif")
        targetTurtle.penup()
        targetTurtle.shape("Golf/envs/flag.gif")

        temp = -1000
        targetTurtle.setpos(temp,self.func(0))
        targetTurtle.pendown()
        for i in range(target+100):
            targetTurtle.setpos(temp+i,self.func(i))
        targetTurtle.penup()
        targetTurtle.setpos(self.target-1000,self.func(self.target)+65)

    def func(self,x):
        return (0.8*x-175)*(x-400)*(x+300)*(x-1400)*(x-1210)*(x+400)*(x-800)*(x-1100)*x/(10**22.3)+25
        
    def sim(self, vel_list, club_list, wind_list):
        for i in range(len(vel_list)):
            self.move(vel_list[i],self.clubs[club_list[i]], wind_list[i])
        self.end_episode()

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

    # simulates one arrow shot
    def move(self, velocity, angle, wind):
        self.theTurtle.pendown()
        horizontal_vel = velocity * math.cos(angle * math.pi / 180)
        vertical_vel = velocity * math.sin(angle * math.pi / 180)
        horizontal_dist = self.curr[0]
        vertical_dist = self.curr[1]
        while((vertical_dist-self.func(horizontal_dist+1000))>=0):
            temp = self.wind_effect(wind * self.time, vertical_dist)
            self.theTurtle.setpos(horizontal_dist,vertical_dist)
            horizontal_dist = horizontal_vel * self.time + horizontal_dist
            vertical_dist = vertical_vel * self.time + vertical_dist
            vertical_vel = vertical_vel + self.gravity * self.time
            if((horizontal_vel>0 and temp>0) or (horizontal_vel<0 and temp<0) ):
                if(abs(horizontal_vel)<abs((temp)/self.time)):
                    horizontal_vel = horizontal_vel + temp
            else:
                horizontal_vel = horizontal_vel + temp

            if(horizontal_dist<-1000):
                self.theTurtle.penup()
                self.theTurtle.setpos(-1000,0)
                horizontal_dist, vertical_dist = -1000, 0
                break
        self.theTurtle.penup()
        self.theTurtle.setpos(horizontal_dist, self.func(horizontal_dist+1000))
        horizontal_dist, vertical_dist = (horizontal_dist, self.func(horizontal_dist+1000))
        self.curr = (horizontal_dist, vertical_dist)
        
    # freeze turtle screen
    def freeze_screen(self):
        turtle.mainloop()

    # end current iteration
    def end_episode(self):
        self.theTurtle.penup()
        self.theTurtle.setpos(self.initial)
        self.theTurtle.pendown()
        self.curr = self.initial

    def clear(self):
        turtle.clearscreen()

if __name__ == '__main__':

    # resizer('bg.png',(2500, 500))
    # resizer('ball.png',(40, 40))
    velocity = [70,70,70,70]
    club = [3,0,1,3]
    wind = [5,-5,-5,5]

    viewer = Viewer(1250)

    viewer.sim(velocity, club, wind)
    viewer.freeze_screen()
