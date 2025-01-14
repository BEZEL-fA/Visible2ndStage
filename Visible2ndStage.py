import pygame
from pygame.locals import *

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

print("axis number :")
axis_number = input()
axis_number = int(axis_number)

try:
    while True:
        for event in pygame.event.get():
            if event.type == JOYAXISMOTION:
                if event.axis == axis_number:
                    sensitivity = (event.value +1.0) / 2.0 * 255
                    print(f"R2 sensitivity: {int(sensitivity)}")

except KeyboardInterrupt:
    print("Exiting...")
    pygame.quit()