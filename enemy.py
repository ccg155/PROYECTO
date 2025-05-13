import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self, enemy_name, pos, groups, obstacle_sprites):

        # Setup general
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # Setup de los recursos gráficos
        self.import_graphics(enemy_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # Movimiento
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # Estadísticas del enemigo
        self.enemy_name = enemy_name
        enemy_info = monster_data[self.enemy_name]
        self.health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.speed = enemy_info['speed']
        self.attack_damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.attack_type = enemy_info['attack_type']


    def import_graphics(self, enemy_name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'./graphics/monsters/{enemy_name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2(0,0)

        return distance, direction

    def enemy_status(self, player):
        distance = self.get_player_distance_direction

        if distance <= self.attack_radius:
            self_status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def update(self):
        self.move(self.speed)

