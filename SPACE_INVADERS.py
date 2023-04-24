import pygame
import os
import time
import random
import sys

WIDTH = 750
HEIGHT = 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # 1

pygame.display.set_caption("Space Invaders")

COLOR_BLUE = (0,0,255) 
COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255,255,51)
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_blue = (0, 85, 92)  # 2

class Ship:  # 3

    HEIGHT = 20
    WIDTH = 70
    HEALTH = 100

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y 
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []

    def draw(self, window): # 4
        pygame.draw.rect(WIN, COLOR_BLUE, pygame.Rect(self.x, self.y, Ship.WIDTH, Ship.HEIGHT))


class Projectile:

    SIZE = 10  # e patrat
    vel = 10 # speed

    HITPOINT_enemy = 100  #HITPOINT
    HITPOINT_bunker1 = 100
    HITPOINT_bunker2 = 100
    HITPOINT_bunker3 = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window): # 4
        pygame.draw.rect(WIN, COLOR_WHITE, pygame.Rect(self.x, self.y, Projectile.SIZE, Projectile.SIZE))

    def move(self):
        self.y -= self.vel

    def ready_to_launch(self): # 11
        if self.y <= HEIGHT/2:
            return 1


class Enemy:

    SIZE = 20

    HITPOINT_PLAYER = 100
    HITPOINT_bunker1 = 100
    HITPOINT_bunker2 = 100
    HITPOINT_bunker3 = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window): # 4
        pygame.draw.rect(WIN, COLOR_GREEN, pygame.Rect(self.x, self.y, Enemy.SIZE, Enemy.SIZE))

    def move(self, vel):
        self.y += vel


class EnemyRocket:

    SIZE = 8

    HITPOINT = 100
    HITPOINT_PLAYER = 100
    HITPOINT_bunker1 = 100
    HITPOINT_bunker2 = 100
    HITPOINT_bunker3 = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window): # 4
        pygame.draw.rect(WIN, COLOR_RED, pygame.Rect(self.x, self.y, EnemyRocket.SIZE, EnemyRocket.SIZE))

    def move(self, vel):
        self.y += vel

    def ready_to_launch(self):
        if self.y >= HEIGHT - 8:
            return 1


class Bunker:

    HEIGHT = 40
    WIDTH = 120

    bunker1_HEALTH = 1000
    bunker2_HEALTH = 1000
    bunker3_HEALTH = 1000

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window): # 4
        pygame.draw.rect(WIN, COLOR_blue, pygame.Rect(self.x, self.y, Bunker.WIDTH, Bunker.HEIGHT))


