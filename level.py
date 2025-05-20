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

    """
    Clase que gestiona toda la lógica del nivel, incluyendo el mapa, jugadores, enemigos, ataques,
    partículas y la interfaz de usuario.

    Atributos
    ----------
    game_paused : bool
        Indica si el juego está en pausa.
    display_surface : pygame.Surface
        Superficie de visualización principal del juego.
    visible_sprites : YSortCameraGroup
        Grupo de sprites visibles ordenados por coordenada Y (efecto de profundidad).
    obstacle_sprites : pygame.sprite.Group
        Grupo de sprites que actúan como obstáculos (colisiones).
    current_attack : Weapon or None
        Ataque activo actual del jugador.
    attackable_sprites : pygame.sprite.Group
        Sprites que pueden ser afectados por ataques.
    attack_sprites : pygame.sprite.Group
        Sprites que representan los ataques activos.
    ui : UI
        Interfaz de usuario.
    upgrade : Upgrade
        Sistema de mejora del jugador.
    animation_exec : AnimationExec
        Administrador de efectos de animaciones/partículas.
    magic_exec : MagicExec
        Administrador de hechizos mágicos.

    Métodos
    -------
    create_attack():
        Crea un ataque físico del jugador.
    create_magic(style, strength, cost):
        Ejecuta un hechizo mágico del jugador.
    destroy_attack():
        Elimina el ataque actual.
    create_map():
        Crea el mapa del juego basado en archivos CSV.
    attack_logic_player():
        Lógica de colisiones entre ataques del jugador y objetos o enemigos.
    dmg_player(amount, attack_type):
        Aplica daño al jugador y crea efectos de partículas.
    enemy_death_particle(pos, particle_type):
        Crea partículas cuando un enemigo muere.
    gain_xp(amount):
        Añade experiencia al jugador.
    toggle_menu():
        Alterna entre pausa y juego activo.
    run():
        Ejecuta la lógica de actualización y renderizado del nivel.
    """

    def __init__(self):
        """
           Inicializa el nivel del juego, configurando los grupos de sprites y la interfaz de usuario.
           Además, crea el mapa, los enemigos y otras entidades necesarias.

           """

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
        """
            Crea un ataque físico para el jugador y lo agrega a los grupos correspondientes.

            """
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        """
           Crea y ejecuta un hechizo mágico basado en el estilo, fuerza y costo proporcionados.

           Parámetros
           ----------
           style : str
               El estilo de magia a ejecutar. Puede ser 'heal' para curación o 'flame' para ataque de fuego.
           strength : int
               La fuerza del hechizo (para curación o daño).
           cost : int
               El costo de maná o energía para ejecutar el hechizo.

           """

        if style == 'heal':
            self.magic_exec.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_exec.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        """
            Elimina el ataque actual del jugador si existe.

            """
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
        
    def create_map(self):
        """
          Crea el mapa del juego cargando y procesando archivos CSV y gráficos.

          Organiza las capas de terreno, obstáculos, objetos y entidades, y coloca los sprites correspondientes
          en la pantalla.

          """
        
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
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
        """
           Lógica de colisiones entre los ataques del jugador y los objetos o enemigos.

           Si un ataque del jugador colisiona con un objeto o enemigo, se aplica el daño o se generan efectos.

           """
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
        """
           Aplica daño al jugador y genera partículas visuales asociadas al tipo de ataque.

           Parámetros
           ----------
           amount : int
               La cantidad de daño que se aplicará al jugador.
           attack_type : str
               El tipo de ataque (por ejemplo, 'flame', 'sword', etc.).

           """
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            # Partículas
            self.animation_exec.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def enemy_death_particle(self, pos, particle_type):
        """
          Crea partículas cuando un enemigo muere, usando el tipo de partícula proporcionado.

          Parámetros
          ----------
          pos : tuple
              La posición en la que se generarán las partículas.
          particle_type : str
              El tipo de partícula a generar (por ejemplo, 'flame', 'blood', etc.).

          """
        self.animation_exec.create_particles(particle_type, pos, self.visible_sprites)


    def gain_xp(self, amount):
        """
          Añade la cantidad de experiencia especificada al jugador.

          Parámetros
          ----------
          amount : int
              La cantidad de experiencia a añadir.

          """
        self.player.exp += amount

    def toggle_menu(self):
        """
          Alterna entre la pausa del juego y el estado activo.

          Cambia el valor de la variable `game_paused` para pausar o reanudar el juego.

          """
        self.game_paused = not self.game_paused

    def run(self):
        """
           Ejecuta la lógica de actualización y renderizado del nivel.

           Actualiza todos los sprites visibles y enemigos, maneja las colisiones y ataques,
           y dibuja la interfaz de usuario.

           """
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
    """
     Grupo de sprites con cámara que ordena los sprites según su coordenada Y,
     proporcionando una simulación de profundidad (z-index).

     Atributos
     ----------
     display_surface : pygame.Surface
         Superficie de visualización principal.
     half_width : int
         Mitad del ancho de la pantalla.
     half_heigth : int
         Mitad de la altura de la pantalla.
     floor_surf : pygame.Surface
         Imagen del suelo del nivel.
     floor_rect : pygame.Rect
         Rectángulo que delimita el suelo.
     offset : pygame.math.Vector2
         Desplazamiento de cámara en x e y, centrado en el jugador.

     Métodos
     -------
     custom_draw(player):
         Dibuja todos los sprites ordenados por Y con desplazamiento centrado en el jugador.
     enemy_update_level(player):
         Llama a la actualización específica de enemigos visibles en el nivel.
     """
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        
        # Creando el suelo
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))


        self.offset = pygame.math.Vector2()
    def custom_draw(self, player):
        """
          Dibuja todos los sprites ordenados por su coordenada Y, aplicando un desplazamiento para centrar la cámara en el jugador.

          Parámetros
          ----------
          player : Player
              El jugador cuya posición se utiliza para centrar la cámara.

          """
        
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
        """
          Actualiza a los enemigos visibles en el nivel, llamando su método de actualización.

          Parámetros
          ----------
          player : Player
              El jugador que es usado para actualizar a los enemigos visibles.

          """
        enemy_sprites = []
        for sprite in self.sprites():
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy':
                enemy_sprites.append(sprite)

        for enemy in enemy_sprites:
            enemy.enemy_update(player)