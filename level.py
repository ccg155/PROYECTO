import pygame
from settings import *
from tile import *
from player import *
from debug import *
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
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE # Coordenadas en x.
                y = row_index * TILESIZE # Coordenadas en y.
                if col == 'x':
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites]) # Creamos una tile y la metemos en el grupo 'visible_sprites'.
                elif col == 'p':
                   self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)
        
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


        self.offset = pygame.math.Vector2()
    def custom_draw(self, player):
        
        # Conseguimos el desplazamiento (offset)
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        