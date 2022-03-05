
import socket
import threading

host=socket.gethostbyname(socket.gethostname())
port=5050
ADDR=(host, port)

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

import pygame
import random
from pygame import mixer


import math
pygame.init()
screen = pygame.display.set_mode((800, 600))
background=pygame.image.load('Forest.PNG')

#background music
mixer.music.load('Boney_M_-_Jingle_Bells.mp3')
mixer.music.play(-1)

# Tittle and icon
pygame.display.set_caption("Merry Christmas")
icon = pygame.image.load('elf.png')
pygame.display.set_icon(icon)

# player
playerIMG = pygame.image.load("santa-claus.png")
playerX = 370
playerY = 480
playerX_change = 0




# enemy
enemyIMG=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=5

for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load("elf.png"))
    enemyX.append(random.randint(0,720))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.9)
    enemyY_change.append(40)

# Bullet
#Ready- you can't see the bulet on the screen
# Fire - the bullet is currently moving

#bullet 1
bulletIMG = pygame.image.load("candy-cane.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state="ready"

#Bulet2

bulletIMG2 = pygame.image.load("candy.png")
bulletX2 = 0
bulletY2 = 480
bulletX_change2 = 0
bulletY_change2 = 5
bullet_state2="ready"

#Score

score_value=0
font= pygame.font.Font('freesansbold.ttf',20)
textX=10
testY=10

#Happy Christmas text
over_font=pygame.font.Font('freesansbold.ttf', 40)


def show_score(x,y):
    score=font.render("Score: "+ str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def Happy_Christmas_text():
    over_text=over_font.render("Happy Christmas", True, (255, 255, 255))
    screen.blit(over_text, (250,200))

def player(x, y):
    screen.blit(playerIMG, (x, y))


def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletIMG, (x, y))

def fire_bullet2(x,y):
    global bullet_state2
    bullet_state2="fire"
    screen.blit(bulletIMG2, (x, y))

def Collision(enemyX, enemyY, bulletX, bulletY):
    distance= ((bulletX-enemyX)**2 + (bulletY-enemyY)**2)**0.5
    if distance<33:
        return True
    else:
        return False

def Collision2(enemyX, enemyY, bulletX2, bulletY2):
    distance= ((bulletX2-enemyX)**2 + (bulletY2-enemyY)**2)**0.5
    if distance<33:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    # RGB colors
    # screen.fill((0, 0, 0))
    # pygame.display.update()
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            message="quit"
            client.send(message.encode('utf-8'))
            running = False
        # if keystroke is pressed check if it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.9

            if event.key == pygame.K_RIGHT:
                playerX_change = 1.9
            if event.key == pygame.K_SPACE:
                if bullet_state=='ready':
                    bullet_Sound=mixer.Sound('mixkit-winning-a-coin-video-game-2069.wav')
                    bullet_Sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_SPACE and bulletY<240:
                    bulletX2=playerX
                    fire_bullet2(bulletX2, bulletY2)
                    bullet_Sound = mixer.Sound('mixkit-winning-a-coin-video-game-2069.wav')
                    bullet_Sound.play()



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 739:
        playerX = 739
    #Enemy Movement
    if score_value==5:
        Happy_Christmas_text()

    for i in range(num_of_enemies):
        # #Game over
        # if enemyY[i] > 200:
        #     for j in range(num_of_enemies):
        #         enemyY[j]=2000
        #     Happy_Christmas_text()
        #     break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.9
            enemyY[i] +=enemyY_change[i]
        elif enemyX[i] >= 739:
            enemyX_change[i] = -1.9
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value+= 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = 2000
            bullet_Sound2 = mixer.Sound('mixkit-player-jumping-in-a-video-game-2043.wav')
            bullet_Sound2.play()

            # Collision2
        collision2 = Collision2(enemyX[i], enemyY[i], bulletX2, bulletY2)
        if collision2:
            bulletY2 = 480
            bullet_state = "ready"
            score_value += 1
            bullet_Sound2 = mixer.Sound('mixkit-player-jumping-in-a-video-game-2043.wav')
            bullet_Sound2.play()

            enemyX[i] = random.randint(0, 800)
            enemyY[i] = 2000

        enemy(enemyX[i], enemyY[i], i)

    #Bullet movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -=bulletY_change
    # Bullet2 movement
    if bulletY2 <= 0:
        bulletY2 = 480
        bullet_state2 = "ready"
    if bullet_state2 == 'fire':
        fire_bullet2(bulletX2, bulletY2)
        bulletY2 -= bulletY_change2

    player(playerX, playerY)
    #score
    show_score(textX, testY)
    pygame.display.flip()
    pygame.display.update()
