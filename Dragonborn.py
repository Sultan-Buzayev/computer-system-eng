# -*- coding: utf-8 -*- 
# Importowanie bibliotek
import pygame
from pygame.locals import *
import math
import random
import sys
import time
import threading
import msvcrt
import os
from sys import exit

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (180,100)

# Inicjowanie gry
pygame.init()
start = 0
start1 = 0
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
acc = [0,0]
arrows = []

keys = [False, False, False, False]
playerpos = [250,300]

badtimer = 100
badtimer1 = 0
badguys = [[840, 100]]
healthvalue = 194
cl_ch = 0

def load_image(name):
    image = pygame.image.load(name)
    return image


class TestSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(TestSprite, self).__init__()
        self.images = []

        for i in range(10, 20):
            for j in range(0, 3):
                self.images.append(load_image("dragon_frame_" + str(i) + '.png'))

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(50, 380, 640, 640)

    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

class TestSprite2(pygame.sprite.Sprite):
    def __init__(self):
        super(TestSprite2, self).__init__()
        self.images = []

        for i in range(10, 20):
            for j in range(0, 3):
                self.images.append(load_image("dragon_frame_" + str(i) + '.png'))

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(50, 10, 640, 640)

    def update(self):
        ''' Ta metoda przechodzi przez elementy wewnatrz self.images i wyswietla kazdy nastepny po kazdemu kadru '''
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        

pygame.mixer.init()
badguyimg = [0, 0]

# Load images
player = pygame.image.load("archer.png")
arrow = pygame.image.load("bullet.png")
badguyimg[0] = pygame.image.load("dragonblue.png")
badguyimg[1] = pygame.image.load("dragongrey.png")
healthbar = pygame.image.load("healthbar.png")
health = pygame.image.load("health.png")

gameover = pygame.image.load("gameover.png")
youwin = pygame.image.load("youwin.png")

# Loading sounds
hit = pygame.mixer.Sound("explode.wav")
enemy = pygame.mixer.Sound("enemy.wav")
shoot = pygame.mixer.Sound("shoot.wav")
hit.set_volume(0.1)
enemy.set_volume(0.05)
shoot.set_volume(0.02)


# Adding a background (Dodawanie tla)
grass = pygame.image.load("background.jpg")
castle = pygame.image.load("castle2.png")
startScreen = pygame.image.load("start11.jpg")

running = 1
exitcode = 0
drag_index = 0

my_sprite = TestSprite()
my_group = pygame.sprite.Group(my_sprite)

my_sprite2 = TestSprite2()
my_group2 = pygame.sprite.Group(my_sprite2)

while start == 0:
    
    screen.fill(0)
    
    screen.blit(startScreen, (-100, -200))
    
    pygame.display.flip()
    
    for event in pygame.event.get():   
         if event.type == pygame.MOUSEBUTTONDOWN:  
            start = 1

screen = pygame.display.set_mode((800, 600))
pygame.mixer.music.load('skyrim.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.21)

# Keep looping through
while running:
    
    badtimer -= 1
    # clear the screen before drawing it again
    screen.fill(0)
    
    screen.blit(grass, (0, 0))
    screen.blit(castle,(0, 50))
    
    # Ustawic pozycje gracza i rotacje
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
    playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)
    playerpos1 = (playerpos[0] - playerrot.get_rect().width/2, playerpos[1] - playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)

    # Narysowac strzalki
    for bullet in arrows:
        index = 0
        # liczba na koncu to predkosc strzalki
        velx = math.cos(bullet[0]) * 25
        vely = math.sin(bullet[0]) * 25
        bullet[1] += velx
        bullet[2] += vely
        
        if bullet[1] < -64 or bullet[1] > 820 or bullet[2] < -64 or bullet[2] > 620:
            arrows.pop(index)
            
        index += 1
        
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))

    # Draw enemies
    if badtimer == 0:
        badguys.append([840, random.randint(40, 500)])
        badtimer = 100 - (badtimer1 * 2)
        if badtimer1 >= 35:
            badtimer1 = 35
            drag_index = 1
        else:
            badtimer1 += 5
            
            
    index = 0
    
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)
        badguy[0] -= 10
        

        # Atakowanie zamku
        badrect = pygame.Rect(badguyimg[drag_index].get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 300:
            hit.play()
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
            cl_ch = 1

        # Sprawdzanie kolizji enemy and arrow
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0] += 1
                if cl_ch == 0: badguys.pop(index)
                arrows.pop(index1)
            index1 += 1
        cl_ch = 0
            
        # Next dragon
        index += 1
    #
    for badguy in badguys:
        screen.blit(badguyimg[drag_index], badguy)
        

    # Rysowanie zegara
    font = pygame.font.Font(None, 22)
    survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000) + ":" + str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, [255, 255, 255])
    textRect = survivedtext.get_rect()
    textRect.topright = [785,5]
    screen.blit(survivedtext, textRect)

    dragons_counter = font.render("Killed bad dragons: " + str(acc[0]), True, (0, 255, 0))
    textRect1 = dragons_counter.get_rect()
    textRect1.topleft = [220, 10]
    screen.blit(dragons_counter, textRect1)

    # Rysowanie paska zdrowia
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1 + 8,8))
    
    my_group.update()
    my_group.draw(screen)

    my_group2.update()
    my_group2.draw(screen)

    # update the screen
    pygame.display.flip()
    
    # loop through the events
    for event in pygame.event.get():   
         
        if event.type == pygame.QUIT:  
            # quit the game
            pygame.display.quit()
            pygame.quit()
            exit(0)
        
        # event checking
        if event.type == pygame.KEYDOWN:
            
            if event.key == K_w:
                 keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
            elif event.key == K_ESCAPE:
                pygame.quit()
                exit(0)
                    
        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
            elif event.key == K_ESCAPE:
                pygame.quit()
                exit(0)

        # Jesli kliknieto mysza, zapisz wartosc rotacji w array arrows na podstawie pozycji kursora
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1] - (playerpos1[1] + 52), position[0] - (playerpos1[0] + 56)), playerpos1[0] + 32, playerpos1[1] + 32])

            
    # Zmiana pozycji gracza
    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    if keys[1]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5

    # Win/Lose Checking
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0
        
    # Wazne! Nie powinnismy dzielic sie przez 0 w przypadku, gdy gracz nie strzelil
    if acc[1] != 0:
        accuracy = acc[0] * 1.0 / acc[1] * 100
    else:
        accuracy = 0

# Win/Lose na ekranie
if exitcode == 0:

    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Killed dragons: " + str(acc[0]) + ", Accuracy: " + "%2.f" % accuracy + "%", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    pygame.font.init();
    font = pygame.font.Font(None, 24)
    text = font.render("Killed dragons: " + str(acc[0]) + ", Accuracy: " + "%2.f" % accuracy + "%", True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
