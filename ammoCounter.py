"""
Created on Sat Mar 10 17:54:13 2018
@author: DrDave
"""
import pygame
import time
import sys
from  ammoCounter_config import *

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.fontHeight = 35
        self.font = pygame.font.Font(None, self.fontHeight)
        size = [1000, 200]
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("IL-2 Ammo Counter")
        self.reset()

    def print_(self, textString):
        #print(textString)
        if type(textString) == str:
            for line in textString.split('\n'):
                if len(line) > 0:
                    self.printLine(line)

    def printLine(self, textString):
        #print(textString, ' len:',  len(textString))
        textBitmap = self.font.render(textString, False, BLACK)
        self.x = 0
        self.screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.screen.fill(WHITE)
        self.x = 10
        self.y = 10
        self.line_height = self.fontHeight


# -------- Main Program Loop -----------
def QUIT():
    pygame.quit()
    sys.exit()

class Plane():
    def __init__(self, planeDef):
        self.name = planeDef['name']
        self.gunDict = {}

        if 'mgName' in planeDef.keys():
            self.mg     = Gun()
            self.mg.setKey( (MG_JOYSTICK,MG_BUTTON) ) #default MG is 0'th joystick button 0
            self.mg.name           = planeDef['mgName']
            self.mg.ammoDuration_s = planeDef['mgDuration']
            self.gunDict[self.mg._key    ] = self.mg
        else:
            self.mg = None

        if 'cannonName' in planeDef.keys():
            self.cannon = Gun()
            self.cannon.setKey( (CANNON_JOYSTICK,CANNON_BUTTON) ) #default Cannon is 0'th joystick button 2 
            self.cannon.name       = planeDef['cannonName']
            self.cannon.ammoDuration_s = planeDef['cannonDuration']
            self.gunDict[self.cannon._key] = self.cannon
        else:
            self.cannon = None

    def print_(self):
        printStr = self.name + '\n'
        for k in self.gunDict.keys():
            printStr += '    ' + self.gunDict[k].print_() + '\n'
        return printStr

    def resetGuns(self):
        for k in self.gunDict.keys():
            self.gunDict[k].reset()

class Gun():
    def __init__(self):
        self.ammoPercentage = 100.0
        self.ammoDuration_s = 30.0
        self.firedDuration_s = 0.0
        self.joystick = 0
        self.button   = 0
        self._key = (self.joystick, self.button)
        self.lastFireTime =    -1.0
        self.lastReleaseTime = -1.0
        self.name = ' '
    def setKey(self, (joystick, button)):
        self.joystick = joystick
        self.button   = button
        self._key = (self.joystick, self.button)
    def ammoDuration_s(self, t_s):
        self.ammoDuration_s = t_s
    def reset(self):
        self.ammoPercentage = 100.0
        self.firedDuration_s = 0.0
        self.lastFireTime =    -1.0
        self.lastReleaseTime = -1.0
    def fire(self):
        self.lastFireTime = time.time()
    def release(self):
        if( self.lastFireTime > 0):
            self.lastReleaseTime =  time.time()
            self.firedDuration_s += (self.lastReleaseTime - self.lastFireTime)
            #print('last fire: ',self.lastFireTime, ' last release: ', self.lastReleaseTime,  'total fire duration: ', self.firedDuration_s)
            self.ammoPercentage = (1.0 - ( self.firedDuration_s / self.ammoDuration_s)) * 100.0
            self.ammoPercentage = max( self.ammoPercentage, 0.0) #crop to zero
        else:
            self.lastFireTime    = -1.0
            self.lastReleaseTime = -1.0
            self.print_()
            print("release before press, ignoring")

    def print_(self):
        printStr =  self.name 
        printStr += 'Joy: ' + str(self._key[0]) + ' Key: ' + str(self._key[1]) + '    '
        printStr += '{:3.3f}'.format(self.firedDuration_s) + ' s   '
        printStr += '{:3.0f}'.format(self.ammoPercentage) + ' %'
        #print(printStr)
        return printStr

###------------------------------------------------------------------###
if __name__=='__main__':
    pygame.init()
    done = False
    clock = pygame.time.Clock()
    # Initialize the joysticks
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

    RESET_KEY = (0,15)
    # Get ready to print
    textPrint = TextPrint()
    #plane = Plane(PLANE_DICT['LAGG3_23'])
    #plane = Plane(PLANE_DICT['YAK1B'])
    #plane = Plane(PLANE_DICT['MIG3-BS700'])
    plane = Plane(PLANE_DICT['YAK7'])
    pygame.event.set_blocked(pygame.JOYAXISMOTION)
    pygame.event.set_blocked(pygame.JOYHATMOTION)
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    while done==False:
        # EVENT PROCESSING STEP
        for event in pygame.event.get(): # User did something
            #print(event)
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
    
            if event.type == pygame.KEYDOWN: #doesn't catch keyboard when Il-2 fullscreen
                if event.key == pygame.K_q:
                    textPrint.print_("Quitting...")
                    QUIT()
                if event.key == pygame.K_m:
                    plane = None
                    plane = Plane(PLANE_DICT['MIG3-BS700'])
                if event.key == pygame.K_b:
                    plane = None
                    plane = Plane(PLANE_DICT['YAK1B'])
                if event.key == pygame.K_y:
                    plane = None
                    plane = Plane(PLANE_DICT['YAK69'])
                if event.key == pygame.K_l:
                    plane = None
                    plane = Plane(PLANE_DICT['LAGG3_23'])
                if event.key == pygame.K_7:
                    plane = None
                    plane = Plane(PLANE_DICT['YAK7'])
                                # Possible joystick actions:
            #JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
    
            if event.type == pygame.JOYBUTTONDOWN or event.type ==  pygame.JOYBUTTONUP:
                k = (event.dict['joy'], event.dict['button'])
                if k in plane.gunDict.keys():
                    #parse gun action: 
                    if event.type == pygame.JOYBUTTONDOWN:
                        plane.gunDict[k].fire()
                        #textPrint.print_("JOYBUTTONDOWN")
                    elif event.type == pygame.JOYBUTTONUP:
                        #textPrint.print_("JOYBUTTONUP")
                        plane.gunDict[k].release()
                        #plane.gunDict[k].print_()
                elif k == RESET_KEY:
                    plane.resetGuns()
        textPrint.reset()
        textPrint.print_( plane.print_())
        pygame.display.flip()
        # Limit to 20 frames per second
        clock.tick(30)
    QUIT()

