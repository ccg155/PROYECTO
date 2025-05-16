import pygame
from settings import *
from entity import Entity
from support import *
from debug import *

class Enemy(Entity):
    def __init__(self, enemy_name, pos, groups, obstacle_sprites, dmg_player, death_particles, gain_xp):

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

        # Interacción con el jugador
        self.able_to_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.dmg_player = dmg_player
        self.death_particles = death_particles
        self.gain_xp = gain_xp

        # Periodo de invencibilidad
        self.vulnerable = True
        self.hit_time = 0
        self.invincibility_duration = 300


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
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.able_to_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def action(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.dmg_player(self.attack_damage, self.attack_type)
        if self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]

    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if not self.able_to_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.able_to_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True


    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.able_to_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.alpha_variation()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_dmg()
            else:
                self.health -= player.get_full_magic_dmg()
                # Daño por magia
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def is_dead(self):
        if self.health <= 0:
            self.death_particles(self.rect.center, self.enemy_name)
            self.kill()
            self.gain_xp(self.exp)
    def knockback(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.knockback()
        self.move(self.speed)

    def enemy_update(self, player):
        self.enemy_status(player)
        self.action(player)
        self.animate()
        self.cooldown()
        self.is_dead()


