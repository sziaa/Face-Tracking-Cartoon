#import for Capturing video using OpenCV
import cv2

#import for creating directory structure
import os

# import for math functions
from math import sin, cos, radians

#import for providing C compatible data type
import ctypes

#import for time access and conversions
import time

#Python modules designed for writing video games
import pygame

#Define a Function to position an image on display
def pos(gameDisplay, ge,x,y):
    gameDisplay.blit(ge,(x,y))

#Define a function to display the attacking image once proxmimty increases
def attack(gameDisplay, kb):
    x = (scl - ix)/2
    y = scb - iy
    gameDisplay.blit(kb, (x,y))
    pygame.display.update()

#Define a function for positioning the eyes on the display screen
def eyeloc(gameDisplay, eye, ex, ey):
    gameDisplay.blit(eye, (ex, ey))

#Define a function for moving the eyes to look around  on the display screen
def move_eyes(gameDisplay, xcord, ycord,):
    w = scl
    h = scb
    x = (w - ix)/2
    y = h - iy
    ex = (w - ix)/2
    ey = h - iy
    nx = ex + xcord / 20 - 10
    ny = ey + ycord / 20 - 10
    gameDisplay.blit(eye, (nx, ny))
    gameDisplay.blit(ge, (x,y))

    #Code to redraw images
    pygame.display.update()

#Define a function to set up intial display
def show_aang_image(w,h):
    w = scl
    h = scb
    os.environ['SDL_VIDEO_WINDOW_POS']="0,0"
    gameDisplay = pygame.display.set_mode((w,h))
    print(gameDisplay)
    pygame.display.set_caption("AANG ATTACK")

    x = (w - ix)/2
    y = h-iy
    ex = (w - ix)/2
    ey = h - iy
    gameDisplay.fill(black)

    pygame.display.update()
    return gameDisplay

#define a function to rotate a image
def rotate_image(image, angle):
    if angle == 0: 
        return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2,height/2),angle,0.9)
    result = cv2.warpAffine(image, rot_mat,(width, height), flags = cv2.INTER_LINEAR)
    return result

#define a function to rotate a point around an image
def rotate_point(pos, img, angle):
    if angle == 0: 
        return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle))+y*sin(radians(angle))+img.shape[1]*0.4
    newy = -x* sin(radians(angle)) + y * cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

###### Main Function ######

if __name__ == '__main__':

    #initalize the pygame libary
    pygame.init()

    #define colour black in RGB
    black = (200,200,200)

    #define image dimensions
    ix = 1800
    iy = 800

    #load in images
    ge = pygame.image.load('aang_happy.PNG')
    eye = pygame.image.load('aang_eyes_exp.PNG')
    kb = pygame.image.load('aang_attack_1.PNG')

    #set screen metrics (width and height)
    scl, scb = 1400,750

    print("Width: ", scl, "Height: ", scb)

    camera = cv2. VideoCapture(0)

    #Set Camera Dimensions:
    w = camera.set(3, scl/2)
    h = camera.set(4, scb/2)

    #Load the face detection cascade classifier
    face = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

    #get camera frame per second
    fps = camera.get(cv2.CAP_PROP_FPS)
    print("fps: ", fps)

    #define face detection settings
    settings = {'scaleFactor': 1.3, 'minNeighbors': 3, 'minSize': (50,50),}

    #set up game display
    gameDisplay = show_aang_image(scl, scb)
                
    running = True
    while running:
        event = pygame.event.get()
        if (event is not None):
            pressed = pygame.key.get_pressed()
            if (pressed[pygame.K_q]):
                running = False
        ret, imgn = camera.read()
        img = cv2.flip(imgn, +1)

        for angle in [0, -25, 25]:
            rimg = rotate_image(img, angle)
            detected = face.detectMultiScale(rimg,**settings)
            if len(detected):
                detected = [rotate_point(detected[-1],img,-angle)]
                break

        for x, y, w, h in detected[-1:]:
            cv2.rectangle(img, (x,y), (x+w, y+h), (200,0,0),2)
            xcord = (x+w)/2
            ycord = 2 * (y + h) / 3
            if x + w > 500 and y + h > 500:
                #print("too close")
                attack(gameDisplay, kb)
            else:
                move_eyes(gameDisplay, xcord, ycord)

        if cv2.waitKey(5) != -1:
            break

    cv2.destroyAllWindows()
    pygame.quit()
    quit()
