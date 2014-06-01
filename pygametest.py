import pygame, sys
from pygame.locals import *
import random
import math


box = pygame.Rect((0, 0), (50, 50))
blue = (0,0,255)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
WIDTH = 1930
HEIGHT = 1200



class Flower(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice([pygame.image.load('flower.png').convert_alpha(),pygame.image.load('flower1.png').convert_alpha()])
        
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def reset_pos(self):
        self.rect.y = random.randrange(-1000, -10)
        self.rect.x = random.randrange(-100,WIDTH+100)

    def update(self):
        self.rect.y += 10
        if self.rect.y>1200:
            self.reset_pos()

def angle_to_vector(ang):
    return [math.cos(ang), -math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,vel,angle, joy=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flutter.png").convert_alpha()
        #self.image.set_colorkey(white)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.pos = [WIDTH//2,HEIGHT//2]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image_center = self.rect.center
        if joy is not None:
            self.joy = pygame.joystick.Joystick(joy)
            self.joy.init()
            print self.joy.get_name()

    def update(self):
        accel = 0.5
        friction = accel/20
        self.angle += self.angle_vel
        self.forward = angle_to_vector(math.radians(self.angle))
        
        axis0 = self.joy.get_axis(0)
        axis1 = self.joy.get_axis(1)

        

        if (abs(axis0) > 0.1) or (abs(axis1) > 0.1):
            self.thrust = True
            self.image = pygame.image.load("flutter2.png").convert_alpha()
            if pygame.time.get_ticks()%2 ==0:
                self.image = pygame.image.load("flutter.png").convert_alpha()
        else:
            self.thrust = False
            self.image = pygame.image.load("flutter.png").convert_alpha()

        #print self.thrust

        self.vel[0] += axis0
        self.vel[1] += axis1

        
        

        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1])% HEIGHT
        self.rect.center = self.pos

class Sparkle(pygame.sprite.Sprite):
    def __init__(self,parent):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(parent.pos)
        self.vel = list(parent.vel)
        self.image = pygame.image.load("bluesparkle.png").convert_alpha()
        self.angle = 0
        self.angle_vel = 0
        self.life = 5
        self.rect = self.image.get_rect()
        self.image_center = self.rect.center
    
    
    def update(self):
        self.life +=1
        self.rect.center = self.pos
        

        
        
        

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
fpsClock = pygame.time.Clock()
score = 0
#Before the loop, load sounds
click_sound = pygame.mixer.Sound("laser5.ogg")
screenSize = (WIDTH,HEIGHT)
surface = pygame.display.set_mode(screenSize)
background = pygame.image.load("outer-space_00399584.jpg").convert()
pygame.display.set_caption("space game")




def flower_spawn(flowerlist,heaven):
    for flower in flowerlist:
        if flower not in heaven:
            flower.update()

Flower_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
sparkles = pygame.sprite.Group()
for i in range(300):
    flower = Flower()
    Flower_list.add(flower)

p1 = Player([0,0],[0,0],0, joy=0)
all_sprites_list.add(p1)

pygame.time.set_timer(USEREVENT+1, 20)



done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == USEREVENT+1:
            print "userevent"
            for sparkle_parent in all_sprites_list:
                sparkles.add(Sparkle(sparkle_parent))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
    surface.blit(background,(0,0))
    #Flower_list.update()
    Flower_list.draw(surface) 
    all_sprites_list.update()
    all_sprites_list.draw(surface)
    sparkles.update()
    sparkles.draw(surface)
    heaven = [] 
    myfont1 = pygame.font.SysFont("monospace",80)
    label1 = myfont1.render("Score : "+str(score),1,(255,1,200))
    surface.blit(label1,(WIDTH-600,20))
    collide_list = pygame.sprite.groupcollide(Flower_list,all_sprites_list,False, False, collided = pygame.sprite.collide_mask)
    for flower in collide_list:
        score+=1
        heaven.append(flower)
        flower.reset_pos()

        #print "Score: "+str(score)
    flower_spawn(Flower_list,heaven)
    pygame.display.flip()
    pygame.display.update()
    fpsClock.tick(30)


pygame.quit ()