#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time
import atexit
#Imports
import pygame, sys
#import _thread
from threading import Thread
import RPi.GPIO as GPIO
import curses

#Constants
WIDTH, HEIGHT = 400, 400
TITLE = "Gantry Controller"

#pygame initialization
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# create a default object, no changes to I2C address or frequency
#17(platfomright),22(bottomright),23(topright),27(plaformleft)switches

#x=1335 y=1051
mh = Adafruit_MotorHAT()
# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    
def motorHomeBase():
    myStepper = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1
    myStepper.setSpeed(1000)             # 30 RPM
    myStepper2 = mh.getStepper(200, 2)  # 200 steps/rev, motor port #1
    myStepper2.setSpeed(1000)             # 30 RPM
    i=GPIO.input(27)
    j=GPIO.input(23)
    counterx=0
    countery=0
    while(i==1):
        i=GPIO.input(27)
        counterx+=1
        myStepper.step(1,Adafruit_MotorHAT.BACKWARD ,  Adafruit_MotorHAT.DOUBLE)
        myStepper2.step(1,Adafruit_MotorHAT.BACKWARD ,  Adafruit_MotorHAT.DOUBLE)
    while(j==1):
        j=GPIO.input(23)
        countery+=1
        myStepper.step(1,Adafruit_MotorHAT.FORWARD ,  Adafruit_MotorHAT.DOUBLE)
        myStepper2.step(1,Adafruit_MotorHAT.BACKWARD ,  Adafruit_MotorHAT.DOUBLE)
    #turnOffMotors()
    print(counterx,countery)
        
def motorRun(motorNum,direction,steps):
    if(direction.lower()=='forward'):
        movement=Adafruit_MotorHAT.FORWARD
    else:
        movement=Adafruit_MotorHAT.BACKWARD
    myStepper = mh.getStepper(200, motorNum)  # 200 steps/rev, motor port #1
    myStepper.setSpeed(40000)             # 30 RPM
    myStepper.step(steps,movement ,  Adafruit_MotorHAT.DOUBLE)
def goToXY(steps,direction):
    if(direction=="down"):
        stepper1="backward"
        stepper2="forward"
    elif(direction=="up"):
        stepper1="forward"
        stepper2="backward"
    elif(direction=="right"):
        stepper1="forward"
        stepper2="forward"
    else:
        stepper1="backward"
        stepper2="backward"
    t1=Thread(target=motorRun, args=(1,stepper1,steps,))
    t2=Thread(target=motorRun, args=(2,stepper2,steps,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    #_thread.start_new_thread(motorRun,(1,stepper1,steps,))
    #_thread.start_new_thread(motorRun,(2,stepper2,steps,))
    #_thread.join()

# push button
def pushButton():
    print("push")
atexit.register(turnOffMotors)


#Player Class
class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, 150, 150)
        self.color = (250, 120, 60)
        self.color_click = (200, 200, 200)
        self.velX = 0
        self.velY = 0
        self.space_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    
    def update(self):
        self.velX = 0
        self.velY = 0

        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
            goToXY(10,"left")
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
            goToXY(10,"right")
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
            goToXY(10,"up")
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
            goToXY(10,"down")
        if self.space_pressed:
            pushButton()
            win.fill((12, 24, 36))
            pygame.draw.rect(win, self.color_click, self.rect)
        if self.x <= 230 and self.x >= 20 and self.y<= 230 and self.y >= 20:
            
            self.x += self.velX
            self.y += self.velY
        if not self.left_pressed and not self.right_pressed and not self.up_pressed and not self.down_pressed and not self.space_pressed:
            self.x = 125 
            self.y = 125 
        self.rect = pygame.Rect(int(self.x), int(self.y), 150, 150)

#Player Initialization
player = Player(WIDTH/2, HEIGHT/2)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP) #Reed
    GPIO.setup(22,GPIO.IN, pull_up_down=GPIO.PUD_UP) #Reed
    GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP) #Reed
    GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_UP) #Reed

    # motorHomeBase()
    # _thread.start_new_thread(motorRun,(1,'forward',500,))
    # _thread.start_new_thread(motorRun,(2,'forward',500,))
    # _thread.start_new_thread(motorRun,(1,'forward',500,))
    # _thread.start_new_thread(motorRun,(2,'forwar',500,))
    # goToXY(1000,"right")
    # goToXY(1000,"down")
    # time.sleep(10000)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.left_pressed = True
                if event.key == pygame.K_RIGHT:
                    player.right_pressed = True
                if event.key == pygame.K_UP:
                    player.up_pressed = True
                if event.key == pygame.K_DOWN:
                    player.down_pressed = True
                if event.key == pygame.K_SPACE:
                    player.space_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.left_pressed = False
                if event.key == pygame.K_RIGHT:
                    player.right_pressed = False
                if event.key == pygame.K_UP:
                    player.up_pressed = False
                if event.key == pygame.K_DOWN:
                    player.down_pressed = False
                if event.key == pygame.K_SPACE:
                    player.space_pressed = False
            
        #Draw
        win.fill((12, 24, 36))  
        player.draw(win)

        #update
        player.update()
        pygame.display.flip()

        clock.tick(120)
        GPIO.cleanup()

main()
