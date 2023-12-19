import pygame
import random


class Character(object):
    """class Character - main object

    :type speed: int
    :type current_animation_left: int
    :type current_animation_right: int
    :type current_animation_down: int
    :type current_animation_up: int
    :type current_animation_default: str
    :type current_animation_type: str
    :type health: int
    :type weapon_bool: bool
    :type weapon: class
    :type width: int
    :type height: int
    :type hb_x: int
    :type hb_y: int
    :type ishit: bool
    :type killing_ghosts: int

    """
    speed = 16
    current_animation_left = 0
    current_animation_right = 0
    current_animation_down = 0
    current_animation_up = 0
    current_animation_default = 'left'
    current_animation_type = 'left'
    health = 3
    weapon_bool = False
    weapon = None
    width = 100
    height = 150
    hb_x = 150
    hb_y = 90
    ishit = False
    killing_ghosts = 0

    def __init__(self, animations_left: list, animations_right: list, animations_down: list, animations_up: list,
                 animations_default: dict,
                 pos_x: int, pos_y: int, heart_im):
        """

        :param animations_left: list[pygame.image()...]
        :param animations_right: list[pygame.image()...]
        :param animations_down: list[pygame.image()...]
        :param animations_up: list[pygame.image()...]
        :param animations_default: dict
        :param pos_x: int
        :param pos_y: int
        :param heart_im: pygame.image()
        """
        self.animations_default = animations_default
        self.animations_left = animations_left
        self.animations_up = animations_up
        self.animations_right = animations_right
        self.animations_down = animations_down

        self.animations_left_count = len(animations_left)
        self.animations_up_count = len(animations_up)
        self.animations_right_count = len(animations_right)
        self.animations_down_count = len(animations_down)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.hitbox_x = pos_x + self.hb_x
        self.hitbox_y = pos_y + self.hb_y
        self.heart_im = heart_im

    def animation_set_type(self, animation_type: str):
        """set self.current_animation_type to 'left', 'right', 'top' or 'down'

        :param animation_type: str
        :return:
        """
        self.current_animation_type = animation_type

    def animation_change_animation_number(self):
        """changes self.current_animation_number

        :return:
        """
        match self.current_animation_type:
            case 'left':
                self.current_animation_left = (self.current_animation_left + 1) % self.animations_left_count
            case 'right':
                self.current_animation_right = (self.current_animation_right + 1) % self.animations_right_count
            case 'down':
                self.current_animation_down = (self.current_animation_down + 1) % self.animations_down_count
            case 'top':
                self.current_animation_up = (self.current_animation_up + 1) % self.animations_up_count

    def animation_set_default(self, default):
        """

        :param default:
        :return:
        """
        self.current_animation_default = default

    def hitbox_movement(self):
        """move the character's hitbox

        :return:
        """
        self.hitbox_x = self.pos_x + self.hb_x
        self.hitbox_y = self.pos_y + self.hb_y

    def weapon_hit(self, weapon, game_map):
        """make hit from weapon to ghost

        :param weapon:
        :param game_map:
        :return:
        """
        rect1 = pygame.Rect(weapon.pos_x, weapon.pos_y, weapon.width, weapon.height)
        for ghost in game_map.ghosts:
            rect2 = pygame.Rect(ghost.hitbox_x, ghost.hitbox_y, ghost.width, ghost.height)
            if pygame.Rect.colliderect(rect1, rect2):
                ghost.health -= 1
                if ghost.health == 0:
                    if ghost.boss:
                        if self.health < 5:
                            self.health += 1
                    self.killing_ghosts += 1
                    game_map.ghosts.remove(ghost)
                    game_map.ghosts_count -= 1

    def status(self, screen):
        """show character's health

        :param screen:
        :return:
        """
        status_x = 50
        status_y = 50
        for i in range(self.health):
            screen.blit(self.heart_im, (status_x, status_y))
            status_x += 50

    def get_weapon(self, weapon):
        """allow character make hits

        :param weapon:
        :return:
        """
        self.weapon_bool = True
        self.weapon = weapon

    def movement(self, screen, game_map):
        """make character's movement and draw it

        :param screen:
        :param game_map:
        :return:
        """
        keys = pygame.key.get_pressed()
        self.status(screen)
        if keys[pygame.K_a] and self.hitbox_x >= game_map.block_down_x:
            self.pos_x -= self.speed
            self.hitbox_movement()
            self.animation_set_type('left')
            self.animation_set_default('left')
        elif keys[pygame.K_d] and self.hitbox_x <= game_map.block_top_x:
            self.pos_x += self.speed
            self.hitbox_movement()
            self.animation_set_type('right')
            self.animation_set_default('right')
        elif keys[pygame.K_w] and self.hitbox_y >= game_map.block_down_y:
            self.pos_y -= self.speed
            self.hitbox_movement()
            self.animation_set_type('top')
            self.animation_set_default('top')
        elif keys[pygame.K_s] and self.hitbox_y <= game_map.block_top_y:
            self.pos_y += self.speed
            self.hitbox_movement()
            self.animation_set_type('down')
            self.animation_set_default('down')
        else:
            self.animation_set_type('default')

        if keys[pygame.K_f] and not self.ishit and self.weapon_bool:
            self.ishit = True
            self.weapon.current_direction = self.current_animation_default

        if self.ishit and self.weapon_bool:
            self.weapon.animations_sword(self.hitbox_x, self.hitbox_y, screen)
            self.weapon_hit(self.weapon, game_map)

            if self.weapon.hit_stop():
                self.ishit = False

        match self.current_animation_type:
            case 'left':
                screen.blit(self.animations_left[self.current_animation_left],
                            (self.pos_x, self.pos_y))
                self.animation_change_animation_number()
            case 'right':
                screen.blit(self.animations_right[self.current_animation_right],
                            (self.pos_x, self.pos_y))
                self.animation_change_animation_number()
            case 'top':
                screen.blit(self.animations_up[self.current_animation_up],
                            (self.pos_x, self.pos_y))
                self.animation_change_animation_number()
            case 'down':
                screen.blit(self.animations_down[self.current_animation_down],
                            (self.pos_x, self.pos_y))
                self.animation_change_animation_number()
            case 'default':
                screen.blit(self.animations_default[self.current_animation_default],
                            (self.pos_x, self.pos_y))


