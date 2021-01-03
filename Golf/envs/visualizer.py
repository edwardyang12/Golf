import gym
import turtle
import math
import cv2

def resizer(image, dimensions):
    src = cv2.imread(image)
    output = cv2.resize(src, dimensions)
    cv2.imwrite(image,output)


class Viewer:
    def __init__(self, target, traps, horizontal_dist = -1000, time = 0.01):
        turtle.screensize(2500, 500, 'white')
        self.screen = turtle.Screen()
        self.theTurtle = turtle.Turtle()
        self.initial = (horizontal_dist, 0)
        self.gravity = -9.81
        self.time = time
        self.clubs = {0:10,1:27,2:42,3:60}
        self.curr = self.initial
        self.target = target
        self.trap = traps
        self.drawBg(target, traps)

    def drawBg(self, target, traps, ball = 'ball.gif', bg = 'bg.png'):
        self.screen.bgpic('bg.png')
        self.screen.update()
        self.screen.addshape("ball.gif")
        self.theTurtle.shape("ball.gif")
        self.theTurtle.penup()
        self.theTurtle.setpos(self.initial)
        self.theTurtle.pendown()
        targetTurtle = turtle.Turtle()
        self.screen.addshape("flag.gif")
        targetTurtle.penup()
        targetTurtle.shape("flag.gif")


        start = True
        before = self.initial[0]
        for i in range(1,len(traps)):
            temp = traps[i] - 1000
            if start:
                start = False
                targetTurtle.penup()
                targetTurtle.setpos(temp,-25)
                targetTurtle.pendown()
            else:
                start = True
                targetTurtle.fillcolor("blue")
                targetTurtle.begin_fill()
                for z in [temp-before,100,temp-before,100]:
                    targetTurtle.forward(z)
                    targetTurtle.right(90)
                targetTurtle.end_fill()
                targetTurtle.penup()
            before = traps[i] - 1000
        targetTurtle.penup()
        targetTurtle.setpos((target-1000,25))


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
        print(horizontal_dist)

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
    velocity = [70,70,50]
    club = [2,1,2]
    wind = [-5,-5,-5]

    viewer = Viewer(1500,[0,500,750,1000,1250,1500])

    viewer.sim(velocity, club, wind)
    viewer.freeze_screen()
