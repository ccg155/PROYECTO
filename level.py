import pygame

from magic import MagicExec
from settings import *
from tile import *
from player import *
from debug import *
from support import *
import random
from weapon import *
from ui import *
from enemy import Enemy
from particles import *
from random import randint
from magic import *
from upgrade import Upgrade

class Level:
    def __init__(self):

        # Pausa del juego
        self.game_paused = False

        # Obtener la display surface. Que no es más que la totalidad de la pantalla
        
        self.display_surface = pygame.display.get_surface()
        
        # Setup de grupos de sprites.
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Sprites de ataque
        self.current_attack = None
        self.attackable_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        # Setup de los sprites.
        self.create_map()

        # Interfaz de usuario
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # Partículas
        self.animation_exec = AnimationExec()
        self.magic_exec = MagicExec(self.animation_exec)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_exec.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_exec.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
        
    def create_map(self):
        
        layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'object': import_csv_layout('./map/map_Objects.csv'),
            'entities': import_csv_layout('./map/map_Entities.csv')
        }
        
        graphics = {
            'grass': import_folder('./graphics/grass'),
            'objects': import_folder('./graphics/objects')
        }
        
        for style, layout in layouts.items():   
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE # Coordenadas en x.
                        y = row_index * TILESIZE # Coordenadas en y.
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'grass', random.choice(graphics['grass']))
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                        if style == 'entities':
                            if col == '394': # ID del jugador en el .CSV
                                self.player = Player((x,y),
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic)
                            else:
                                if col == '390': enemy_name = 'bamboo'
                                elif col == '391': enemy_name = 'spirit'
                                elif col == '392': enemy_name = 'raccoon'
                                elif col == '393': enemy_name = 'squid'
                                Enemy(enemy_name,(x,y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites, self.dmg_player, self.enemy_death_particle, self.gain_xp)

    def attack_logic_player(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,50)
                            for leaf in range(randint(3,6)):
                                self.animation_exec.create_grass_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        elif target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def dmg_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            # Partículas
            self.animation_exec.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def enemy_death_particle(self, pos, particle_type):
        self.animation_exec.create_particles(particle_type, pos, self.visible_sprites)


    def gain_xp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        # Mostrar menú de mejoras
        if self.game_paused:
            self.upgrade.display()
        # Ejecutar el juego
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update_level(self.player)
            self.attack_logic_player()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        
        # Creando el suelo
        self.floor_surf = pygame.image.load('./graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))


        self.offset = pygame.math.Vector2()
    def custom_draw(self, player):
        
        # Conseguimos el desplazamiento (offset)
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth 
        
        # Dibujando el mapa
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update_level(self, player):
        enemy_sprites = []
        for sprite in self.sprites():
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy':
                enemy_sprites.append(sprite)

        for enemy in enemy_sprites:
            enemy.enemy_update(player)