#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time
import atexit
#import _thread
from threading import Thread
import RPi.GPIO as GPIO
import curses
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
atexit.register(turnOffMotors)
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
    screen = curses.initscr()
    curses.noecho() 
    curses.cbreak()
    screen.keypad(True)

    try:    
            
            while True:
                
                char = screen.getch()
                if char == ord('q'):
                 
                    break
                elif char == curses.KEY_UP:
                    
                    print("up")
                    goToXY(10,"up")
                    
              
                    
                    
                elif char == curses.KEY_DOWN:
                    
                    goToXY(10,"down")
                    print("down")
                   
                elif char == curses.KEY_RIGHT:
                 
                    print("right")
                    goToXY(10,"right")
                    
                elif char == curses.KEY_LEFT:
                 
                    print("left")
                    goToXY(10,"left")
                  
                elif char == ord('s'):
               
                    print("stop")
                    turnOffMotors()
                curses.flushinp()
                
    finally:
        #Close down curses properly, inc turn echo back on!
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()
        GPIO.cleanup()

main()
