import pygame
import sys


pygame.init()  # Inicializar Pygame

# Configuración de la pantalla
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption("RGB ADVENTURE")  # Título de la ventana

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_BLUE = (0, 50, 100)
LIGHT_BLUE = (50, 150, 200)



title_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.15))
button_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))

# Inicializar el mezclador de sonido
pygame.mixer.init()

# Fondo (cargar ambas imágenes: día y noche)
background_day = pygame.image.load("imagen_fondo_final.png").convert()
background_day = pygame.transform.scale(background_day, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_night = pygame.image.load("imagen_fondo_noche.png").convert()
background_night = pygame.transform.scale(background_night, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable para controlar el fondo actual (True para día, False para noche)
is_day = True

# Temporizador para cambiar entre día y noche (en milisegundos)
background_switch_time = 10000  # Cambiar cada 10 segundos
last_switch_time = pygame.time.get_ticks()  # Tiempo del último cambio

# Variables para la transición de desvanecimiento
fade_duration = 2000  # Duración de la transición en milisegundos (2 segundos)
fade_start_time = None  # Tiempo en que comienza la transición
fading = False  # Indica si estamos en medio de una transición
fade_alpha = 0  # Valor de transparencia (0 = completamente transparente, 255 = completamente opaco)

# Música
background_music = pygame.mixer.Sound("musica_fondo.wav")
button_sound = pygame.mixer.Sound("musica_boton.wav")
background_music.play(-1)
background_music.set_volume(0.2)

# Título del juego con sombra
title_text = title_font.render("RGB ADVENTURE", True, LIGHT_BLUE)
title_shadow = title_font.render("RGB ADVENTURE", True, BLACK)
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.15)))
title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 5, int(SCREEN_HEIGHT * 0.15 + 5)))  # Sombra desplazada

