from classes.input import Input
from classes.scene_manager import SceneManager
import pygame as pg
from os.path import join
from classes.sprite import Sprite
import config.constant as c
from classes.group import Group
from classes.camera import Camera


class TestScene:
    def __init__(self):
        # layers
        self.all_sprites = Group()
        # nodes
        # SPRITE
        village_spritesheet_surface = pg.image.load(
            join("images", "village.png"))
        self.TEST_SPRITE = Sprite(village_spritesheet_surface,
                                  self.all_sprites, 22, 10)
        # edit the frame index
        self.TEST_SPRITE.frame_index = 110
        # edit its position
        self.TEST_SPRITE.rect.top = c.TILE_SIZE
        # CAMERA
        self.camera = Camera()

    def update(self, delta):
        if Input.is_action_pressed(pg.K_SPACE):
            self.TEST_SPRITE.frame_index += 1
            print("Space key is pressed from TestScene",
                  self.TEST_SPRITE.frame_index)

        if Input.is_action_pressed(pg.K_LEFT):
            MODULE_PATH = join("scenes", "another_test_scene.py")
            SceneManager.change_scene_to_file(MODULE_PATH, "AnotherTestScene")

        if Input.is_action_pressed(pg.K_RIGHT):
            self.camera.position += pg.Vector2(1, 0)

    def draw(self, native_surface):
        self.all_sprites.draw(native_surface, self.camera.position)

    def input(self, event):
        pass
