import pygame
from settings import *

class UI:
    def __init__(self):

        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Setup de las barras
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.enery_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Convertir diccionario de armas en lista de las rutas de sus imágenes
        self.weapon_graphics = []
        for row in weapon_data.values():
            path = row['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []
        for row in magic_data.values():
            path  = row['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current_amount, max_amount, bg_rect, color):
        # Dibujar fondo de la barra
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, bg_rect)

        # Convertir estadística a píxel
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Dibujar la barra
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, text_rect.inflate(10,10))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, text_rect.inflate(10,10), 3)

    def selection_box(self, x, y, is_switching):
        bg_rect = pygame.Rect(x, y, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, bg_rect)
        if is_switching:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, is_switching):
        bg_rect = self.selection_box(10, 630, is_switching)
        weapon_img = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_img.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_img, weapon_rect)

    def magic_overlay(self, magic_index, is_switching):
        bg_rect = self.selection_box(80, 620, is_switching)
        magic_img = self.magic_graphics[magic_index]
        magic_rect = magic_img.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_img, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'],self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'],self.enery_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, not player.able_to_switch_weapon)
        self.magic_overlay(player.magic_index, not player.able_to_switch_magic)
       # self.selection_box(80, 635) # Magia

