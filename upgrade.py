import pygame
from settings import *

class Upgrade:
    def __init__(self, player):

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
        if not self.able_to_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= self.selection_time_cooldown:
                self.able_to_move = True

    def display(self):
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
    def __init__(self, x, y, width, height, index, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
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
        stat_upgrade = list(player.stats.keys())[self.index]
        if player.exp >= player.upgrade_cost[stat_upgrade]:
            player.exp -= player.upgrade_cost[stat_upgrade]
            player.stats[stat_upgrade] *= 1.2
            player.upgrade_cost[stat_upgrade] *= 1.4

    def display(self, surface, selection_index, stat_name, value, max_value, cost):
        if self.index == selection_index:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BACKGROUND_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, stat_name, cost, self.index == selection_index)
        self.display_bar(surface, value, max_value, self.index == selection_index)






