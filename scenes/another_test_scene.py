from classes.input import Input
from classes.scene_manager import SceneManager
import pygame as pg
from os.path import join


class AnotherTestScene:
    def __init__(self):
        # props + children
        pass

    def update(self, delta):
        if Input.is_action_pressed(pg.K_SPACE):
            print("Space key is pressed from AnotherTestScene")

        if Input.is_action_pressed(pg.K_RIGHT):
            MODULE_PATH = join("scenes", "test_scene.py")
            SceneManager.change_scene_to_file(MODULE_PATH, "TestScene")

    def draw(self, native_surface):
        pass
