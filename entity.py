import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    """
        Clase base para entidades del juego (jugadores, enemigos, etc.)

        Esta clase maneja el movimiento, la colisión, la animación y la variación de la transparencia
        (alfa) de las entidades. Además, gestiona la interacción con otros sprites mediante las
        colisiones y permite la actualización visual de las entidades a través de animaciones.

        Atributos
        ---------
        frame_index : float
            Índice actual del cuadro de animación.
        animation_speed : float
            Velocidad a la que cambian los cuadros de animación.
        direction : pygame.math.Vector2
            Dirección de movimiento de la entidad.
        hitbox : pygame.Rect
            Rectángulo que define el área de colisión de la entidad.
        rect : pygame.Rect
            Rectángulo de la imagen de la entidad (para renderizarla).
        """
    def __init__(self, groups):
        """
           Inicializa una nueva instancia de la clase Entity.

           Configura el índice de fotogramas de animación, la velocidad de animación y la dirección de
           movimiento. Además, configura la entidad como un sprite y le asigna los grupos en los que
           debe ser insertada.

           Parámetros
           ----------
           groups : list
               Lista de grupos de sprites a los que la entidad debe ser añadida.
           """
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        """
           Mueve la entidad en la dirección indicada, manejando las colisiones con los obstáculos.

           Si la dirección de movimiento no es cero, la entidad se moverá en esa dirección, a una
           velocidad determinada. Durante el movimiento, se manejan las colisiones en las direcciones
           horizontal y vertical.

           Parámetros
           ----------
           speed : float
               Velocidad de movimiento de la entidad.
           """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """
           Detecta y maneja las colisiones de la entidad en una dirección específica.

           Verifica si la entidad entra en colisión con algún sprite en la dirección proporcionada.
           Si hay colisión, ajusta la posición de la entidad para evitarla.

           Parámetros
           ----------
           direction : str
               Dirección en la que se verifica la colisión. Puede ser 'horizontal' o 'vertical'.
           """

        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Nos movemos a la derecha.
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # Nos movemos a la izquierda.
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Nos movemos hacia abajo
                        self.hitbox.bottom = sprite.hitbox.top  # Ponemos la parte baja del player(Self.rect.Bottom) pegada a la parte alta del obstacle (sprite.rect.top).
                    if self.direction.y < 0:  # Nos movemos hacia arriba.
                        self.hitbox.top = sprite.hitbox.bottom
    def animate(self):
        """
         Actualiza la animación de la entidad cambiando el fotograma actual.

         Se basa en el estado de la entidad y el índice de fotograma. Si el índice supera la cantidad
         de fotogramas de la animación, se reinicia.

         """
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0


        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    @staticmethod
    def alpha_variation():
        """
            Calcula y devuelve el valor de transparencia (alfa) de la entidad basado en el tiempo.

            La transparencia alterna entre 0 y 255 utilizando una función seno en función del tiempo
            transcurrido desde el inicio del juego. Esto puede ser útil para efectos visuales.

            Retorna
            -------
            int
                255 si el valor del seno es positivo, 0 si es negativo.
            """
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0