import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    """
      Representa un bloque o azulejo en el mundo del juego. Los azulejos pueden ser objetos o
      parte del fondo y tienen un tipo de sprite asociado.

      Hereda de:
      ----------
      pygame.sprite.Sprite

      Parámetros
      ----------
      pos : tuple
          Posición del azulejo en el mundo del juego (x, y).
      groups : list
          Lista de grupos de sprites a los que se debe agregar este azulejo.
      sprite_type : str
          Tipo de sprite ('object' o 'background') que determina su comportamiento en el mundo.
      surface : pygame.Surface, opcional
          Superficie que representa el azulejo, por defecto es un cuadrado vacío de tamaño `TILESIZE`.
      """
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        """
            Inicializa un nuevo azulejo en el juego.

            Parámetros
            ----------
            pos : tuple
                Posición del azulejo en el mundo del juego (x, y).
            groups : list
                Lista de grupos de sprites a los que se debe agregar este azulejo.
            sprite_type : str
                Tipo de sprite ('object' o 'background') que determina su comportamiento en el mundo.
            surface : pygame.Surface, opcional
                Superficie que representa el azulejo. Se usa una superficie predeterminada de tamaño
                `TILESIZE` si no se proporciona una. Por defecto es un cuadrado vacío.

            Atributos
            ----------
            sprite_type : str
                Tipo de sprite del azulejo ('object' o 'background').
            image : pygame.Surface
                Superficie que contiene la imagen del azulejo.
            rect : pygame.Rect
                Rectángulo delimitador del azulejo, se utiliza para colisiones y posicionamiento.
            hitbox : pygame.Rect
                Rectángulo que representa la "zona activa" para interacciones, ligeramente más pequeño que `rect`.
            """
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE ))
        
        else: 
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)