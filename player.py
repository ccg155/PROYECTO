import pygame
from support import *
from settings import *
from entity import *

class Player(Entity):

    """
    Clase que representa al jugador en el juego.

    Esta clase hereda de la clase `Entity` y gestiona las acciones del jugador, como el movimiento, ataques, magia,
    y el manejo de estadísticas y recursos. Además, controla las animaciones y la interacción del jugador con el
    entorno.

    Atributos
    ----------
    image : pygame.Surface
        Superficie de la imagen del jugador.
    rect : pygame.Rect
        Rectángulo de la posición y dimensiones del jugador.
    hitbox : pygame.Rect
        Rectángulo para la detección de colisiones del jugador.
    attacking : bool
        Indica si el jugador está en medio de un ataque.
    attack_cooldown : int
        Tiempo de espera para realizar un nuevo ataque (en milisegundos).
    attack_time : int
        Tiempo en milisegundos del último ataque realizado.
    create_attack : callable
        Función para crear el ataque del jugador.
    destroy_attack : callable
        Función para destruir el ataque cuando termina.
    weapon_index : int
        Índice del arma actual equipada.
    weapon : str
        Nombre del arma equipada.
    able_to_switch_weapon : bool
        Indica si el jugador puede cambiar de arma.
    weapon_switch_time : int
        Tiempo en milisegundos del último cambio de arma.
    switch_duration : int
        Duración en milisegundos del tiempo necesario para cambiar de arma.
    create_magic : callable
        Función para crear un hechizo del jugador.
    magic_index : int
        Índice de la magia actual equipada.
    magic : str
        Nombre de la magia equipada.
    able_to_switch_magic : bool
        Indica si el jugador puede cambiar de magia.
    magic_switch_time : int
        Tiempo en milisegundos del último cambio de magia.
    obstacle_sprites : list
        Lista de los sprites con los que el jugador puede colisionar.
    animations : dict
        Diccionario que almacena las animaciones del jugador para diferentes direcciones y acciones.
    stats : dict
        Diccionario con las estadísticas del jugador, como salud, energía, ataque, magia, y velocidad.
    max_stats : dict
        Diccionario con las estadísticas máximas del jugador.
    upgrade_cost : dict
        Diccionario con los costos de mejora de las estadísticas del jugador.
    health : int
        Salud actual del jugador.
    energy : int
        Energía actual del jugador.
    exp : int
        Experiencia del jugador.
    speed : int
        Velocidad de movimiento del jugador.
    vulnerable : bool
        Indica si el jugador es vulnerable o está en estado de invencibilidad.
    hurt_time : int
        Tiempo de daño recibido por el jugador.
    invincibility_duration : int
        Duración en milisegundos de la invencibilidad tras recibir daño.
    weapon_attack_sound : pygame.mixer.Sound
        Sonido que se reproduce al atacar con el arma.

    Métodos
    -------
    input():
        Gestiona la entrada del jugador para el movimiento, ataques, magia y cambio de armas.
    cooldowns():
        Gestiona los tiempos de recarga de ataques, cambios de arma, magia y la invulnerabilidad.
    import_player_assets():
        Carga los activos gráficos de las animaciones del jugador.
    get_status():
        Actualiza el estado del jugador según su movimiento y acciones.
    get_full_weapon_dmg():
        Calcula el daño total del arma equipada del jugador.
    animate():
        Actualiza la animación del jugador, incluyendo el parpadeo de invulnerabilidad.
    energy_regen():
        Regenera energía del jugador en función de su estadística de magia.
    get_full_magic_dmg():
        Calcula el daño total de la magia equipada del jugador.
    get_value_by_index(index):
        Obtiene el valor de una estadística del jugador por su índice.
    get_cost_by_index(index):
        Obtiene el costo de mejora de una estadística del jugador por su índice.
    update():
        Actualiza el estado del jugador, incluyendo la entrada, movimiento, animaciones, y regeneración de energía.
    """

    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        """
           Inicializa al jugador en el juego.

           Este método configura los atributos del jugador, como su imagen, hitbox, estadísticas, y las funciones relacionadas
           con los ataques y magia. Además, prepara las animaciones y gestiona el entorno de obstáculos con el que el jugador
           interactúa.

           Parámetros
           ----------
           pos : tuple
               Coordenadas iniciales (x, y) del jugador.
           groups : list
               Lista de grupos a los que pertenece el jugador (por ejemplo, sprites de enemigos, objetos).
           obstacle_sprites : list
               Lista de sprites con los que el jugador puede colisionar.
           create_attack : callable
               Función para crear un ataque del jugador.
           destroy_attack : callable
               Función para destruir el ataque del jugador cuando termina.
           create_magic : callable
               Función para crear un hechizo del jugador.
           """
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)

        # Contador de ataque
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0

        # Arma
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.able_to_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration = 400

        # Magia
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.able_to_switch_magic = True
        self.magic_switch_time = None

        self.obstacle_sprites = obstacle_sprites

        # Setup de recursos gráficos para las animaciones
        self.import_player_assets()
        self.status = 'down'

        # Estadísitcas del jugador
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.max_stats = {'health': 300, 'energy': 200, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 500
        self.speed = self.stats['speed']

        # Periodo de invencibilidad
        self.vulnerable = True
        self.hurt_time = 0
        self.invincibility_duration = 500

        # Importar sonido
        self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    def input(self):
        """
           Gestiona la entrada del jugador para el movimiento, ataques, magia y cambio de armas.

           Este método recibe las teclas pulsadas por el jugador para moverlo, atacar, usar magia o cambiar de arma y magia.

           """

        keys = pygame.key.get_pressed()

        # Input del movimiento
        if not self.attacking:
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0 # Si no hay ninguna tecla pulsada, Player no se mueve
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Input del ataque
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.weapon_attack_sound.play()
                self.create_attack()

            # Input de magia
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']

                self.create_magic(style, strength, cost)

            # Cambiar de arma
            if keys[pygame.K_c] and self.able_to_switch_weapon:
                self.able_to_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            # Cambiar magia
            if keys[pygame.K_r] and self.able_to_switch_magic:
                self.able_to_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]



    def cooldowns(self):
        """
           Gestiona los tiempos de recarga de ataques, cambios de arma, magia y la invulnerabilidad.

           Este método comprueba si han pasado los tiempos necesarios para realizar una nueva acción, como un ataque o
           cambiar de arma o magia, y permite que se realicen nuevamente.

           """
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.able_to_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration:
                self.able_to_switch_weapon = True

        if not self.able_to_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration:
                self.able_to_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.vulnerable = True

    def import_player_assets(self):
        """
           Carga los activos gráficos de las animaciones del jugador.

           Este método carga las imágenes de las animaciones del jugador desde los directorios correspondientes y las
           almacena en un diccionario.

           """
        character_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        """
          Actualiza el estado del jugador según su movimiento y acciones.

          Este método establece el estado actual del jugador (por ejemplo, 'up', 'down', 'right', 'left', etc.) en función
          de su dirección y si está atacando o no.

          """
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def get_full_weapon_dmg(self):
        """
           Calcula el daño total del arma equipada del jugador.

           Este método devuelve la suma del daño base del jugador y el daño adicional del arma equipada.

           Retorna
           -------
           int
               El daño total del arma equipada.
           """
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def animate(self):
        """
           Actualiza la animación del jugador, incluyendo el parpadeo de invulnerabilidad.

           Este método gestiona las animaciones del jugador, incluyendo el efecto de parpadeo cuando el jugador no es
           vulnerable.

           """
        super().animate()

        # Parpadeo
        if not self.vulnerable:
            alpha = self.alpha_variation()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def energy_regen(self):
        """
          Regenera energía del jugador en función de su estadística de magia.

          Este método aumenta la energía del jugador gradualmente hasta su límite máximo, dependiendo de su estadística
          de magia.

          """
        if self.energy < self.stats['energy']:
            self.energy += 0.005 * self.stats['magic']
        if self.energy >= self.stats['energy']:
            self.energy = self.stats['energy']

    def get_full_magic_dmg(self):
        """
           Calcula el daño total de la magia equipada del jugador.

           Este método devuelve la suma del daño base de magia del jugador y el daño adicional de la magia equipada.

           Retorna
           -------
           int
               El daño total de la magia equipada.
           """
        base_dmg = self.stats['magic']
        spell_dmg = magic_data[self.magic]['strength']
        actual_dmg = base_dmg + spell_dmg
        return actual_dmg

    def get_value_by_index(self, index):
        """
           Obtiene el valor de una estadística del jugador por su índice.

           Este método devuelve el valor de la estadística del jugador en la posición indicada.

           Parámetros
           ----------
           index : int
               El índice de la estadística que se desea obtener.

           Retorna
           -------
           int
               El valor de la estadística en la posición indicada.
           """
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        """
           Obtiene el coste de mejora de una estadística del jugador por su índice.

           Este método devuelve el costo de mejora de la estadística del jugador en la posición indicada.

           Parámetros
           ----------
           index : int
               El índice de la estadística cuyo costo de mejora se desea obtener.

           Retorna
           -------
           int
               El coste de mejora de la estadística en la posición indicada.
           """
        return list(self.upgrade_cost.values())[index]

    def update(self):
        """
           Actualiza el estado del jugador, incluyendo la entrada, movimiento, animaciones, y regeneración de energía.

           Este método se llama en cada ciclo del juego y actualiza la entrada del jugador, su movimiento, los tiempos de
           recarga, las animaciones y la regeneración de energía.

           """
        self.input()
        self.move(self.speed)
        self.cooldowns()
        self.get_status()
        self.animate()
        self.energy_regen()
