from classes.input import Input
from classes.scene_manager import SceneManager
import pygame as pg


class AnotherTestScene:
    def __init__(self):
        # props + children
        pass

    def update(self, delta):
        if Input.is_action_pressed(pg.K_SPACE):
            print("Space key is pressed from AnotherTestScene")

        if Input.is_action_pressed(pg.K_RIGHT):
            SceneManager.change_scene_to_file(
                "./scenes/test_scene.py", "TestScene")

    def draw(self):
        pass
