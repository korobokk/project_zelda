from game_classes import *

def GameProcess(screen, game_map, main_character):
    match game_map.current_map:
        case 1:
            game_map.change_map_borders()
            game_map.draw_map1(screen)
            game_map.ghosts_spawn_x_min = 350
            game_map.ghosts_spawn_x_max = 1500
            game_map.ghosts_spawn_y_min = 50
            game_map.ghosts_spawn_y_max = 950
            if not main_character.weapon_bool:
                game_map.sword_take(main_character)
            for ghost in game_map.ghosts:
                ghost.movement(main_character.hitbox_x, main_character.hitbox_y, screen)
                if ghost.collide_w_hero(main_character):
                    main_character.health -= 1
                    game_map.ghosts.remove(ghost)
                    game_map.ghosts_count -= 1
            if game_map.ghosts_count == 0:
                game_map.ghosts_at_map += 1
                if game_map.ghosts_at_map >= 3:
                    game_map.boss_spawn(main_character)
                for i in range(game_map.ghosts_at_map):
                    game_map.ghosts_spawn(main_character)
            if game_map.ghosts_at_map == 4:
                main_character.pos_x = 700
                main_character.pos_y = 540
                main_character.hitbox_movement()
                game_map.current_map = 2
                game_map.ghosts = []
                game_map.ghosts_count = 0
                game_map.ghosts_at_map = 0
        case 2:
            game_map.change_map_borders()
            game_map.draw_map2(screen)
            game_map.ghosts_spawn_x_min = 700
            game_map.ghosts_spawn_x_max = 950
            game_map.ghosts_spawn_y_min = 0
            game_map.ghosts_spawn_y_max = 500
            for ghost in game_map.ghosts:
                ghost.movement(main_character.hitbox_x, main_character.hitbox_y, screen)
                if ghost.collide_w_hero(main_character):
                    main_character.health -= 1
                    game_map.ghosts.remove(ghost)
                    game_map.ghosts_count -= 1
            print(game_map.ghosts_count)
            if game_map.ghosts_count == 0:
                game_map.ghosts_at_map += 1
                if game_map.ghosts_at_map >= 3:
                    game_map.boss_spawn(main_character)
                for i in range(game_map.ghosts_at_map):
                    game_map.ghosts_spawn(main_character)
    if main_character.health <= 0:
        return (False, main_character.killing_ghosts)
    main_character.movement(screen, game_map)

    return (True, 0)


def start_zel_game():
    gameplay = True
    running = True
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("лютый марио")
    game_map1 = pygame.image.load("linkleft/map_12.png")
    game_map2 = pygame.image.load("linkleft/map_13.png")
    ghost_im = pygame.image.load("linkleft/ghost.png")
    ghost_boss = pygame.image.load("linkleft/ghost_red.png")
    play_map = Game_map([game_map1, game_map2], Ghost, ghost_im, ghost_boss)

    link_left = [
        pygame.image.load("linkleft/game_now_1.png"),
        pygame.image.load("linkleft/game_now_2.png"),
        pygame.image.load("linkleft/game_now_3.png"),
        pygame.image.load("linkleft/game_now_4.png"),
    ]

    link_right = [
        pygame.image.load("linkright/Sprite-0001.png"),
        pygame.image.load("linkright/Sprite-0002.png"),
        pygame.image.load("linkright/Sprite-0003.png"),
        pygame.image.load("linkright/Sprite-0004.png"),
    ]

    link_top = [
        pygame.image.load("linktop/game_now_12.png"),
        pygame.image.load("linktop/game_now_13.png"),
        pygame.image.load("linktop/game_now_14.png"),
        pygame.image.load("linktop/game_now_15.png"),
        pygame.image.load("linktop/game_now_16.png"),
        pygame.image.load("linktop/game_now_17.png"),
        pygame.image.load("linktop/game_now_18.png"),
        pygame.image.load("linktop/game_now_19.png"),
        pygame.image.load("linktop/game_now_20.png")
    ]

    link_down = [
        pygame.image.load("linkdown/game_now_22.png"),
        pygame.image.load("linkdown/game_now_23.png"),
        pygame.image.load("linkdown/game_now_24.png"),
        pygame.image.load("linkdown/game_now_25.png"),
        pygame.image.load("linkdown/game_now_26.png"),
        pygame.image.load("linkdown/game_now_27.png"),
        pygame.image.load("linkdown/game_now_28.png"),
        pygame.image.load("linkdown/game_now_29.png"),
        pygame.image.load("linkdown/game_now_30.png")
    ]

    default = {
        'left': pygame.image.load("linkleft/game_now_1.png"),
        'right': pygame.image.load("linkright/Sprite-0001.png"),
        'top': pygame.image.load("linktop/game_now_12.png"),
        'down': pygame.image.load("linkdown/game_now_22.png")
    }

    sword_anim_top = [pygame.image.load("linkleft/sword_12.png"), pygame.image.load("linkleft/sword_22.png"),
                      pygame.image.load("linkleft/sword_32.png"), pygame.image.load("linkleft/sword_42.png")]
    sword_anim_left = [pygame.image.load("linkleft/sword_124.png"), pygame.image.load("linkleft/sword_224.png"),
                       pygame.image.load("linkleft/sword_324.png"), pygame.image.load("linkleft/sword_424.png")]
    sword_anim_right = [pygame.image.load("linkleft/sword_122.png"), pygame.image.load("linkleft/sword_222.png"),
                        pygame.image.load("linkleft/sword_322.png"), pygame.image.load("linkleft/sword_422.png")]
    sword_anim_down = [pygame.image.load("linkleft/sword_123.png"), pygame.image.load("linkleft/sword_223.png"),
                       pygame.image.load("linkleft/sword_323.png"), pygame.image.load("linkleft/sword_423.png")]
    sword_anim_default = pygame.image.load("linkleft/sword_12.png")
    sword = Sword(sword_anim_default, sword_anim_top, sword_anim_left, sword_anim_right, sword_anim_down)
    play_map.sword_spawn(sword, 650, 250)
    heart_im = pygame.image.load("linkleft/heart.png")
    main_character = Character(link_left, link_right, link_down, link_top, default, 500, 500, heart_im)
    main_character.speed = 24
    result = 0
    while running:
        if gameplay:
            gameplay, result = GameProcess(screen, play_map, main_character)
        else:
            running = False
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(16)
    pygame.quit()

    return result