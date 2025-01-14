#Now it can show R2 trigger sensitivity per 60fps

import pygame
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()

if joystick_count == 0:
    print("No controller attached")
else:
    for i in range (joystick_count):
        joystick = pygame.joystick.Joystick(i)
        print(f"Controller {i}: {joystick.get_name()}")
    print("Select joystick number :")
    
    number = input()
    number = int(number)
    joystick = pygame.joystick.Joystick(number)
    joystick.init()
    print(f"Controller attached: {joystick.get_name()}")
    
axis_count = joystick.get_numaxes()
print(f"Number of axis: {axis_count}")

#Select axis signal
print("axis number :")
axis_number = input()
axis_number = int(axis_number)

sens = 0
t = 0 #Hold timer 60flame
flag = 0 #Hold flag

try:
    while True:
        for event in pygame.event.get():
            if event.type == JOYAXISMOTION:
                if event.axis == axis_number:
                    sens = (event.value +1.0) / 2.0 * 255
                    sens = int(sens)
        #print(f"R2 sensitivity: {sens}") 
        if sens < 141:
            t = 0 #reset t
            flag = 0
        elif sens > 140 and sens < 220:
            t = t + 1
            print(t)
            flag = 1
        elif sens > 219 and flag == 1:
            if t > 11 and t < 23:
                print("SS Successed")
                flag = 0
            else:
                print("SS failed")
                flag = 0
            t = 0 #reset t
        clock.tick(60)

#ctrl+c option
except KeyboardInterrupt:
    print("Exiting...")
    pygame.quit()