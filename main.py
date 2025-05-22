from level import *
from player import *
from menu.principal_menu import *
from database import DataBase

class Game:
    """
       Clase principal del juego que inicializa y ejecuta el bucle principal de la aplicación.

       Métodos
       -------
       __init__():
           Inicializa la pantalla, el reloj, el nivel del juego y reproduce la música de fondo.

       run():
           Ejecuta el bucle principal del juego, procesando eventos, actualizando el nivel y refrescando la pantalla.
    """
    def __init__(self):
        """
              Inicializa la instancia del juego:
              - Configura la ventana principal de pygame.
              - Establece el título del juego.
              - Crea un objeto Level para manejar la lógica del nivel.
              - Reproduce música de fondo en bucle.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('FlowerPower Hardcore')
        self.clock = pygame.time.Clock()
        self.level = Level(self.database)  # Se llama a la función level, por lo que se ejecuta su constructor
        self.menu = Menu()   # Inicializamos el menú
        self.database = DataBase('database.py')



    def run(self):
        """
               Ejecuta el bucle principal del juego:
               - Muestra el menú al inicio y espera el resultado.
               - Si el resultado es 'game', comienza el bucle del juego.
               - Captura y gestiona eventos del teclado y del sistema.
               - Llama a la función de ejecución del nivel.
               - Actualiza la pantalla a la velocidad de fotogramas definida.
        """
        result = self.menu.run()  # Mostramos el menú y obtenemos el resultado
        if result == 'game':
            # Sonido
            main_sound = pygame.mixer.Sound('audio/main.ogg')
            main_sound.play(loops=-1)
            main_sound.set_volume(0.4)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.level.save_game()
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.level.toggle_menu()
                self.screen.fill(WATER_COLOR)
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()