def main(): # 5

    run = True
    FPS = 60
    clock = pygame.time.Clock()

    background = pygame.Surface((WIDTH, HEIGHT))
    background = background.convert()
    background.fill(COLOR_BLACK)

    SCORE = 0
    HIGHSCORE = 0

    missed_enemies = 0

    player_vel = 5  # 9 -  viteza navei-player 

    projectiles = [] # am initializat lista de proiectile

    enemies = []
    enemy_vel = 1  # viteza inamicilor
    wave_length = 5
    
    enemy_rockets = []
    enemy_rocket_vel = 3  # 19 -  viteza rachetelor inamice


    enemy_rocket = EnemyRocket(WIDTH, HEIGHT)  # daca nu initializam asta imi dadea eroarea: referenced before assignment
    
    projectile = Projectile(0, 0)

    ship = Ship(WIDTH/2 - Ship.WIDTH/2, HEIGHT - Ship.HEIGHT - 4)  # am facut ca nava sa fie desneta la mijlocul axei OX si cu 5 pixeli mai sus de fundul ecranului

    bunker1 = Bunker(3, HEIGHT - Bunker.HEIGHT - Ship.HEIGHT*5)
    bunker2 = Bunker(ship.x + ship.WIDTH/2 - Bunker.WIDTH/2, HEIGHT - Bunker.HEIGHT - Ship.HEIGHT*5)
    bunker3 = Bunker(WIDTH - Bunker.WIDTH - 3, HEIGHT - Bunker.HEIGHT - Ship.HEIGHT*5)


    def redraw_window(): # 6

        WIN.blit(background, (0,0))  # a pus poza sa inceapa din coltul din stanga: x=0,y=0
        
        for enemy in enemies:
            if (enemy.HITPOINT_bunker2 > 0 or bunker2.bunker2_HEALTH < 0) and (enemy.HITPOINT_bunker1 > 0 or bunker1.bunker1_HEALTH < 0) and (enemy.HITPOINT_bunker3 > 0 or bunker3.bunker3_HEALTH < 0) and enemy.HITPOINT_PLAYER > 0:
                enemy.draw(WIN)

        for enemy_rocket in enemy_rockets:
            if (enemy_rocket.HITPOINT_bunker2 > 0 or bunker2.bunker2_HEALTH < 0) and (enemy_rocket.HITPOINT_bunker1 > 0 or bunker1.bunker1_HEALTH < 0) and (enemy_rocket.HITPOINT_bunker3 > 0 or bunker3.bunker3_HEALTH < 0) and enemy_rocket.HITPOINT_PLAYER > 0:
                enemy_rocket.draw(WIN)
        
        if bunker1.bunker1_HEALTH > 0:
            bunker1.draw(WIN)
        if bunker2.bunker2_HEALTH > 0:
            bunker2.draw(WIN)
        if bunker3.bunker3_HEALTH > 0:
            bunker3.draw(WIN)

        ship.draw(WIN)
    
        # aici controlez afisarea laserului
        # daca laserul atinge bunkerul sau vreun enemy, atunci dispare
        # suplimentar daca bunkerul este distrus, atunci laserul nu mai dispare cand loveste zona in care a fost bunkerul
        for projectile in projectiles:
            if (projectile.HITPOINT_bunker2 > 0 or bunker2.bunker2_HEALTH < 0) and (projectile.HITPOINT_bunker1 > 0 or bunker1.bunker1_HEALTH < 0) and (projectile.HITPOINT_bunker3 > 0 or bunker3.bunker3_HEALTH < 0) and projectile.HITPOINT_enemy > 0:
                projectile.draw(WIN)

        pygame.display.set_caption("Space invaders  |   SCORE :  " + str(SCORE) + "   |   HIGHSCORE:  " + str(HIGHSCORE) )

        pygame.display.update()


    while run: # 7

        clock.tick(FPS)
        redraw_window() # am apelat functia de desenare a obiectelor claselor
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed() # 8
        if keys[pygame.K_ESCAPE]:
            quit()
        if keys[pygame.K_a] and ship.x - player_vel > 0:  # stanga
            ship.x -= player_vel
        if keys[pygame.K_d] and ship.x + player_vel + ship.WIDTH < WIDTH:  # dreapta
            ship.x += player_vel
        #if keys[pygame.K_w] and ship.y - player_vel > 0:  # up
            #ship.y -= player_vel 
        #if keys[pygame.K_s] and ship.y + player_vel + ship.HEIGHT < HEIGHT:  # down
            #ship.y += player_vel
        if keys[pygame.K_SPACE]:
            if projectile.ready_to_launch() == 1: # 10 
                projectile = Projectile(ship.x + ship.WIDTH/2 - Projectile.SIZE/2, ship.y - projectile.SIZE)  # am apelat clasa folosind o variabila cum am facut si cu ship
                projectiles.append(projectile) 
        
        for projectile in projectiles[:]: # 12
                    projectile.move()  # inainte sa il pun in for misca doar laserul curent, precedentul ingheta odata ce general altul
                    if projectile.x >= bunker1.x - projectile.SIZE and projectile.x <= bunker1.x + bunker1.WIDTH + projectile.SIZE and projectile.HITPOINT_bunker1 > 0: # 
                        if projectile.y <= bunker1.y + bunker1.HEIGHT: # verific coliziunea cu bunker1
                            bunker1.bunker1_HEALTH -= 200   # trebuie sa tragi de 5 ori in bunker ca sa dispara
                            projectile.HITPOINT_bunker1 = 0
                    if projectile.x >= bunker2.x - projectile.SIZE and projectile.x <= bunker2.x + bunker2.WIDTH + projectile.SIZE and projectile.HITPOINT_bunker2 > 0: # 
                        if projectile.y <= bunker2.y + bunker2.HEIGHT: # verific coliziunea cu bunker2
                            bunker2.bunker2_HEALTH -= 200   # trebuie sa tragi de 5 ori in bunker ca sa dispara
                            projectile.HITPOINT_bunker2 = 0
                    if projectile.x >= bunker3.x - projectile.SIZE and projectile.x <= bunker3.x + bunker3.WIDTH + projectile.SIZE and projectile.HITPOINT_bunker3 > 0: # 
                        if projectile.y <= bunker3.y + bunker3.HEIGHT: # verific coliziunea cu bunker3
                            bunker3.bunker3_HEALTH -= 200   # trebuie sa tragi de 5 ori in bunker ca sa dispara
                            projectile.HITPOINT_bunker3 = 0
                            #projectiles.remove(projectile)
                    if projectile.y + projectile.SIZE < 0: # 21
                        projectiles.remove(projectile)

        if len(enemies) == 0:  # 14 -  daca nu puneam conditia asta imi dadea o cascada de inamici, am vrut sa apara alt val de inamici doar dupa ce s a dus precedentul
            wave_length += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100)) #din nou am apelat clasa folosind o variabila ca la ship vreau sa genereze inamici la pozitii diferite
                enemies.append(enemy) # ii adaugam in lista cu inamici

        for enemy in enemies[:]: # 15 -  am facut o copie listei pt ca vom sterge din ea
            enemy.move(enemy_vel) # as putea s o pun in functia enemy hmm..
            
            if projectile.x >= enemy.x - projectile.SIZE and projectile.x <= enemy.x + enemy.SIZE and projectile.HITPOINT_enemy > 0:  # 13 -  am verificat coliziunea dintre enemy si projectile
                if projectile.y <= enemy.y + enemy.SIZE:
                    enemies.remove(enemy)
                    projectile.HITPOINT_enemy = 0  # ca sa fac laserul sa dispara cand loveste inamic
                    SCORE = SCORE + 1  # scorul creste cu 1 de fiecare data cand laserul a lovit un enemy

            if enemy.y > 0 and enemy.y < (HEIGHT/2) and enemy_rocket.ready_to_launch() == 1:  # 17
                enemy_rocket = EnemyRocket(enemy.x + enemy.SIZE/2 - EnemyRocket.SIZE/2, enemy.y + enemy.SIZE) # vreau sa se genereze din fundul lui enemy
                enemy_rockets.append(enemy_rocket)
            
            if enemy.x >= bunker1.x - enemy.SIZE and enemy.x <= bunker1.x + bunker1.WIDTH + enemy.SIZE: # 16 -  verific coliziunea dintre enemy si bunker1
                if enemy.y >= bunker1.y - enemy.SIZE:
                    enemy.HITPOINT_bunker1 = 0

            if enemy.x >= bunker2.x - enemy.SIZE and enemy.x <= bunker2.x + bunker2.WIDTH + enemy.SIZE: # verific coliziunea dintre enemy si bunker2
                if enemy.y >= bunker2.y - enemy.SIZE:
                    enemy.HITPOINT_bunker2 = 0

            if enemy.x >= bunker3.x - enemy.SIZE and enemy.x <= bunker3.x + bunker3.WIDTH + enemy.SIZE: # verific coliziunea dintre enemy si bunker3
                if enemy.y >= bunker3.y - enemy.SIZE:
                    enemy.HITPOINT_bunker3 = 0

            if enemy.x >= ship.x - enemy.SIZE and enemy.x <= ship.x + ship.WIDTH + enemy.SIZE:  # verific coliziunea cu nava player
                    if enemy.y >= ship.y - enemy.SIZE:
                        enemy.HITPOINT_PLAYER = 0
                        if (enemy.HITPOINT_bunker2 == 0 and bunker2.bunker2_HEALTH >= 0) or (enemy.HITPOINT_bunker1 == 0 and bunker1.bunker1_HEALTH >= 0) or (enemy.HITPOINT_bunker3 == 0 and bunker3.bunker3_HEALTH >= 0):
                            ship.HEALTH = 1
                        else:
                            ship.HEALTH = 0

            if enemy.y + enemy.SIZE > HEIGHT: #21
                enemies.remove(enemy)
                missed_enemies += 1

        
            if missed_enemies == 3:
                quit()

        for enemy_rocket in enemy_rockets[:]:  # 18

            enemy_rocket.move(enemy_rocket_vel)

            if enemy_rocket.x >= bunker1.x - enemy_rocket.SIZE and enemy_rocket.x <= bunker1.x + bunker1.WIDTH + enemy_rocket.SIZE: # verific coliziunea pe OX
                if enemy_rocket.y >= bunker1.y - enemy_rocket.SIZE:
                    bunker1.bunker1_HEALTH -= 1
                    enemy_rocket.HITPOINT_bunker1 = 0

            if enemy_rocket.x >= bunker2.x - enemy_rocket.SIZE and enemy_rocket.x <= bunker2.x + bunker2.WIDTH + enemy_rocket.SIZE: # verific coliziunea pe OX
                if enemy_rocket.y >= bunker2.y - enemy_rocket.SIZE:
                    bunker2.bunker2_HEALTH -= 1
                    enemy_rocket.HITPOINT_bunker2 = 0

            if enemy_rocket.x >= bunker3.x - enemy_rocket.SIZE and enemy_rocket.x <= bunker3.x + bunker3.WIDTH + enemy_rocket.SIZE: # verific coliziunea pe OX
                if enemy_rocket.y >= bunker3.y - enemy_rocket.SIZE:
                    bunker3.bunker3_HEALTH -= 1
                    enemy_rocket.HITPOINT_bunker3 = 0

            if enemy_rocket.x >= ship.x - enemy_rocket.SIZE and enemy_rocket.x <= ship.x + ship.WIDTH + enemy_rocket.SIZE:  # verific coliziunea cu nava player
                    if enemy_rocket.y >= ship.y - enemy_rocket.SIZE:
                        enemy_rocket.HITPOINT_PLAYER = 0  
                        if (enemy_rocket.HITPOINT_bunker2 == 0 and bunker2.bunker2_HEALTH >= 0) or (enemy_rocket.HITPOINT_bunker1 == 0 and bunker1.bunker1_HEALTH >= 0) or (enemy_rocket.HITPOINT_bunker3 == 0 and bunker3.bunker3_HEALTH >= 0):
                            ship.HEALTH = 1 
                        else:
                            ship.HEALTH = 0 

            if ship.HEALTH == 0: # verificam daca nava e moarta si daca da, atunci jocul se incheie
                quit()    
            
            if enemy_rocket.y + enemy_rocket.SIZE > HEIGHT: #20
                enemy_rockets.remove(enemy_rocket)
        
        # am notat bunker1-3.bunker1-3.HEALTH sanatatea bunkerelor
        # am notat projectile.HITPOINT_bunker1-3 variabila care comunica functie de afisare daca trebuie sa afiseze in continuare laserul (pentru projectile.HITPOINT_bunker1-3 > 0 DA, altfel NU)
main()