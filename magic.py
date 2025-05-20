import pygame
from settings import *
from random import randint

class MagicExec:
    """
       Clase que gestiona la ejecución de hechizos mágicos en el juego.

       Esta clase maneja la lógica para ejecutar hechizos mágicos como la curación (heal) y los ataques de fuego (flame).
       Además, se encarga de reproducir los sonidos asociados a los hechizos y de crear las partículas correspondientes
       utilizando la clase `AnimationExec`.

       Atributos
       ----------
       animation_exec : AnimationExec
           Instancia del objeto que maneja las animaciones y efectos de partículas.
       sounds : dict
           Diccionario que almacena los sonidos asociados a los hechizos mágicos.

       Métodos
       -------
       heal(player, strength, cost, groups):
           Ejecuta un hechizo de curación sobre el jugador.
       flame(player, cost, groups):
           Ejecuta un hechizo de fuego que genera una secuencia de partículas de fuego.
       """

    def __init__(self, animation_exec):
        """
           Inicializa la clase `MagicExec`, configurando los sonidos de los hechizos y almacenando la instancia
           de `AnimationExec`.

           Parámetros
           ----------
           animation_exec : AnimationExec
               Instancia del objeto encargado de gestionar las animaciones y partículas mágicas.

           """
        self.animation_exec = animation_exec
        self.sounds = {
            'heal': pygame.mixer.Sound('audio/heal.wav'),
            'flame': pygame.mixer.Sound('audio/Fire.wav')
        }
    def heal(self, player, strength, cost, groups):
        """
           Ejecuta un hechizo de curación sobre el jugador, aumentando su salud y reduciendo su energía.

           Parámetros
           ----------
           player : Player
               El jugador que será curado por el hechizo.
           strength : int
               La cantidad de salud que se restaurará al jugador.
           cost : int
               El costo de energía para ejecutar el hechizo.
           groups : list
               Lista de grupos de sprites donde se generarán las partículas del hechizo.

           """
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_exec.create_particles('aura',player.rect.center, groups)
            self.animation_exec.create_particles('heal',player.rect.center + pygame.math.Vector2(0,-65), groups)


    def flame(self, player, cost, groups):
        """
         Ejecuta un hechizo de fuego que crea una serie de partículas de fuego en la dirección que está mirando el jugador.

         Parámetros
         ----------
         player : Player
             El jugador que ejecuta el hechizo.
         cost : int
             El costo de energía para ejecutar el hechizo.
         groups : list
             Lista de grupos de sprites donde se generarán las partículas de fuego.

         """
        if player.energy >= cost:
            self.sounds['flame'].play()
            player.energy -= cost

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0,-1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1,6):
                if direction.x: # Horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint( -TILESIZE//3, TILESIZE//3 )
                    y = player.rect.centery + randint( -TILESIZE//3, TILESIZE//3 )
                    self.animation_exec.create_particles('flame', (x,y), groups)

                else: # Vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx  + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_exec.create_particles('flame', (x, y), groups)

