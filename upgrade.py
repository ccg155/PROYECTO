import pygame
from settings import *

class Upgrade:

    """
    Clase que gestiona el sistema de mejoras del jugador mediante una interfaz de usuario.

    Atributos
    ----------
    display_surface : pygame.Surface
        Superficie principal de renderizado.
    player : Player
        Referencia al jugador para acceder a sus estadísticas y experiencia.
    attribute_n : int
        Número total de estadísticas que pueden mejorarse.
    attribute_names : list
        Nombres de las estadísticas del jugador.
    font : pygame.font.Font
        Fuente usada para mostrar texto.
    max_values : list
        Valores máximos permitidos por cada estadística.
    height : float
        Altura de cada rectángulo de mejora.
    width : int
        Ancho de cada rectángulo de mejora.
    item_list : list
        Lista de instancias de `Item`, representando cada mejora visualmente.
    selection_index : int
        Índice del ítem actualmente seleccionado.
    selection_time : int
        Tiempo en el que se realizó la última selección.
    able_to_move : bool
        Controla si se puede mover la selección entre estadísticas.
    selection_time_cooldown : int
        Tiempo de espera en milisegundos entre movimientos de selección.

    Métodos
    -------
    input():
        Captura entradas del teclado para navegar y aplicar mejoras.
    selection_cooldown():
        Controla el tiempo entre cada movimiento de selección.
    display():
        Renderiza la interfaz de mejora, incluyendo las barras, nombres y costos.
    create_items():
        Crea los objetos `Item` con su posición y apariencia.
    """

    def __init__(self, player):
        """
           Inicializa el sistema de mejoras.

           Parámetros
           ----------
           player : Player
               Referencia al objeto jugador que contiene las estadísticas y experiencia.
           """

        # Setup general
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_n = len(player.stats) # Número de estadísticas
        self.attribute_names = list(player.stats.keys()) # Nombre de las estadísticas
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.max_values = list(player.max_stats.values())

        # Creación de los ítems
        self.height = self.display_surface.get_size()[1] * 0.8 # Altura de los objetos
        self.width = self.display_surface.get_size()[0] // 6 # Anchura entre los rectángulos
        self.create_items()

        # Sistema de selección
        self.selection_index = 0
        self.selection_time = 0
        self.able_to_move = True
        self.selection_time_cooldown = 300



    def input(self):
        """
           Captura entradas del teclado para navegar y aplicar mejoras.

           Permite mover la selección entre las estadísticas y aplicar mejoras cuando se presiona la tecla de espacio.
           """
        keys = pygame.key.get_pressed()

        if self.able_to_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_n - 1:
                self.selection_index += 1
                self.able_to_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.able_to_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]: # Botón de selección
                self.able_to_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        """
           Controla el tiempo entre cada movimiento de selección.

           Evita que el jugador se mueva rápidamente entre las estadísticas sin esperar el tiempo de cooldown.
           """
        if not self.able_to_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= self.selection_time_cooldown:
                self.able_to_move = True

    def display(self):
        """
         Renderiza la interfaz de mejora, incluyendo las barras, nombres y costos.

         Muestra visualmente las estadísticas disponibles para mejorar y las opciones de selección.
         """
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):

            # Conseguir nombre de las estadísticas
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)

            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


    def create_items(self):
        """
           Crea los objetos `Item` que representan cada mejora visualmente.

           Establece la posición y apariencia de los ítems en la interfaz de usuario.
           """
        self.item_list = []

        for item, index in enumerate(range(self.attribute_n)):

            # Horizontal
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_n
            x = (item * increment) + (increment - self.width) // 2

            # Vertical
            y = self.display_surface.get_size()[1] * 0.1


            # Crear stat
            item = Item(x, y, self.width, self.height, index, self.font)
            self.item_list.append(item)


class Item:
    """
      Clase que representa un ítem dentro del sistema de mejoras del jugador.

      Atributos
      ----------
      rect : pygame.Rect
          Rectángulo que define la posición y tamaño del ítem.
      index : int
          Índice que representa la estadística que se va a mejorar.
      font : pygame.font.Font
          Fuente usada para mostrar texto en el ítem.

      Métodos
      -------
      display_names(surface, name, cost, selected):
          Muestra el nombre y el costo de la mejora en el ítem.
      display_bar(surface, value, max_value, selected):
          Muestra una barra de progreso representando el valor de la estadística.
      trigger(player):
          Aplica la mejora al jugador si tiene suficiente experiencia.
      display(surface, selection_index, stat_name, value, max_value, cost):
          Renderiza el ítem visualmente, mostrando el nombre, la barra de progreso y el costo.
      """

    def __init__(self, x, y, width, height, index, font):
        """
           Inicializa el ítem de mejora.

           Parámetros
           ----------
           x : int
               Posición horizontal del ítem.
           y : int
               Posición vertical del ítem.
           width : int
               Ancho del ítem.
           height : int
               Alto del ítem.
           index : int
               Índice que representa la estadística que se va a mejorar.
           font : pygame.font.Font
               Fuente usada para mostrar texto.
           """

        self.rect = pygame.Rect(x, y, width, height)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        """
           Muestra el nombre y el costo de la mejora en el ítem.

           Parámetros
           ----------
           surface : pygame.Surface
               Superficie sobre la cual se renderiza el texto.
           name : str
               Nombre de la estadística a mejorar.
           cost : int
               Costo de la mejora.
           selected : bool
               Indica si el ítem está seleccionado.
           """
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR


        # Título
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        # Coste
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))
         # Dibujado
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)


    def display_bar(self, surface, value, max_value, selected):
        """
           Muestra una barra de progreso representando el valor de la estadística.

           Parámetros
           ----------
           surface : pygame.Surface
               Superficie sobre la cual se renderiza la barra.
           value : int
               Valor actual de la estadística.
           max_value : int
               Valor máximo que puede alcanzar la estadística.
           selected : bool
               Indica si el ítem está seleccionado.
           """
        # Parámetros de dibujado
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # Parámetros de la barra
        full_height = bottom[1] - top[1]
        relative_number = (value/max_value) * full_height # Si tengo 300 de máximo y 10 de stat, la posición ha de ser 1/3
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10 )
        # Dibujado
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        """
          Aplica la mejora al jugador si tiene suficiente experiencia.

          La mejora aumenta la estadística del jugador en un 20%, y el costo para mejorarla se incrementa en un 40%.

          Parámetros
          ----------
          player : Player
              Objeto que representa al jugador, sobre el cual se aplica la mejora.
          """
        stat_upgrade = list(player.stats.keys())[self.index]
        if player.exp >= player.upgrade_cost[stat_upgrade]:
            player.exp -= player.upgrade_cost[stat_upgrade]
            player.stats[stat_upgrade] *= 1.2
            player.upgrade_cost[stat_upgrade] *= 1.4

    def display(self, surface, selection_index, stat_name, value, max_value, cost):
        """
           Renderiza el ítem visualmente, mostrando el nombre, la barra de progreso y el costo.

           Parámetros
           ----------
           surface : pygame.Surface
               Superficie sobre la cual se renderiza el ítem.
           selection_index : int
               Índice del ítem actualmente seleccionado.
           stat_name : str
               Nombre de la estadística a mejorar.
           value : int
               Valor actual de la estadística.
           max_value : int
               Valor máximo que puede alcanzar la estadística.
           cost : int
               Costo de la mejora.
           """
        if self.index == selection_index:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BACKGROUND_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, stat_name, cost, self.index == selection_index)
        self.display_bar(surface, value, max_value, self.index == selection_index)






