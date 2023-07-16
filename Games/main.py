import pygame
import math
import random
from pygame import mixer

# initializing pygame
pygame.init()

# setting screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("bcg.jpg")

# background sound
mixer.music.load("background.mp3")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invadors")
icon = pygame.image.load("sicon.webp")
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load("player.png")
playerX = 368
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("ghost.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(0.6)
    enemyY_change.append(40)

# laser
laserImg = pygame.image.load("laser.png")
laserX = playerX
laserY = playerY
laserX_change = 0
laserY_change = 1.2
laser_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 560

# game over
over_font = pygame.font.Font('game_over.ttf', 240)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 122, 143))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (120, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))


def isCollision(enX, enY, laX, laY):
    distance = math.sqrt(math.pow(enX - laX, 2) + math.pow(enY - laY, 2))
    if distance <= 30:
        return True
    else:
        return False


# game loop
running = True
while running:

    screen.fill((0, 0, 21))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.25
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.25
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    bullet_sound = mixer.Sound("laser.mp3")
                    bullet_sound.play()
                    laserX = playerX
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        # game over
        if enemyY[i] >= 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] = - enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            collision_sound = mixer.Sound("explosion.mp3")
            collision_sound.play()
            laserY = 480
            laser_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 200)

        enemy(enemyX[i], enemyY[i], i)

    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state == 'fire':
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()