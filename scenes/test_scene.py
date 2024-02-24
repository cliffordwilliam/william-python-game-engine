from classes.input import Input
from classes.scene_manager import SceneManager
import pygame as pg


class TestScene:
    def __init__(self):
        # props + children
        pass

    def update(self, delta):
        # get axis
        # direction = Input.get_axis(pg.K_LEFT, pg.K_RIGHT)
        # print(direction)
        # switch scene test
        if Input.is_action_pressed(pg.K_SPACE):
            print("Space key is pressed from TestScene")

        if Input.is_action_pressed(pg.K_LEFT):
            SceneManager.change_scene_to_file(
                "./scenes/another_test_scene.py", "AnotherTestScene")

    def draw(self):
        pass
