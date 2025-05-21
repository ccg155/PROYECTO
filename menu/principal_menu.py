import pygame
import sys


class Menu:
    """
    Clase que representa el menú principal del juego RGB Adventure.

    Maneja la interfaz de usuario del menú, incluyendo botones, controles, créditos y animaciones.
    Permite al usuario navegar entre diferentes pantallas (menú, controles, créditos) y ajustar
    el volumen de la música de fondo.
    """

    def __init__(self):
        """
        Inicializa el menú principal, configurando Pygame, la pantalla, colores, fuentes,
        fondos, música y elementos del menú como botones y el personaje animado.
        """
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()
        pygame.display.set_caption("RGB ADVENTURE")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (100, 100, 100)
        self.DARK_BLUE = (0, 50, 100)
        self.LIGHT_BLUE = (50, 150, 200)

        self.title_font = pygame.font.Font(None, int(self.SCREEN_HEIGHT * 0.15))
        self.button_font = pygame.font.Font(None, int(self.SCREEN_HEIGHT * 0.05))

        # Cargar fondos día/noche
        self.background_day = pygame.transform.scale(pygame.image.load("menu/imagen_fondo_final.png").convert(),
                                                     (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background_night = pygame.transform.scale(pygame.image.load("menu/imagen_fondo_noche.png").convert(),
                                                       (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.is_day = True
        self.background_switch_time = 10000
        self.last_switch_time = pygame.time.get_ticks()
        self.fade_duration = 2000
        self.fade_start_time = None
        self.fading = False
        self.fade_alpha = 0

        # Música
        self.background_music = pygame.mixer.Sound("menu/musica_fondo.wav")
        self.button_sound = pygame.mixer.Sound("menu/musica_boton.wav")
        self.background_music.play(-1)
        self.background_music.set_volume(0.2)

        # Título
        self.title_text = self.title_font.render("RGB ADVENTURE", True, self.LIGHT_BLUE)
        self.title_shadow = self.title_font.render("RGB ADVENTURE", True, self.BLACK)
        self.title_rect = self.title_text.get_rect(center=(self.SCREEN_WIDTH // 2, int(self.SCREEN_HEIGHT * 0.15)))
        self.title_shadow_rect = self.title_shadow.get_rect(
            center=(self.SCREEN_WIDTH // 2 + 5, int(self.SCREEN_HEIGHT * 0.15 + 5)))

        self.button_width = int(self.SCREEN_WIDTH * 0.25)
        self.button_height = int(self.SCREEN_HEIGHT * 0.08)
        self.button_spacing = int(self.SCREEN_HEIGHT * 0.03)
        self.button_x = (self.SCREEN_WIDTH - self.button_width) // 2
        self.button_y_start = self.SCREEN_HEIGHT // 3

        self.current_screen = "menu"

        # Personaje animado
        self.img_normal = pygame.image.load("menu/imagen.png").convert_alpha()
        self.img_izquierda = pygame.image.load("menu/imagen1_izq.png").convert_alpha()
        self.img_derecha = pygame.image.load("menu/imagen1_der.png").convert_alpha()
        self.img_girado = pygame.image.load("menu/imagen1_giro.png").convert_alpha()
        self.character_width, self.character_height = self.img_normal.get_size()
        self.character_x = -self.character_width
        self.ground_y = int(self.SCREEN_HEIGHT * 0.75)
        self.character_y = self.ground_y
        self.character_speed = 2
        self.jumping = True
        self.jump_counter = 0
        self.jump_height = 120
        self.jump_max = 150
        self.character_phase = "normal"
        self.wait_counter = 0

        self.Slider = self._create_slider_class()
        self.Button = self._create_button_class()

        self.slider = self.Slider(20, self.SCREEN_HEIGHT - 40, int(self.SCREEN_WIDTH * 0.2), 10)
        self.buttons = [
            self.Button("Jugar", self.button_x, self.button_y_start, self.button_width, self.button_height,
                        self.LIGHT_BLUE, self.start_game),
            self.Button("Controles", self.button_x, self.button_y_start + self.button_height + self.button_spacing,
                        self.button_width, self.button_height, self.LIGHT_BLUE, self.show_controls),
            self.Button("Créditos", self.button_x, self.button_y_start + 2 * (self.button_height + self.button_spacing),
                        self.button_width, self.button_height, self.LIGHT_BLUE, self.show_credits),
            self.Button("Salir", self.button_x, self.button_y_start + 3 * (self.button_height + self.button_spacing),
                        self.button_width, self.button_height, self.LIGHT_BLUE, self.quit_game)
        ]

    def _create_button_class(self):
        """
        Crea una clase interna Button para manejar los botones del menú.

        Returns:
            Button: Clase Button para manejar botones interactivos.
        """
        menu = self

        class Button:
            """
            Clase para manejar botones interactivos en el menú.

            Attributes:
                text (str): Texto del botón.
                base_rect (pygame.Rect): Rectángulo base del botón.
                rect (pygame.Rect): Rectángulo ajustado para efectos de hover.
                color (tuple): Color del botón.
                action (callable): Función a ejecutar al hacer clic.
                hovered (bool): Indica si el mouse está sobre el botón.
            """

            def __init__(self, text, x, y, width, height, color, action=None):
                self.text = text
                self.base_rect = pygame.Rect(x, y, width, height)
                self.rect = self.base_rect.copy()
                self.color = color
                self.action = action
                self.hovered = False

            def draw(self, screen):
                """
                Dibuja el botón en la pantalla con un efecto de escala al pasar el mouse.

                Args:
                    screen (pygame.Surface): Superficie donde dibujar el botón.
                """
                scale = 1.2 if self.hovered else 1.0
                new_rect = self.base_rect.inflate(scale * self.base_rect.width - self.base_rect.width,
                                                  scale * self.base_rect.height - self.base_rect.height)
                self.rect = new_rect
                pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
                text_surf = menu.button_font.render(self.text, True, menu.WHITE)
                scaled_text = pygame.transform.scale(text_surf, (
                int(text_surf.get_width() * scale), int(text_surf.get_height() * scale)))
                text_rect = scaled_text.get_rect(center=self.rect.center)
                screen.blit(scaled_text, text_rect)

            def check_hover(self, pos):
                """
                Verifica si el mouse está sobre el botón.

                Args:
                    pos (tuple): Posición del mouse (x, y).
                """
                self.hovered = self.rect.collidepoint(pos)

            def click(self):
                """
                Maneja el evento de clic en el botón, ejecutando la acción asociada.

                Returns:
                    Any: Resultado de la acción (si existe).
                """
                menu.button_sound.play()
                if self.action:
                    return self.action()
                return None

        return Button

    def _create_slider_class(self):
        """
        Crea una clase interna Slider para manejar el control de volumen.

        Returns:
            Slider: Clase Slider para manejar el control de volumen.
        """
        menu = self

        class Slider:
            """
            Clase para manejar un control deslizante de volumen en el menú.

            Attributes:
                rect (pygame.Rect): Rectángulo del slider.
                handle_rect (pygame.Rect): Rectángulo del manejador del slider.
                value (float): Valor del volumen (0.0 a 1.0).
                dragging (bool): Indica si el slider está siendo arrastrado.
            """

            def __init__(self, x, y, width, height):
                self.rect = pygame.Rect(x, y, width, height)
                self.handle_rect = pygame.Rect(x, y, 20, height * 2)
                self.value = 0.2
                self.dragging = False

            def draw(self, screen):
                """
                Dibuja el slider en la pantalla.

                Args:
                    screen (pygame.Surface): Superficie donde dibujar el slider.
                """
                pygame.draw.rect(screen, menu.GRAY, self.rect)
                self.handle_rect.x = self.rect.x + (self.value * (self.rect.width - self.handle_rect.width))
                pygame.draw.rect(screen, menu.LIGHT_BLUE, self.handle_rect)

            def handle_event(self, event):
                """
                Maneja los eventos del mouse para ajustar el volumen.

                Args:
                    event (pygame.event.Event): Evento de Pygame.
                """
                if event.type == pygame.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
                    self.dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                elif event.type == pygame.MOUSEMOTION and self.dragging:
                    new_x = max(self.rect.x, min(event.pos[0] - self.handle_rect.width // 2,
                                                 self.rect.x + self.rect.width - self.handle_rect.width))
                    self.value = (new_x - self.rect.x) / (self.rect.width - self.handle_rect.width)
                    menu.background_music.set_volume(self.value)

        return Slider

    def draw_shadow(self, x, y):
        """
        Dibuja una sombra elíptica debajo del personaje animado.

        Args:
            x (int): Posición x del personaje.
            y (int): Posición y del personaje.
        """
        shadow_surface = pygame.Surface((self.character_width * 0.6, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0), shadow_surface.get_rect())
        self.screen.blit(shadow_surface, (x + (self.character_width * 0.2), self.ground_y + self.character_height - 10))

    def start_game(self):
        """
        Inicia el juego, deteniendo la música de fondo.

        Returns:
            str: Identificador para iniciar el juego ('game').
        """
        return 'game'

    def show_controls(self):
        """
        Cambia la pantalla actual a la pantalla de controles.
        """
        self.current_screen = "controls"

    def show_credits(self):
        """
        Cambia la pantalla actual a la pantalla de créditos.
        """
        self.current_screen = "credits"

    def quit_game(self):
        """
        Cierra Pygame y termina el programa.
        """
        pygame.quit()
        sys.exit()

    def run(self):
        """
        Ejecuta el bucle principal del menú, manejando eventos, animaciones y transiciones.

        Returns:
            str: Resultado del menú ('game' si se inicia el juego).
        """
        clock = pygame.time.Clock()
        while True:
            self.screen.fill(self.BLACK)
            current_time = pygame.time.get_ticks()

            if not self.fading and current_time - self.last_switch_time >= self.background_switch_time:
                self.fading = True
                self.fade_start_time = current_time

            if self.fading:
                elapsed_time = current_time - self.fade_start_time
                fade_progress = min(elapsed_time / self.fade_duration, 1.0)
                self.fade_alpha = int(fade_progress * 255)
                if fade_progress >= 1.0:
                    self.fading = False
                    self.last_switch_time = current_time
                    self.is_day = not self.is_day

            # Dibujar fondo
            if self.is_day:
                self.screen.blit(self.background_day, (0, 0))
                if self.fading:
                    self.background_night.set_alpha(self.fade_alpha)
                    self.screen.blit(self.background_night, (0, 0))
            else:
                self.screen.blit(self.background_night, (0, 0))
                if self.fading:
                    self.background_day.set_alpha(self.fade_alpha)
                    self.screen.blit(self.background_day, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        button.check_hover(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            result = button.click()
                            if result == 'game':
                                self.background_music.stop()
                                return 'game'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.current_screen = "menu" if self.current_screen != "menu" else "exit"
                    if self.current_screen == "exit":
                        self.quit_game()
                self.slider.handle_event(event)

            if self.current_screen == "menu":
                self.character_x += self.character_speed
                if self.character_x > self.SCREEN_WIDTH:
                    self.character_x = -self.character_width
                    self.character_y = self.ground_y
                    self.jump_counter = 0
                    self.jumping = True

                if self.jumping:
                    self.jump_counter += 1
                    if self.jump_counter <= self.jump_max // 3:
                        self.character_y -= self.jump_height / (self.jump_max // 3)
                        self.character_phase = "subiendo"
                    elif self.jump_counter <= 2 * (self.jump_max // 3):
                        self.character_phase = "arriba"
                    elif self.jump_counter < self.jump_max:
                        self.character_y += self.jump_height / (self.jump_max // 3)
                        self.character_phase = "bajando"
                    else:
                        self.jumping = False
                        self.jump_counter = 0
                        self.character_y = self.ground_y
                        self.character_phase = "normal"
                else:
                    if self.wait_counter < 30:
                        self.wait_counter += 1
                        self.character_phase = "normal"
                    else:
                        self.jumping = True
                        self.wait_counter = 0

                if self.character_phase == "subiendo":
                    img = self.img_izquierda
                elif self.character_phase == "arriba":
                    img = self.img_girado
                elif self.character_phase == "bajando":
                    img = self.img_derecha
                else:
                    img = self.img_normal

                self.draw_shadow(self.character_x, self.character_y)
                self.screen.blit(img, (self.character_x, self.character_y))
                self.screen.blit(self.title_shadow, self.title_shadow_rect)
                self.screen.blit(self.title_text, self.title_rect)
                for button in self.buttons:
                    button.draw(self.screen)
                self.slider.draw(self.screen)
                volume_text = self.button_font.render("Volumen", True, self.WHITE)
                self.screen.blit(volume_text, (20, self.SCREEN_HEIGHT - 70))

            elif self.current_screen == "controls":
                # Lista de controles con descripción
                controls_texts = [
                    "W: Mover arriba",
                    "S: Mover abajo",
                    "A: Mover izquierda",
                    "D: Mover derecha",
                    "ESPACIO: Saltar",
                    "R: Cambio de habilidad",
                    "C: Cambio de arma",
                    "ESC: Menu de estadísticas"
                ]
                # Calcular la posición inicial para centrar los controles verticalmente
                total_height = len(controls_texts) * 40  # 40 píxeles de separación entre líneas
                start_y = (self.SCREEN_HEIGHT - total_height) // 2
                # Dibujar cada línea de control
                for i, control_text in enumerate(controls_texts):
                    text = self.button_font.render(control_text, True, self.BLACK)
                    self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, start_y + i * 40))
                # Texto de "Volver"
                back = self.button_font.render("Presiona ESC para volver", True, self.BLACK)
                self.screen.blit(back, (
                self.SCREEN_WIDTH // 2 - back.get_width() // 2, start_y + len(controls_texts) * 40 + 50))

            elif self.current_screen == "credits":
                # Lista de nombres para los créditos
                credits_names = ["Carlos Crespo Gutiérrez", "Xavier Fuentes Navarro", "Alba García Calvete", "Victoria Pérez Bernabeu", "Hugo López de la Rosa"]
                # Calcular la posición inicial para centrar los nombres verticalmente
                total_height = len(credits_names) * 40  # 40 píxeles de separación entre líneas
                start_y = (self.SCREEN_HEIGHT - total_height) // 2
                # Dibujar cada nombre
                for i, name in enumerate(credits_names):
                    text = self.button_font.render(name, True, self.BLACK)
                    self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, start_y + i * 40))
                # Texto de "Volver"
                back = self.button_font.render("Presiona ESC para volver", True, self.BLACK)
                self.screen.blit(back, (
                self.SCREEN_WIDTH // 2 - back.get_width() // 2, start_y + len(credits_names) * 40 + 50))

            pygame.display.flip()
            clock.tick(60)


# Para probar el menú directamente:
if __name__ == "__main__":
    """
    Punto de entrada para probar el menú directamente.
    """
    menu = Menu()
    result = menu.run()
    print("Resultado:", result)