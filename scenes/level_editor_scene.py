from classes.input import Input
from classes.scene_manager import SceneManager
import pygame as pg
from os.path import join
from classes.sprite import Sprite
import config.constant as c
from classes.group import Group
from classes.camera import Camera


class LevelEditorScene:
    def __init__(self):
        # layers
        self.all_sprites = Group()
        # nodes
        # CAMERA
        self.camera = Camera()
        # grid settings
        self.grid_size = c.TILE_SIZE
        self.grid_color = "blue3"
        self.scale_factor = c.DISPLAY_WIDTH // c.NATIVE_RESOLUTION_WIDTH

    def draw_grid(self, surface):
        # self.camera.position -> rel pos
        rel_x = self.camera.position.x % self.grid_size
        rel_y = self.camera.position.y % self.grid_size
        # draw v line as much as native width + offset
        for x in range(0, c.NATIVE_RESOLUTION_WIDTH, self.grid_size):
            pg.draw.line(surface, self.grid_color, (x - rel_x, 0),
                         (x - rel_x, c.NATIVE_RESOLUTION_HEIGHT))
        # draw h line as much as native width + offset
        for y in range(0, c.NATIVE_RESOLUTION_HEIGHT, self.grid_size):
            pg.draw.line(surface, self.grid_color, (0, y - rel_y),
                         (c.NATIVE_RESOLUTION_WIDTH, y - rel_y))

    def snap_to_grid(self, pos):
        scaled_pos = (pos[0] // self.scale_factor, pos[1] // self.scale_factor)
        x = scaled_pos[0] // self.grid_size * self.grid_size
        y = scaled_pos[1] // self.grid_size * self.grid_size
        return (x, y)

    def on_mouse_grid_left_click(self):
        mouse_pos = pg.mouse.get_pos() + self.camera.position * self.scale_factor
        snapped_pos = self.snap_to_grid(mouse_pos)
        surface = pg.Surface((c.TILE_SIZE, c.TILE_SIZE))
        TILE_SPRITE = Sprite(surface, self.all_sprites, 1, 1)
        TILE_SPRITE.rect.topleft = snapped_pos

    def update(self, delta):
        direction = pg.Vector2(0, 0)
        direction.x = Input.get_axis(pg.K_LEFT, pg.K_RIGHT)
        direction.y = Input.get_axis(pg.K_UP, pg.K_DOWN)
        self.camera.position += direction

    def draw(self, native_surface):
        self.draw_grid(native_surface)
        self.all_sprites.draw(native_surface, self.camera.position)

    def input(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_mouse_grid_left_click()
