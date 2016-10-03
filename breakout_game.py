# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 21:40:02 2015

@author: Mateja Sela and Veronica Estudillo Velasco

"""
person = input('Please enter your name: ' ) #input your name
paddlecolor = input('What is your favorite color, red green or blue: ') #imput of paddle color
while 'red' !=paddlecolor and 'blue' !=paddlecolor and 'green' != paddlecolor: # loop until the wanted outcome is reached
    paddlecolor = input('What is your favorite color, red green or blue: ')
from pyprocessing import *
counter = 0
WIDTH = 600
HEIGHT = 500
class Ball:
    """
    This class creates a simple ball that bounces around the screen
    """
    def __init__(self, x,y,radius,color):
        """
        Initialize the ball.
        
        The properties x,y, radius, and color are all parameters, while the velocity is 8 and -8 
        for x and y respectively
        
        x - initial x position
        y - initial y position
        radius - radius of the ball
        color - color as specified as a tuple of RGBA value (RGB plus alpha) with all values between 0-255
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = 8
        self.vy = -8
        
        
    def draw(self):
        """
        Draw the circle.
        """
        ellipseMode(CENTER)
        fill(self.color[0], self.color[1], self.color[2])
        ellipse(self.x, self.y, self.radius*2,self.radius*2)
        
        # conditional that stops the simulation once the ball has disappeared offscreen.    
        if self.y >= HEIGHT :
            textSize(40)
            text("You Lost", 200, 250)
            cursor()
            noLoop()
        else:
            noCursor()
            
            

    def update(self, obstacles):
        """
        Move the ball by the amounts in vx and vy.
        
        This also does basic checking to see if it is going to collide with a wall. If it does,
        the velocity component in that direction is flipped to create a perfect bounce.
        """
        self.x += self.vx
        self.y += self.vy
        
        # bounce off of the left or right wall
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.vx = -self.vx
        
        # bounce off of the ceiling 
        if self.y - self.radius <= 0:
            self.vy = -self.vy 
        
        # Deflect when you hit an object. 
        bounces = []    
        for item in obstacles: 
            bounces.extend(item.bounce(self))
        if 'l' in bounces or 'r' in bounces:
            self.vx = -self.vx
        if 't' in bounces or 'b' in bounces:
            self.vy = -self.vy
# The Paddle 

class Paddle: 
    """
    This class creates a simple paddle that moves horizontially at the bottom of the screen
    """
    def __init__(self, width,height,color):
        """
        Initialize the paddle.
        The properties width, height and color are all parameters
        x - x position
        y - y position
        width - initial width
        height - initial height
        color - color as specified as a tuple of RGBA value (RGB plus alpha) with all values between 0-255
        """
        self.width = width
        self.height = height
        self.x = WIDTH//2
        self.y = HEIGHT - self.height
        self.color = color
    
    def draw(self):
        """
        Draw a paddle
        """
        fill(self.color[0], self.color[1], self.color[2])
        rect(self.x,self.y, self.width,self.height)

    def update(self):
        """
        Move the paddle by the mouse movement. Make the paddle not go off the screen.
        """
        self.x = mouse.x
        
            
    def bounce(self, ball):
        """
        This function will detect when the ball has collided with the paddle.
        The 1st condition to check for if the ball is in the same “column” as the paddle.
        The 2nd condition to check  if the lower edge of the ball is at/has passed the top of the paddle.
        """
        # Conditional
        if ball.x + ball.radius >= self.x and ball.x - ball.radius <= self.x + self.width:       
            if ball.y-ball.vy + ball.radius <= self.y and ball.y + ball.radius >= self.y:
                return ['t']
        return []

class Brick:
    def __init__(self, x, y, width, height, color):
        
        """
        Initialize the Brick.
        
        The properties width, height and color are all parameters
        x - initial x position
        y - initial y position
        width - initial width
        height - initial height
        color - color as specified as a tuple of RGBA value (RGB plus alpha) with all values between 0-255
        """
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.visible = True
 
    def draw(self):
        """
        Draw a brick if visible
        """
        if self.visible == True:
            fill(self.color[0], self.color[1], self.color[2])
            rect(self.x,self.y, self.width,self.height)
     
    def bounce(self, ball):
        global counter
        bounces = [] 
        if self.visible == True:
            # top
            if ball.x + ball.radius >= self.x and ball.x - ball.radius <= self.x + self.width: 
                if ball.y - ball.vy + ball.radius <= self.y and ball.y + ball.radius >= self.y:
                    bounces.append('t')
 
            # bottom
            if ball.x + ball.radius >= self.x and ball.x - ball.radius <= self.x + self.width:
                if ball.y - ball.vy - ball.radius >= self.y + self.height and ball.y - ball.radius <= self.y + self.height: 
                    bounces.append('b')

            # Right
            if ball.y - ball.radius >= self.y and ball.y - ball.radius <= self.y + self.height :
                if ball.x - ball.radius <= self.x + self.width and ball.x - ball.radius - ball.vx >= self.x + self.width : 
                    bounces.append('r')

            # Left         
            if ball.y - ball.radius >= self.y and ball.y - ball.radius <= self.y + self.height :
                if ball.x + ball.radius >= self.x and ball.x + ball.radius - ball.vx <= self.x: 
                    bounces.append('l')
            if bounces != []:
                self.visible = False
                textSize(32)
                fill(10, 150, 200,200)
                text("Ouch", 300, 350)
                counter +=1
        return bounces

ball = Ball(WIDTH//2, HEIGHT - 50, 10, (20,100,100))
obstacles = []
if paddlecolor == 'red':
    paddle = Paddle(200,25, (200,100,100))
if paddlecolor == 'green':
    paddle = Paddle(200,25, (100,200,100))
if paddlecolor == 'blue':
    paddle = Paddle(200,25, (100,100,200))
obstacles.append(paddle)

def setup():
    """
    Set the brick size, position, etc.
    """
    size(WIDTH, HEIGHT) # set the size of the window
    # create a bunch of bricks to create a wall. 
    for k in range(0,12,2):
        for i in range(15):
            brick = Brick((40*i),(20*k+40),40, 20, (i*10,12*k,i*5+100))
            obstacles.append(brick)
    
def draw():
    """
    This is another special function known to pyProcessing. It will call this function repeatedly, allowing us to use it for animation.
    """
    global person
    background(255,255,255)
    
    paddle.update()            
    for item in obstacles:
        item.draw()
          
    # update and then draw each ball in the list
    ball.update(obstacles)
    ball.draw()
   
    textSize(32)
    fill(0, 102, 153)
    text('Player: '+person, 10, 30) # keep the score somehow
    
    textSize(32)
    fill(20, 102, 153)
    text("Score "+str(counter), 10, 72)
# start pyprocessing   
run()
   