import gym
import turtle
import math
import cv2

def resizer(image, dimensions):
    src = cv2.imread(image)
    output = cv2.resize(src, dimensions)
    cv2.imwrite(image,output)


class Viewer:
    def __init__(self, horizontal_dist = -1000, time = 0.01):
        turtle.screensize(2500, 500, 'white')
        self.screen = turtle.Screen()
        self.screen.bgpic('bg.png')
        self.screen.update()
        self.screen.addshape("ball.gif")
        self.theTurtle = turtle.Turtle()
        self.theTurtle.shape("ball.gif")
        self.theTurtle.penup()
        self.theTurtle.setpos(horizontal_dist,0)
        self.theTurtle.pendown()
        self.initial = (horizontal_dist, 0)
        self.gravity = -9.81
        self.time = time
        self.clubs = {0:10,1:27,2:42,3:60}
        self.curr = self.initial


    def sim(self, vel_list, club_list, wind_list):
        for i in range(len(vel_list)):
            self.move(vel_list[i],self.clubs[club_list[i]], wind_list[i])
        self.end_episode()
        
    # simulates one arrow shot
    def move(self, velocity, angle, wind):
        wind = wind * self.time
        horizontal_vel = velocity * math.cos(angle * math.pi / 180)
        vertical_vel = velocity * math.sin(angle * math.pi / 180)
        horizontal_dist = self.curr[0]
        vertical_dist = self.curr[1]
        while((vertical_dist>=0) or (vertical_vel>0)):
            
            self.theTurtle.setpos(horizontal_dist,vertical_dist)
            horizontal_dist = horizontal_vel * self.time + horizontal_dist
            vertical_dist = vertical_vel * self.time + vertical_dist
            vertical_vel = vertical_vel + self.gravity * self.time
            horizontal_vel = horizontal_vel + wind
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
    velocity = [70,20,50]
    club = [1,0,2]
    wind = [-3,2,5]

    viewer = Viewer()
   
    viewer.sim(velocity, club, wind)
    viewer.freeze_screen()