class Game_map(object):
    """Create game map

    :type current_map: int
    :type block_top_y: int
    :type block_top_x: int
    :type block_down_y: int
    :type block_down_x: int
    :type ghosts_count: int
    :type ghosts_at_map: int
    :type ghosts_spawn_x_min: int
    :type ghosts_spawn_x_max: int
    :type ghosts_spawn_y_min: int
    :type ghosts_spawn_y_max: int
    """
    current_map = 1
    block_top_y = 1080
    block_top_x = 1920
    block_down_y = 0
    block_down_x = 0
    ghosts_count = 0
    ghosts_at_map = 0
    ghosts_spawn_x_min = 900
    ghosts_spawn_x_max = 1400
    ghosts_spawn_y_min = 500
    ghosts_spawn_y_max = 700
    ghosts_spawn_position = (
        random.randint(ghosts_spawn_x_min, ghosts_spawn_x_max), random.randint(ghosts_spawn_y_min, ghosts_spawn_y_max)
    )
    ghosts = []
    weapons = []

    def __init__(self, maps: list, ghost_class, ghost_im, ghost_boss):
        """initialize map

        :param maps: list[pygame.image()..]
        :param ghost_class: class
        :param ghost_im: pygame.image()
        :param ghost_boss: pygame.image()
        """
        self.maps = maps
        self.ghost_class = ghost_class
        self.ghost_im = ghost_im
        self.ghost_boss = ghost_boss

    def draw_map1(self, screen):
        """draw first map with their properties

        :param screen:
        :return:
        """
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1920, 1080))
        screen.blit(self.maps[0], (0, 0))
        for weapon in self.weapons:
            weapon[0].animations_sword(weapon[1], weapon[2], screen)

    def draw_map2(self, screen):
        """draw second map with their properties

        :param screen:
        :return:
        """
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1920, 1080))
        screen.blit(self.maps[1], (0, 0))

    def ghosts_spawn(self, hero):
        """spawn ghost not too close to hero

        :param hero:
        :return:
        """
        self.ghosts_spawn_position = (random.randint(self.ghosts_spawn_x_min, self.ghosts_spawn_x_max),
                                      random.randint(self.ghosts_spawn_y_min, self.ghosts_spawn_y_max))
        rect1 = pygame.Rect(self.ghosts_spawn_position[0], self.ghosts_spawn_position[1], 150, 200)
        rect2 = pygame.Rect(hero.hitbox_x, hero.hitbox_y, hero.width, hero.height)
        while pygame.Rect.colliderect(rect1, rect2):
            self.ghosts_spawn_position = (random.randint(self.ghosts_spawn_x_min, self.ghosts_spawn_x_max),
                                          random.randint(self.ghosts_spawn_y_min, self.ghosts_spawn_y_max))
            rect1 = pygame.Rect(self.ghosts_spawn_position[0], self.ghosts_spawn_position[1], 200, 250)
            rect2 = pygame.Rect(hero.hitbox_x, hero.hitbox_y, hero.width, hero.height)

        self.ghosts.append(Ghost(self.ghost_im, *self.ghosts_spawn_position))
        self.ghosts_count += 1

    def boss_spawn(self, hero):
        """spawn boss not too close to hero

        :param hero:
        :return:
        """
        self.ghosts_spawn_position = (random.randint(self.ghosts_spawn_x_min, self.ghosts_spawn_x_max),
                                      random.randint(self.ghosts_spawn_y_min, self.ghosts_spawn_y_max))
        rect1 = pygame.Rect(self.ghosts_spawn_position[0], self.ghosts_spawn_position[1], 150, 200)
        rect2 = pygame.Rect(hero.hitbox_x, hero.hitbox_y, hero.width, hero.height)
        while pygame.Rect.colliderect(rect1, rect2):
            self.ghosts_spawn_position = (random.randint(self.ghosts_spawn_x_min, self.ghosts_spawn_x_max),
                                          random.randint(self.ghosts_spawn_y_min, self.ghosts_spawn_y_max))
            rect1 = pygame.Rect(self.ghosts_spawn_position[0], self.ghosts_spawn_position[1], 150, 200)
            rect2 = pygame.Rect(hero.hitbox_x, hero.hitbox_y, hero.width, hero.height)

        self.ghosts.append(Ghost(self.ghost_boss, *self.ghosts_spawn_position))
        self.ghosts_count += 1
        self.ghosts[-1].health = 15
        self.ghosts[-1].boss = True

    def sword_spawn(self, sword, pos_x, pos_y):
        """spawn sword at pos_x, pos_y

        :param sword:
        :param pos_x:
        :param pos_y:
        :return:
        """
        self.weapons.append((sword, pos_x, pos_y))

    def sword_take(self, hero):
        """allow hero takes the sword

        :param hero:
        :return:
        """
        sword = self.weapons[0]
        rect1 = pygame.Rect(hero.hitbox_x, hero.hitbox_y, hero.width, hero.height)
        rect2 = pygame.Rect(sword[0].pos_x, sword[0].pos_y, sword[0].width, sword[0].height)
        if pygame.Rect.colliderect(rect1, rect2):
            hero.get_weapon(sword[0])
            self.weapons.remove(sword)

    def change_ghost_spawn_position(self):
        """change ghost spawn position depend on game_map

        :return:
        """
        match self.current_map:
            case 1:
                self.ghosts_spawn_position = (random.randint(700, 1200), 1200)
            case 2:
                self.ghosts_spawn_position = (random.randint(700, 1200), 1200)

    def change_map_borders(self):
        """change map borders depend on game_map

        :return:
        """
        match self.current_map:
            case 1:
                self.block_top_y = 950
                self.block_top_x = 1500
                self.block_down_y = 50
                self.block_down_x = 350
            case 2:
                self.block_top_y = 950
                self.block_top_x = 950
                self.block_down_y = 50
                self.block_down_x = 700