# Clase botón
class Button:
    def __init__(self, text, x, y, width, height, color, action=None):
        self.text = text
        self.base_rect = pygame.Rect(x, y, width, height)
        self.rect = self.base_rect.copy()
        self.color = color
        self.action = action
        self.hovered = False

    def draw(self, screen):
        scale = 1.2 if self.hovered else 1.0
        new_width = int(self.base_rect.width * scale)
        new_height = int(self.base_rect.height * scale)
        new_x = self.base_rect.centerx - new_width // 2
        new_y = self.base_rect.centery - new_height // 2
        self.rect = pygame.Rect(new_x, new_y, new_width, new_height)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        text_surf = button_font.render(self.text, True, WHITE)
        scaled_text = pygame.transform.scale(text_surf,
                                             (int(text_surf.get_width() * scale),
                                              int(text_surf.get_height() * scale)))
        text_rect = scaled_text.get_rect(center=self.rect.center)
        screen.blit(scaled_text, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def click(self):
        button_sound.play()
        if self.action:
            self.action()

# Clase slider volumen
class Slider:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_rect = pygame.Rect(x, y, 20, height * 2)
        self.value = 0.2
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        self.handle_rect.x = self.rect.x + (self.value * (self.rect.width - self.handle_rect.width))
        pygame.draw.rect(screen, LIGHT_BLUE, self.handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = max(self.rect.x, min(event.pos[0] - self.handle_rect.width // 2,
                                         self.rect.x + self.rect.width - self.handle_rect.width))
            self.value = (new_x - self.rect.x) / (self.rect.width - self.handle_rect.width)
            background_music.set_volume(self.value)

# Funciones de acción
def start_game():
    global current_screen
    current_screen= 'game'

def show_controls():
    global current_screen
    current_screen = "controls"

def show_credits():
    global current_screen
    current_screen = "credits"

def quit_game():
    pygame.quit()
    sys.exit()

# Botones
button_width = int(SCREEN_WIDTH * 0.25)
button_height = int(SCREEN_HEIGHT * 0.08)
button_spacing = int(SCREEN_HEIGHT * 0.03)
button_x = (SCREEN_WIDTH - button_width) // 2
button_y_start = SCREEN_HEIGHT // 3

buttons = [
    Button("Jugar", button_x, button_y_start, button_width, button_height, LIGHT_BLUE, start_game),
    Button("Controles", button_x, button_y_start + button_height + button_spacing, button_width, button_height, LIGHT_BLUE, show_controls),
    Button("Créditos", button_x, button_y_start + 2 * (button_height + button_spacing), button_width, button_height, LIGHT_BLUE, show_credits),
    Button("Salir", button_x, button_y_start + 3 * (button_height + button_spacing), button_width, button_height, LIGHT_BLUE, quit_game)
]

# Slider volumen
slider_width = int(SCREEN_WIDTH * 0.2)
slider = Slider(20, SCREEN_HEIGHT - 40, slider_width, 10)

# Pantalla actual
current_screen = "menu"

# Cargar imágenes del personaje
img_normal = pygame.image.load("imagen.png").convert_alpha()
img_izquierda = pygame.image.load("imagen1_izq.png").convert_alpha()
img_derecha = pygame.image.load("imagen1_der.png").convert_alpha()
img_girado = pygame.image.load("imagen1_giro.png").convert_alpha()
character_width, character_height = img_normal.get_size()

# Posición y salto
character_x = -character_width
ground_y = int(SCREEN_HEIGHT * 0.75)
character_y = ground_y
character_speed = 2
jumping = True
jump_counter = 0
jump_height = 120
jump_max = 150
character_phase = "normal"

# Sombra
def draw_shadow(x, y):
    shadow_width = character_width * 0.6
    shadow_height = 10
    shadow_x = x + (character_width - shadow_width) // 2
    shadow_y = ground_y + character_height - 10
    shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surface, (0, 0, 0), (0, 0, shadow_width, shadow_height))
    screen.blit(shadow_surface, (shadow_x, shadow_y))

# Bucle principal
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    # Verificar si es momento de iniciar una transición
    current_time = pygame.time.get_ticks()
    if not fading and current_time - last_switch_time >= background_switch_time:
        fading = True
        fade_start_time = current_time

    # Manejar la transición de desvanecimiento
    if fading:
        elapsed_time = current_time - fade_start_time
        fade_progress = min(elapsed_time / fade_duration, 1.0)  # Progreso de la transición (0 a 1)
        fade_alpha = int(fade_progress * 255)  # Convertir a valor de alfa (0 a 255)

        if fade_progress >= 1.0:
            fading = False  # Terminar la transición
            last_switch_time = current_time
            is_day = not is_day  # Cambiar entre día y noche al final de la transición

    # Dibujar los fondos con desvanecimiento
    if is_day:
        # Día es el fondo principal, noche se desvanece
        screen.blit(background_day, (0, 0))
        if fading:
            background_night.set_alpha(fade_alpha)  # Aumentar opacidad de la noche
            screen.blit(background_night, (0, 0))
    else:
        # Noche es el fondo principal, día se desvanece
        screen.blit(background_night, (0, 0))
        if fading:
            background_day.set_alpha(fade_alpha)  # Aumentar opacidad del día
            screen.blit(background_day, (0, 0))

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
                current_screen = "menu" if current_screen != "menu" else "exit"
                if current_screen == "exit":
                    running = False
        slider.handle_event(event)

    if current_screen == "menu":
        # Movimiento horizontal
        character_x += character_speed
        if character_x > SCREEN_WIDTH:
            character_x = -character_width
            character_y = ground_y
            jump_counter = 0
            jumping = True

        # Animación de salto
        if jumping:
            jump_counter += 1
            if jump_counter <= jump_max // 3:
                character_y -= jump_height / (jump_max // 3)
                character_phase = "subiendo"
            elif jump_counter <= 2 * (jump_max // 3):
                character_phase = "arriba"
            elif jump_counter < jump_max:
                character_y += jump_height / (jump_max // 3)
                character_phase = "bajando"
            else:
                jumping = False
                jump_counter = 0
                character_y = ground_y
                character_phase = "normal"
        else:
            if 'wait_counter' not in locals():
                wait_counter = 0
            if wait_counter < 30:  # Espera medio segundo (30 frames)
                wait_counter += 1
                character_phase = "normal"
            else:
                jumping = True
                wait_counter = 0

        # Imagen según la fase del salto
        if character_phase == "subiendo":
            character_img = img_izquierda
        elif character_phase == "arriba":
            character_img = img_girado
        elif character_phase == "bajando":
            character_img = img_derecha
        else:
            character_img = img_normal

        # Dibujar sombra y personaje
        draw_shadow(character_x, character_y)
        screen.blit(character_img, (character_x, character_y))

        # Elementos del menú
        # Dibujar la sombra del título primero
        screen.blit(title_shadow, title_shadow_rect)
        # Dibujar el título principal encima
        screen.blit(title_text, title_rect)
        for button in buttons:
            button.draw(screen)
        slider.draw(screen)
        volume_text = button_font.render("Volumen", True, WHITE)
        screen.blit(volume_text, (20, SCREEN_HEIGHT - 70))

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

    elif current_screen == 'game':
        done=True
        pygame.quit()
        sys.exit()


    pygame.display.flip()
    clock.tick(60)
