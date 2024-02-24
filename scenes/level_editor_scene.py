from classes.input import Input
from classes.scene_manager import SceneManager
import pygame as pg
from os.path import join
from classes.sprite import Sprite
import config.constant as c
from classes.group import Group
from classes.camera import Camera


# TODO: add autotiling feature - dedicate a mode + different texture to use
class LevelEditorScene:
    def __init__(self):
        self.layer_1 = Group()
        self.layer_2 = Group()
        self.fixed_layer = Group()
        self.layers = [
            self.layer_1,
            self.layer_2,
            self.fixed_layer
        ]
        # nodes
        # CAMERA
        self.camera = Camera()
        # grid settings
        self.grid_size = c.TILE_SIZE
        self.grid_color = "blue3"
        self.scale_factor = c.DISPLAY_WIDTH // c.NATIVE_RESOLUTION_WIDTH
        # to be saved
        self.sprites_info = []
        # spritesheet
        self.spritesheet_surface = pg.image.load(join("images", "village.png"))
        # the current choosen sprite display - TODO: DISPLAY THIS INFO ON SCREEN
        self.current_sprite = Sprite(
            self.spritesheet_surface, self.fixed_layer, 22, 10, True)
        # set starting frame_index
        self.current_sprite.frame_index = 0
        # shift it down by 1 tile
        self.current_sprite.rect.topleft += pg.Vector2(0, c.TILE_SIZE)
        # set the starting layer
        self.current_layer = 0

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
        # check collision with existing sprites in the same layer
        for sprite in self.layers[self.current_layer]:
            if sprite.rect.topleft == snapped_pos:
                return
        # instance sprite
        new_tile_sprite = Sprite(
            self.spritesheet_surface, self.layers[self.current_layer], 22, 10)
        # set its position
        new_tile_sprite.rect.topleft = snapped_pos
        # set its frame_index
        new_tile_sprite.frame_index = self.current_sprite.frame_index
        # update sprites_info
        sprite_info = {
            'topleft': new_tile_sprite.rect.topleft,
            'frame_index': new_tile_sprite.frame_index,
            'layer': self.layers[self.current_layer],
        }
        self.sprites_info.append(sprite_info)

    def update(self, delta):
        # move camera
        direction = pg.Vector2(0, 0)
        direction.x = Input.get_axis(pg.K_LEFT, pg.K_RIGHT)
        direction.y = Input.get_axis(pg.K_UP, pg.K_DOWN)
        self.camera.position += direction

        # TODO: save the map
        # if Input.is_action_pressed(pg.K_SPACE):
        #     print(self.sprites_info)

        # update current_sprite.frame_index and current_layer
        if Input.is_action_just_pressed(pg.K_d):
            self.current_sprite.frame_index += 1

        if Input.is_action_just_pressed(pg.K_a):
            self.current_sprite.frame_index -= 1

        if Input.is_action_just_pressed(pg.K_w):
            self.current_layer += 1

        if Input.is_action_just_pressed(pg.K_s):
            self.current_layer -= 1

        # clamp current_sprite.frame_index and current_layer
        self.current_layer = max(
            0, min(self.current_layer, len(self.layers) - 1))

        self.current_sprite.frame_index = max(
            0, min(self.current_sprite.frame_index, self.current_sprite.total_frames))

    def draw(self, native_surface):
        # render grid at most bottom
        self.draw_grid(native_surface)
        # render the layers from bottom up
        for layer in self.layers:
            layer.draw(native_surface, self.camera.position)
        # render current_layer here for dynamic value
        font = pg.font.SysFont(None, 16)
        current_layer_surface = font.render(
            'current layer: %s' % self.current_layer, True, "aliceblue")
        native_surface.blit(current_layer_surface, (0, 0))

    def input(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_mouse_grid_left_click()
        # TODO: buy a mouse - add a delete feature with the other button
