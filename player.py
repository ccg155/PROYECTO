import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        
        self.direction = pygame.math.Vector2() # Vector x: 0, y: 0
        self.speed = 5
        
        self.obstacle_sprites = obstacle_sprites
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0 # Si no hay ninguna tecla pulsada, Player no se mueve
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
       
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # Nos movemos a la derecha.
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # Nos movemos a la izquierda.
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # Nos movemos hacia abajo
                        self.hitbox.bottom = sprite.hitbox.top # Ponemos la parte baja del player(Self.rect.Bottom) pegada a la parte alta del obstacle (sprite.rect.top).
                    if self.direction.y < 0: # Nos movemos hacia arriba.
                        self.hitbox.top = sprite.hitbox.bottom
                    


        
    
    def update(self):
        self.input()
        self.move(self.speed)