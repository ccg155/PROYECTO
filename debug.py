import pygame
pygame.init()
font = pygame.font.Font(None,30)


def debug(info,y = 10, x = 10):
	"""
    Muestra un mensaje de depuración en la pantalla durante la ejecución del juego.

    Esta función renderiza texto sobre un rectángulo negro en la superficie principal
    de Pygame, útil para mostrar información como coordenadas, estados o variables
    durante el desarrollo del juego.

    Parámetros:
    ----------
    info : str
        Información que se desea mostrar en pantalla.
    y : int, opcional
        Posición vertical (coordenada Y) desde la esquina superior izquierda de la pantalla (por defecto 10).
    x : int, opcional
        Posición horizontal (coordenada X) desde la esquina superior izquierda de la pantalla (por defecto 10).
	"""
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'White')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(display_surface,'Black',debug_rect)
	display_surface.blit(debug_surf,debug_rect)