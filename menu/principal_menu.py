import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla en modo pantalla completa
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption("Menú del Juego")

# Colores
WHITE = (255, 255, 255)  # Blanco
BLACK = (0, 0, 0)        # Negro
GRAY = (100, 100, 100)   # Gris
DARK_BLUE = (0, 50, 100) # Azul oscuro
LIGHT_BLUE = (50, 150, 200) # Azul claro

# Fuentes (ajustadas según el tamaño de la pantalla)
title_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.1))  # Fuente para el título
button_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))  # Fuente para los botones

# Inicializar el mezclador de sonido (necesario para reproducir audio)
pygame.mixer.init()

# Cargar música de fondo y sonido del botón
background_music = pygame.mixer.Sound("musica_fondo.wav")  # Cambia esta ruta
button_sound = pygame.mixer.Sound("musica_boton.wav")  # Cambia esta ruta

# Reproducir la música de fondo en bucle (-1 significa que se repite para siempre)
background_music.play(-1)

# Clase para los botones
class Button:
    def __init__(self, text, x, y, width, height, color, action=None):
        self.text = text
        self.base_rect = pygame.Rect(x, y, width, height)  # Rectángulo base (tamaño normal)
        self.rect = self.base_rect.copy()  # Rectángulo actual (puede cambiar)
        self.color = color
        self.action = action
        self.hovered = False  # Indica si el cursor está encima

    def draw(self, screen):
        # Escala: aumenta a 1.2x si el cursor está encima, vuelve a 1.0x si no
        scale = 1.2 if self.hovered else 1.0

        # Ajustar el tamaño del botón según la escala
        new_width = int(self.base_rect.width * scale)
        new_height = int(self.base_rect.height * scale)
        new_x = self.base_rect.centerx - new_width // 2
        new_y = self.base_rect.centery - new_height // 2
        self.rect = pygame.Rect(new_x, new_y, new_width, new_height)

        # Dibujar el botón con bordes redondeados
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)

        # Escalar el texto del botón
        text_surf = button_font.render(self.text, True, WHITE)
        scaled_text = pygame.transform.scale(text_surf,
                                            (int(text_surf.get_width() * scale),
                                             int(text_surf.get_height() * scale)))
        text_rect = scaled_text.get_rect(center=self.rect.center)
        screen.blit(scaled_text, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)  # Detecta si el cursor está encima

    def click(self):
        # Reproducir el sonido del botón al hacer clic
        button_sound.play()
        if self.action:
            self.action()  # Ejecuta la acción del botón

# Funciones para las acciones de los botones
def start_game():
    print("Iniciando el juego...")

def show_controls():
    global current_screen
    current_screen = "controls"

def show_credits():
    global current_screen
    current_screen = "credits"

def quit_game():
    pygame.quit()
    sys.exit()

# Dimensiones y posiciones de los botones
button_width = int(SCREEN_WIDTH * 0.25)
button_height = int(SCREEN_HEIGHT * 0.08)
button_spacing = int(SCREEN_HEIGHT * 0.03)
button_x = (SCREEN_WIDTH - button_width) // 2
button_y_start = SCREEN_HEIGHT // 3

# Crear los botones
buttons = [
    Button("Jugar", button_x, button_y_start, button_width, button_height, LIGHT_BLUE, start_game),
    Button("Controles", button_x, button_y_start + button_height + button_spacing, button_width, button_height, LIGHT_BLUE, show_controls),
    Button("Créditos", button_x, button_y_start + 2 * (button_height + button_spacing), button_width, button_height, LIGHT_BLUE, show_credits),
    Button("Salir", button_x, button_y_start + 3 * (button_height + button_spacing), button_width, button_height, LIGHT_BLUE, quit_game)
]

# Pantalla actual
current_screen = "menu"

# Título del juego
title_text = title_font.render("Mi Juego", True, WHITE)
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.15)))

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)  # Limpiar la pantalla con fondo negro
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    button.click()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_screen != "menu":
                    current_screen = "menu"
                else:
                    running = False

    if current_screen == "menu":
        screen.blit(title_text, title_rect)
        for button in buttons:
            button.draw(screen)
    elif current_screen == "controls":
        controls_text = button_font.render("Controles: W,A,S,D (prueba)", True, WHITE)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT // 2))
        back_text = button_font.render("Presiona ESC para volver", True, WHITE)
        screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    elif current_screen == "credits":
        credits_text = button_font.render("Créditos: Equipo TBD", True, WHITE)
        screen.blit(credits_text, (SCREEN_WIDTH // 2 - credits_text.get_width() // 2, SCREEN_HEIGHT // 2))
        back_text = button_font.render("Presiona ESC para volver", True, WHITE)
        screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()