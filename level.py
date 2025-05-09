import pygame
from settings import *
from tile import *
from player import *
from debug import *
from support import *
import random

class Level:
    def __init__(self):
        
        # Obtener la display surface. Que no es más que la totalidad de la pantalla
        
        self.display_surface = pygame.display.get_surface()
        
        # Setup de grupos de sprites.
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # Setup de los sprites.
        
        self.create_map()
        
    def create_map(self):
        
        layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'object': import_csv_layout('./map/map_Objects.csv')
        }
        
        graphics = {
            'grass': import_folder('./graphics/Grass'),
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
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'grass', random.choice(graphics['grass']))
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                            
                        
        self.player = Player((2000,1430), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player) # Llamamos a la funcion draw en el grupo 'visible_sprites' y dibujamos al mismo sobre display_surface
        self.visible_sprites.update()
        debug(self.player.direction)
        
        
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
        