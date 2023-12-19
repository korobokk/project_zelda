from game_classes import *
import pytest

testable_object1 = Ghost(pygame.image.load("linkleft/ghost.png"), 600, 600)
testable_object2 = Ghost(pygame.image.load("linkleft/ghost.png"), 0, 0)
anim = pygame.image.load("linkleft/game_now_1.png")
default = {
    'left': pygame.image.load("linkleft/game_now_1.png"),
    'right': pygame.image.load("linkright/Sprite-0001.png"),
    'top': pygame.image.load("linktop/game_now_12.png"),
    'down': pygame.image.load("linkdown/game_now_22.png")
}
testable_hero = Character([anim], [anim], [anim], [anim], default, 0, 0, anim)


def test_collide_with_large():
    testable_object2.hitbox_x = 0
    testable_object2.hitbox_y = 0
    testable_object1.hitbox_x = 800
    testable_object1.hitbox_y = 800
    testable_object2.width = 1920
    testable_object2.height = 1080
    assert testable_object1.collide_w_hero(testable_object2)


def test_colide_with_small():
    testable_object2.hitbox_x = 600
    testable_object2.hitbox_y = 600
    testable_object1.hitbox_x = 600
    testable_object1.hitbox_y = 600
    testable_object2.width = 1
    testable_object2.height = 1
    assert testable_object1.collide_w_hero(testable_object2)


def test_collide_with_close():
    testable_object2.hitbox_x = 600
    testable_object2.hitbox_y = 600
    testable_object1.hitbox_x = 599
    testable_object1.hitbox_y = 599
    testable_object2.width = 1
    testable_object2.height = 1
    assert testable_object1.collide_w_hero(testable_object2)


def test_not_collide_with_close():
    testable_object2.hitbox_x = 600
    testable_object2.hitbox_y = 600
    testable_object1.hitbox_x = 598
    testable_object1.hitbox_y = 598
    testable_object2.width = 1
    testable_object2.height = 1
    assert testable_object1.collide_w_hero(testable_object2)


def test_movement_animation_change_number():
    testable_hero.animations_left = [anim, anim, anim, anim, anim, anim, anim, anim]
    testable_hero.animations_left_count = 8
    testable_hero.animations_right = [anim, anim, anim, anim, anim, anim, anim, anim, anim]
    testable_hero.animations_right_count = 9
    testable_hero.animations_up = [anim, anim, anim, anim, anim, anim, anim, anim, anim, anim]
    testable_hero.animations_up_count = 10
    testable_hero.animations_down = [anim, anim, anim, anim]
    testable_hero.animations_down_count = 4
    testable_hero.current_animation_left = 0
    testable_hero.current_animation_right = 0
    testable_hero.current_animation_up = 0
    testable_hero.current_animation_down = 0
    testable_hero.current_animation_type = 'left'
    for i in range(1, 100):
        testable_hero.animation_change_animation_number()
        assert testable_hero.current_animation_left == i % 8
    testable_hero.animation_set_type('right')
    for i in range(1, 100):
        testable_hero.animation_change_animation_number()
        assert testable_hero.current_animation_right == i % 9
    testable_hero.animation_set_type('top')
    for i in range(1, 100):
        testable_hero.animation_change_animation_number()
        assert testable_hero.current_animation_up == i % 10
    testable_hero.animation_set_type('down')
    for i in range(1, 100):
        testable_hero.animation_change_animation_number()
        assert testable_hero.current_animation_down == i % 4


def test_ghosts_spawner():
    game_map = Game_map([anim], Ghost, anim, anim)
    testable_hero.hitbox_x = 600
    testable_hero.hitbox_y = 600
    for i in range(10000):
        game_map.ghosts_spawn(testable_hero)
    for ghost in game_map.ghosts:
        assert not ghost.collide_w_hero(testable_hero)
