import pygame 
import time
from buildhat import *

pygame.init()                                   #pygame initialize
pygame.display.set_caption("Keyboard Control")  #window name
screen = pygame.display.set_mode((200,200))     #window size
screen.fill((0, 0, 0))                          #fill the screen with black

#set motors
lm = Motor('A')
rm = Motor('B')
lm.off()
rm.off()

def drive(speedl,speedr):
    lm.pwm(speedl*(-0.01))
    rm.pwm(speedr*(0.01))

def stop():
    rm.stop()
    lm.stop()

def motor_control(key):                         #key값에 따라 모터 동작
    if key == 'No Input':
        stop()
    if key == 'f':
        drive(22,20)
    if key == 'r':
        drive(25,0)
    if key == 'b':
        drive(-20,-20)
    if key == 'l':
        drive(0,25)

try:
    exit=False
    while not exit:
        for event in pygame.event.get():        #key값 받기
            pressed = pygame.key.get_pressed()  #눌린 key
            key="s"
            if pressed[pygame.K_q]:
                exit = True
            if pressed[pygame.K_UP]:
                key="f"
            elif pressed[pygame.K_DOWN]:
                key="b"
            elif pressed[pygame.K_LEFT]:
                key="l"
            elif pressed[pygame.K_RIGHT]:
                key="r"
        motor_control(key)
        time.sleep(0.1)
finally:
    print("Control End")

