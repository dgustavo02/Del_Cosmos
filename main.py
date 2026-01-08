import pygame
from pygame.locals import *
import random
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption('')


bg = pygame.image.load("assets/bg.png")

#clase Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, salud):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.salud_inicial= salud
        self.restante=salud
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        cooldown = 500

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if key[pygame.K_RIGHT] and self.rect.right < 600:
            self.rect.x += self.speed

        #a
        timer = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and timer- self.last_shot > cooldown:
            laser = Laser(self.rect.centerx, self.rect.top)
            grupo_laser.add(laser)
            self.last_shot = timer
        #green = (0, 255, 0)
        #red = (255, 0, 0)
        pygame.draw.rect(screen, (255, 0, 0),(self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.restante> 0:
            pygame.draw.rect(screen, (0, 255, 0),(self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.restante / self.salud_inicial) ), 15))

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/laser.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -=5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, grupo_meteor, True):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, s):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/meteor.png")
        self.rect = self.image.get_rect(center=(random.randint(50, 600 - 50), -50))
        self.speed = random.randint(4, 6) + s

    def update(self):
        self.rect.y += self.speed
        if pygame.sprite.spritecollide(self, grupo_player, False) and player.restante>0:
            self.kill()
            player.restante-= 2

        



    
grupo_player = pygame.sprite.Group()
grupo_laser = pygame.sprite.Group()
grupo_meteor = pygame.sprite.Group()

def create_enemy(sp):
    enemy = Enemy(sp)
    grupo_meteor.add(enemy)



player = Player(300,700, 6)
grupo_player.add(player)



def draw_bg(): 
    screen.blit(bg, (0,0))


def draw_text(text, size, x, y): 
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, (255, 255, 255))
    rect = render.get_rect(center=(x, y))
    screen.blit(render, rect)


def main_menu(): # menu principal de dos opciones empezar el juego o salirse del juego
    
    while True:
        draw_bg()
        draw_text("DEL COSMOS", 60, 300, 200)
        draw_text("Presiona ENTER para jugar", 30, 300, 300)
        draw_text("ESC para salir", 25, 300, 350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
    
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)

def game_over():
    while True:
        screen.fill((0, 0, 0))
        draw_text("GAME OVER", 60, 300 , 200)
        draw_text("ENTER para volver al menú", 30, 300, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player.restante = 6
                    grupo_meteor.empty()
                    main_menu()
                    
        pygame.display.update()
        clock.tick(60)


def game_loop():
    diff=0
    counter = 0
    spawn_timer = 0
    running = True
    while running:
        draw_bg()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Crear enemigos
        spawn_timer += 1
        if spawn_timer > 60:
            create_enemy(diff)
            spawn_timer=0
            counter +=1
            if counter > 5:
                create_enemy(diff)
                counter +=1
                diff= 2
                
        

        # actualizacion de sprites
        player.update()
        grupo_laser.update()
        grupo_meteor.update()

        if player.restante <= 0:
            game_over()
            
            
    

        # Dibujar
        grupo_player.draw(screen)
        grupo_laser.draw(screen)
        grupo_meteor.draw(screen)

        pygame.display.update()
        clock.tick(60)

main_menu()