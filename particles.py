import pygame
from support import import_folder
from random import choice

class AnimationExec:
    """
        Clase que gestiona la ejecución de animaciones y efectos de partículas en el juego.

        Esta clase controla la carga de animaciones para hechizos, ataques y efectos de muerte de enemigos. También
        proporciona métodos para crear partículas de animaciones específicas en el juego, como llamas, aura, curación, etc.

        Atributos
        ----------
        frames : dict
            Diccionario que almacena las animaciones de las partículas, categorizadas por tipo (magia, ataques, muerte de enemigos, etc.).

        Métodos
        -------
        invert_images(frames):
            Invierte las imágenes de una animación en torno al eje X.
        create_grass_particles(pos, groups):
            Crea partículas de hierba en la posición especificada.
        create_particles(attack_type, pos, groups):
            Crea partículas para un tipo de ataque específico en la posición indicada.
        """
    def __init__(self):
        """
            Inicializa la clase `AnimationExec` y carga las animaciones de partículas para diferentes efectos.

            Carga una serie de animaciones de partículas (como fuego, aura, curación, etc.) y las almacena en un diccionario
            para su uso posterior en el juego.

            """

        self.frames = {
            # Magia
            'flame': import_folder('./graphics/particles/flame/frames'),
            'aura': import_folder('./graphics/particles/aura'),
            'heal': import_folder('./graphics/particles/heal/frames'),

            # Ataques
            'claw': import_folder('./graphics/particles/claw'),
            'slash': import_folder('./graphics/particles/slash'),
            'sparkle': import_folder('./graphics/particles/sparkle'),
            'leaf_attack': import_folder('./graphics/particles/leaf_attack'),
            'thunder': import_folder('./graphics/particles/thunder'),

            # Muerte de enemigos
            'squid': import_folder('./graphics/particles/smoke_orange'),
            'raccoon': import_folder('./graphics/particles/raccoon'),
            'spirit': import_folder('./graphics/particles/nova'),
            'bamboo': import_folder('./graphics/particles/bamboo'),

            # Hojas
            'leaf': (
                import_folder('./graphics/particles/leaf1'),
                import_folder('./graphics/particles/leaf2'),
                import_folder('./graphics/particles/leaf3'),
                import_folder('./graphics/particles/leaf4'),
                import_folder('./graphics/particles/leaf5'),
                import_folder('./graphics/particles/leaf6'),
                self.invert_images(import_folder('./graphics/particles/leaf1')),
                self.invert_images(import_folder('./graphics/particles/leaf2')),
                self.invert_images(import_folder('./graphics/particles/leaf3')),
                self.invert_images(import_folder('./graphics/particles/leaf4')),
                self.invert_images(import_folder('./graphics/particles/leaf5')),
                self.invert_images(import_folder('./graphics/particles/leaf6'))
            )
        }

    def invert_images(self, frames ):
        """
            Invierte las imágenes de una animación en torno al eje X.

            Esto se utiliza para crear animaciones que se ejecuten en la dirección opuesta (por ejemplo, invertir el sentido
            de un ataque o una acción del personaje).

            Parámetros
            ----------
            frames : list
                Lista de superficies de imágenes que componen una animación.

            Retorna
            -------
            list
                Lista de superficies de imágenes invertidas en el eje X.
            """
        new_frames = []

        for frame in frames:
            inversed_frame = pygame.transform.flip(frame, True, False) # Giramos el frame en torno al eje X
            new_frames.append(inversed_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        """
           Crea partículas de hierba en la posición especificada.

           Esto se utiliza para crear efectos visuales de partículas cuando el jugador interactúa con la hierba o cuando
           se realiza un ataque relacionado con hojas o hierba.

           Parámetros
           ----------
           pos : tuple
               Coordenadas (x, y) donde se generarán las partículas.
           groups : list
               Lista de grupos de sprites donde se agregarán las partículas generadas.

           """
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, attack_type, pos, groups):
        """
          Crea partículas para un tipo de ataque específico en la posición indicada.

          Este método se usa para generar efectos visuales cuando el jugador realiza un ataque, como llamas, rayos,
          cortes, entre otros.

          Parámetros
          ----------
          attack_type : str
              Tipo de ataque que determina qué animación de partículas se debe crear (por ejemplo, 'flame', 'heal', 'claw').
          pos : tuple
              Coordenadas (x, y) donde se generarán las partículas.
          groups : list
              Lista de grupos de sprites donde se agregarán las partículas generadas.

          """
        animation_frames = self.frames[attack_type]
        ParticleEffect(pos, animation_frames, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.sprite_type = 'magic'

    def animate(self):
        """
           Actualiza el fotograma de la animación.

           Este método avanza al siguiente fotograma de la animación y se asegura de que, cuando se haya completado
           la animación, la instancia de `ParticleEffect` sea eliminada.

           """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        """
           Actualiza la animación en cada fotograma.

           Este método llama al método `animate()` para actualizar la animación de partículas y garantizar que se
           muestre correctamente en cada ciclo del juego.

           """
        self.animate()