class Ghost(object):
    """class Ghost

    :type speed: int
    :type width: int
    :type height: int
    :type health: int
    :type boss: bool
    """
    speed = 1
    width = 50
    height = 100
    health = 1
    boss = False

    def __init__(self, ghost_image, pos_x, pos_y):
        """Initialize Ghost

        :param ghost_image:
        :param pos_x:
        :param pos_y:
        """
        self.ghost_image = ghost_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.hitbox_x = pos_x + 30
        self.hitbox_y = pos_y + 10

    def hitbox_movement(self):
        """move the ghost's hitbox

        :return:
        """
        self.hitbox_x = self.pos_x + 25
        self.hitbox_y = self.pos_y + 10

    def movement(self, target_x, target_y, screen):
        """move ghost closly to hero and draw it

        :param target_x:
        :param target_y:
        :param screen:
        :return:
        """
        if self.pos_y > target_y:
            self.pos_y -= self.speed
            self.hitbox_movement()
        else:
            self.pos_y += self.speed
            self.hitbox_movement()
        if self.pos_x > target_x:
            self.pos_x -= self.speed
            self.hitbox_movement()
        else:
            self.pos_x += self.speed
            self.hitbox_movement()
        screen.blit(self.ghost_image, (self.pos_x, self.pos_y))

    def collide_w_hero(self, hero):
        """check the ghost's collide with hero

        :param hero:
        :rtype: bool
        """
        rect1 = pygame.Rect(self.hitbox_x, self.hitbox_y, self.width, self.height)
        rect2 = pygame.Rect(hero.hitbox_x, hero.hitbox_y, hero.width, hero.height)
        return pygame.Rect.colliderect(rect1, rect2)


class Sword:
    """class Sword

    :type current_direction: str
    :type current_animation: int
    :type width: int
    :type height: int
    :type pos_x: int
    :type pos_y: int
    """
    current_direction = 'default'
    current_animation = 0
    width = 200
    height = 130
    pos_x = 0
    pos_y = 0

    def __init__(self, sword_default, sword_anim_top: list, sword_anim_left: list, sword_anim_right: list,
                 sword_anim_down: list):
        """Initializate sword

        :param sword_default:
        :param sword_anim_top:
        :param sword_anim_left:
        :param sword_anim_right:
        :param sword_anim_down:
        """
        self.sword_default = sword_default
        self.sword_anim_top = sword_anim_top
        self.sword_anim_left = sword_anim_left
        self.sword_anim_right = sword_anim_right
        self.sword_anim_down = sword_anim_down

    def animations_sword(self, pos_x, pos_y, screen):
        """draw sword and make it animationized

        :param pos_x:
        :param pos_y:
        :param screen:
        :return:
        """
        match self.current_direction:
            case 'default':
                self.pos_x = pos_x - 75
                self.pos_y = pos_y
                screen.blit(self.sword_default, (self.pos_x, self.pos_y))
            case 'top':
                self.pos_x = pos_x - 50
                self.pos_y = pos_y - 125
                self.width = 200
                self.height = 130
                screen.blit(self.sword_anim_top[self.current_animation], (self.pos_x, self.pos_y))
                self.current_animation += 1

            case 'left':
                self.pos_x = pos_x - 135
                self.pos_y = pos_y
                self.width = 130
                self.height = 200
                screen.blit(self.sword_anim_left[self.current_animation], (self.pos_x, self.pos_y))
                self.current_animation += 1

            case 'right':
                self.pos_x = pos_x + 100
                self.pos_y = pos_y
                self.width = 130
                self.height = 200
                screen.blit(self.sword_anim_right[self.current_animation], (self.pos_x - 75, self.pos_y))
                self.current_animation += 1

            case 'down':
                self.pos_x = pos_x - 30
                self.pos_y = pos_y + 150
                self.width = 200
                self.height = 130
                screen.blit(self.sword_anim_down[self.current_animation], (self.pos_x, self.pos_y - 100))
                self.current_animation += 1

    def hit_stop(self):
        """stops sword's animation

        :rtype: bool
        """
        if self.current_animation == 4:
            self.current_animation = 0
            return True
        else:
            return False
