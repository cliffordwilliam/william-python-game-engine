from classes.input import Input
from classes.scene_manager import SceneManager
import pygame as pg
from os.path import join
from classes.sprite import Sprite
import config.constant as c
from classes.group import Group
from classes.camera import Camera
from data.village_rect_data import VILLAGE_RECT_DATA
import random


# TODO: add autotiling feature - dedicate a mode + different texture to use
class LevelEditorScene:
    def __init__(self):
        # layers
        self.fixed_layer = Group()
        self.layers = [
            Group(),
            Group(),
            Group()
        ]
        self.current_layer = 0

        # camera
        self.camera = Camera()

        # grid settings
        self.grid_size = c.TILE_SIZE
        self.grid_color = "gray5"
        self.grid_color_secondary = "gray10"
        self.scale_factor = c.DISPLAY_WIDTH // c.NATIVE_RESOLUTION_WIDTH

        # to be saved
        # self.sprites_info = []

        # spritesheet
        self.spritesheet_surface = pg.image.load(join("images", "village.png"))

        # font
        self.font = pg.font.Font(join("fonts", "cg-pixel-3x5.ttf"), 5)

        # menu
        self.menu_items = []
        for item in VILLAGE_RECT_DATA:
            x = item["x"] * c.TILE_SIZE
            y = item["y"] * c.TILE_SIZE
            width = item["width"] * c.TILE_SIZE
            height = item["height"] * c.TILE_SIZE
            is_autotile = item.get("is_autotile", False)
            v_frame = item.get("v_frame", 1)
            h_frame = item.get("h_frame", 1)
            rect = pg.Rect(x, y, width, height)
            item = (rect, is_autotile, v_frame, h_frame)
            self.menu_items.append(item)
        self.menu_offset = 0  # user can move its position horizontally
        self.menu_item_icon_width = 12
        self.current_spritesheet_rect = self.menu_items[0][0]
        self.current_is_autotile = self.menu_items[0][1]
        self.current_v_frame = self.menu_items[0][2]
        self.current_h_frame = self.menu_items[0][3]

    def draw_ruler(self, surface):
        # calculate the position of the ruler relative to the camera
        rel_x = self.camera.position.x % self.grid_size
        rel_y = self.camera.position.y % self.grid_size

        # calculate the starting number based on the current scroll position
        start_number_x = self.camera.position.x // self.grid_size
        start_number_y = self.camera.position.y // self.grid_size

        # draw vertical ruler
        for x in range(0, c.NATIVE_RESOLUTION_WIDTH + c.TILE_SIZE, self.grid_size):
            number = int(start_number_x + x // self.grid_size)
            text_surface = self.font.render(str(number), True, "white")
            surface.blit(text_surface, (x - rel_x, 0))

        # draw horizontal ruler
        for y in range(0, c.NATIVE_RESOLUTION_HEIGHT + c.TILE_SIZE, self.grid_size):
            number = int(start_number_y + y // self.grid_size)
            text_surface = self.font.render(str(number), True, "white")
            surface.blit(text_surface, (0, y - rel_y))

    def draw_grid(self, surface, multiplier=1, color=None):
        # custom color?
        if color is None:
            color = self.grid_color

        # self.camera.position -> rel pos
        rel_x = self.camera.position.x % (self.grid_size * multiplier)
        rel_y = self.camera.position.y % (self.grid_size * multiplier)

        # draw v line as much as native width + offset
        for x in range(0, c.NATIVE_RESOLUTION_WIDTH + c.TILE_SIZE, (self.grid_size * multiplier)):
            pg.draw.line(surface, color, (x - rel_x, 0),
                         (x - rel_x, c.NATIVE_RESOLUTION_HEIGHT))

        # draw h line as much as native width + offset
        for y in range(0, c.NATIVE_RESOLUTION_HEIGHT + c.TILE_SIZE, (self.grid_size * multiplier)):
            pg.draw.line(surface, color, (0, y - rel_y),
                         (c.NATIVE_RESOLUTION_WIDTH, y - rel_y))

    def draw_origin(self, surface):
        pg.draw.circle(surface, "red", (0 - self.camera.position.x,
                       0 - self.camera.position.y), 1)

    def snap_to_grid(self, pos):
        x = pos[0] // self.grid_size * self.grid_size
        y = pos[1] // self.grid_size * self.grid_size
        return (x, y)

    def get_mouse_pos_with_scaled_camera_offset(self):
        mouse_pos = pg.mouse.get_pos()
        scaled_mouse_pos_x = mouse_pos[0] // self.scale_factor
        scaled_mouse_pos_y = mouse_pos[1] // self.scale_factor
        shifted_mouse_pos_x = scaled_mouse_pos_x + self.camera.position.x
        shifted_mouse_pos_y = scaled_mouse_pos_y + self.camera.position.y
        return (shifted_mouse_pos_x, shifted_mouse_pos_y)

    def get_mouse_pos_with_scaled(self):
        mouse_pos = pg.mouse.get_pos()
        scaled_mouse_pos_x = mouse_pos[0] // self.scale_factor
        scaled_mouse_pos_y = mouse_pos[1] // self.scale_factor
        return (scaled_mouse_pos_x, scaled_mouse_pos_y)

    def on_mouse_grid_left_click(self, mouse_pos_with_scaled_camera_offset):
        # snap mouse position to grid top left cell
        snapped_pos = self.snap_to_grid(mouse_pos_with_scaled_camera_offset)

        # Loop through each sprite
        for sprite in self.layers[self.current_layer]:
            # Check if sprite rect matches snapped position
            if sprite.rect.topleft == snapped_pos:
                return

        # Instance sprite
        new_tile_sprite = Sprite(self.spritesheet_surface, self.layers[self.current_layer],
                                 self.current_h_frame, self.current_v_frame, False, self.current_spritesheet_rect)

        # Set its position
        new_tile_sprite.rect.topleft = snapped_pos

        # Autotile sprite handling
        if self.current_is_autotile:
            new_tile_sprite.is_autotile = True
            #  get THIS - ignore non autotile
            for sprite in self.layers[self.current_layer]:
                if sprite.is_autotile == False:
                    continue
                # prepare mask
                mask = [
                    [0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]
                ]
                for other_sprite in self.layers[self.current_layer]:
                    # OTHER rel to THIS
                    dx = (other_sprite.rect.left -
                          sprite.rect.left) // c.TILE_SIZE
                    dy = (other_sprite.rect.top -
                          sprite.rect.top) // c.TILE_SIZE

                    # Update THIS mask based on ALL OTHER
                    possible_positions = [
                        [(-1, -1), (0, -1), (1, -1),],
                        [(-1, 0), (0, 0), (1, 0),],
                        [(-1, 1), (0, 1), (1, 1)]
                    ]
                    # TODO: update corner checks, eg. tr corder is true if there is a top and right neigbour
                    for y, row in enumerate(possible_positions):
                        for x, possible_position in enumerate(row):
                            if possible_position == (dx, dy):
                                mask[y][x] = 1
                # mask ready
                # TODO: remove this DEBUG prop later

                # filter, if the top-left bit is set, the cell directly above, directly left, and diagonally above-left must be filled

                # handle TL
                if mask[0][0] == 1:
                    if mask[0][1] == 0 or mask[1][0] == 0:
                        mask[0][0] = 0

                # handle TR
                if mask[0][2] == 1:
                    if mask[0][1] == 0 or mask[1][2] == 0:
                        mask[0][2] = 0

                # handle BL
                if mask[2][0] == 1:
                    if mask[1][0] == 0 or mask[2][1] == 0:
                        mask[2][0] = 0

                # handle BR
                if mask[2][2] == 1:
                    if mask[1][2] == 0 or mask[2][1] == 0:
                        mask[2][2] = 0

                sprite.mask = mask
                # mask -> frame index
                # TODO: somehow make the frameindex be dynamic to each diff autotile
                frame_indices = {
                    (
                        (0, 0, 0),
                        (0, 1, 1),
                        (0, 1, 1)
                    ): 0,
                    (
                        (0, 1, 1),
                        (0, 1, 1),
                        (0, 1, 1)
                    ): 1,
                    (
                        (0, 1, 1),
                        (0, 1, 1),
                        (0, 0, 0)
                    ): 2,
                    (
                        (0, 0, 0),
                        (0, 1, 1),
                        (0, 0, 0)
                    ): 3,
                    (
                        (1, 1, 1),
                        (1, 1, 1),
                        (1, 1, 1)
                    ): random.choice([4, 6, 9]),
                    (
                        (0, 0, 0),
                        (1, 1, 1),
                        (1, 1, 1)
                    ): 5,
                    (
                        (1, 1, 1),
                        (1, 1, 1),
                        (0, 0, 0)
                    ): 7,
                    (
                        (0, 0, 0),
                        (1, 1, 1),
                        (0, 0, 0)
                    ): 8,
                    (
                        (0, 0, 0),
                        (1, 1, 0),
                        (1, 1, 0)
                    ): 10,
                    (
                        (1, 1, 0),
                        (1, 1, 0),
                        (1, 1, 0)
                    ): 11,
                    (
                        (1, 1, 0),
                        (1, 1, 0),
                        (0, 0, 0)
                    ): 12,
                    (
                        (0, 0, 0),
                        (1, 1, 0),
                        (0, 0, 0)
                    ): 13,
                    (
                        (0, 0, 0),
                        (0, 1, 0),
                        (0, 1, 0)
                    ): 15,
                    (
                        (0, 1, 0),
                        (0, 1, 0),
                        (0, 1, 0)
                    ): 16,
                    (
                        (0, 1, 0),
                        (0, 1, 0),
                        (0, 0, 0)
                    ): 17,
                    (
                        (0, 0, 0),
                        (0, 1, 0),
                        (0, 0, 0)
                    ): 18,
                    (
                        (0, 0, 0),
                        (0, 1, 1),
                        (0, 1, 0)
                    ): 20,
                    (
                        (0, 1, 1),
                        (0, 1, 1),
                        (0, 1, 0)
                    ): 21,
                    (
                        (0, 1, 0),
                        (0, 1, 1),
                        (0, 1, 1)
                    ): 22,
                    (
                        (0, 1, 0),
                        (0, 1, 1),
                        (0, 0, 0)
                    ): 23,
                    (
                        (0, 1, 0),
                        (0, 1, 1),
                        (0, 1, 0)
                    ): 24,
                    (
                        (0, 0, 0),
                        (1, 1, 1),
                        (1, 1, 0)
                    ): 25,
                    (
                        (1, 1, 1),
                        (1, 1, 1),
                        (1, 1, 0)
                    ): 26,
                    (
                        (1, 1, 0),
                        (1, 1, 1),
                        (1, 1, 1)
                    ): 27,
                    (
                        (1, 1, 0),
                        (1, 1, 1),
                        (0, 0, 0)
                    ): 28,
                    (
                        (1, 1, 0),
                        (1, 1, 1),
                        (1, 1, 0)
                    ): 29,
                    (
                        (0, 0, 0),
                        (1, 1, 1),
                        (0, 1, 1)
                    ): 30,
                    (
                        (1, 1, 1),
                        (1, 1, 1),
                        (0, 1, 1)
                    ): 31,
                    (
                        (0, 1, 1),
                        (1, 1, 1),
                        (1, 1, 1)
                    ): 32,
                    (
                        (0, 1, 1),
                        (1, 1, 1),
                        (0, 0, 0)
                    ): 33,
                    (
                        (0, 1, 1),
                        (1, 1, 1),
                        (0, 1, 1)
                    ): 34,
                    (
                        (0, 0, 0),
                        (1, 1, 0),
                        (0, 1, 0)
                    ): 35,
                    (
                        (1, 1, 0),
                        (1, 1, 0),
                        (0, 1, 0)
                    ): 36,
                    (
                        (0, 1, 0),
                        (1, 1, 0),
                        (1, 1, 0)
                    ): 37,
                    (
                        (0, 1, 0),
                        (1, 1, 0),
                        (0, 0, 0)
                    ): 38,
                    (
                        (0, 1, 0),
                        (1, 1, 0),
                        (0, 1, 0)
                    ): 39,
                    (
                        (0, 0, 0),
                        (1, 1, 1),
                        (0, 1, 0)
                    ): 40,
                    (
                        (1, 1, 1),
                        (1, 1, 1),
                        (0, 1, 0)
                    ): 41,
                    (
                        (0, 1, 0),
                        (1, 1, 1),
                        (1, 1, 1)
                    ): 42,
                    (
                        (0, 1, 0),
                        (1, 1, 1),
                        (0, 0, 0)
                    ): 43,
                    (
                        (0, 1, 0),
                        (1, 1, 1),
                        (0, 1, 0)
                    ): 44,
                    (
                        (1, 1, 0),
                        (1, 1, 1),
                        (0, 1, 1)
                    ): 45,
                    (
                        (0, 1, 1),
                        (1, 1, 1),
                        (1, 1, 0)
                    ): 46,
                    (
                        (0, 1, 0),
                        (1, 1, 1),
                        (0, 1, 1)
                    ): 47,
                    (
                        (0, 1, 1),
                        (1, 1, 1),
                        (0, 1, 0)
                    ): 48,
                    (
                        (0, 1, 0),
                        (1, 1, 1),
                        (1, 1, 0)
                    ): 52,
                    (
                        (1, 1, 0),
                        (1, 1, 1),
                        (0, 1, 0)
                    ): 53,
                }
                #  mask -> sprite.frame_index
                tuple_key = tuple(map(tuple, mask))
                sprite.frame_index = frame_indices.get(tuple_key, 18)

    def on_mouse_grid_right_click(self, mouse_pos_with_scaled_camera_offset):
        snapped_pos = self.snap_to_grid(mouse_pos_with_scaled_camera_offset)
        # check collision with existing sprites in the same layer
        for sprite in self.layers[self.current_layer]:
            if sprite.rect.topleft == snapped_pos:
                sprite.kill()

    def on_icon_left_click(self, icon_rect, is_autotile, v_frame, h_frame):
        self.current_spritesheet_rect = icon_rect
        self.current_is_autotile = is_autotile
        self.current_v_frame = v_frame
        self.current_h_frame = h_frame

    def get_one_menu_item_rect(self, i):
        item_rect = pg.Rect((0, 0), (c.TILE_SIZE, c.TILE_SIZE))
        item_rect.bottom = c.NATIVE_RESOLUTION_HEIGHT
        item_rect.left += i * c.TILE_SIZE
        item_rect.left += self.menu_offset
        return item_rect

    def scale_sprite_to_icon(self, icon_surface):
        current_width = icon_surface.get_width()
        current_height = icon_surface.get_height()
        desired_width = self.menu_item_icon_width
        scale_factor = desired_width / current_width
        desired_height = int(current_height * scale_factor)
        return pg.transform.scale(
            icon_surface, (desired_width, desired_height))

    def render_one_menu_item(self, scaled_icon_surface, item_rect, native_surface):
        scaled_icon_rect = scaled_icon_surface.get_frect()
        scaled_icon_rect.center = item_rect.center
        pg.draw.rect(native_surface, "grey0", item_rect)
        pg.draw.rect(native_surface, "brown4", item_rect, 1)
        native_surface.blit(scaled_icon_surface, scaled_icon_rect)

    def get_current_spritesheet_rect(self):
        item_rect = pg.Rect((0, 0), (c.TILE_SIZE, c.TILE_SIZE))
        item_rect.topleft += pg.Vector2(c.TILE_SIZE, 2 * c.TILE_SIZE)
        return item_rect

    def update(self, delta):
        # move camera
        direction = pg.Vector2(0, 0)
        direction.x = Input.get_axis(pg.K_LEFT, pg.K_RIGHT)
        direction.y = Input.get_axis(pg.K_UP, pg.K_DOWN)
        self.camera.position += direction

        # if Input.is_action_pressed(pg.K_SPACE):
        # TODO: save map
        # update sprites_info
        # sprite_info = {
        #     'topleft': new_tile_sprite.rect.topleft,
        #     'spritesheet_rect': new_tile_sprite.spritesheet_rect,
        #     'layer': self.layers[self.current_layer],
        # }
        # self.sprites_info.append(sprite_info)

        # select layer
        if Input.is_action_just_pressed(pg.K_w):
            self.current_layer += 1

        if Input.is_action_just_pressed(pg.K_s):
            self.current_layer -= 1

        # move menu pos
        if Input.is_action_just_pressed(pg.K_e):
            self.menu_offset += c.TILE_SIZE

        if Input.is_action_just_pressed(pg.K_q):
            self.menu_offset -= c.TILE_SIZE

        # clamp current_sprite.frame_index and current_layer
        self.current_layer = max(
            0, min(self.current_layer, len(self.layers) - 1))

    def draw(self, native_surface):
        self.draw_grid(native_surface)

        self.draw_grid(native_surface, 5, self.grid_color_secondary)

        self.draw_origin(native_surface)

        self.draw_ruler(native_surface)

        # render the layers from bottom up
        for layer in self.layers:
            layer.draw(native_surface, self.camera.position)

        # render the fixed layer
        self.fixed_layer.draw(native_surface, self.camera.position)

        # render current_layer UI for dynamic value
        current_layer_surface = self.font.render(
            'current layer: %s' % self.current_layer, True, "aliceblue")
        native_surface.blit(current_layer_surface, (c.TILE_SIZE, c.TILE_SIZE))

        # render menu items
        for i, item in enumerate(self.menu_items):
            one_menu_item_rect = self.get_one_menu_item_rect(i)
            icon_surface = self.spritesheet_surface.subsurface(
                item[0]).copy()
            scaled_icon_surface = self.scale_sprite_to_icon(icon_surface)
            self.render_one_menu_item(
                scaled_icon_surface, one_menu_item_rect, native_surface)

        # render the current_spritesheet_rect UI
        current_spritesheet_rect_item_rect = self.get_current_spritesheet_rect()
        icon_surface = self.spritesheet_surface.subsurface(
            self.current_spritesheet_rect).copy()
        scaled_icon_surface = self.scale_sprite_to_icon(icon_surface)
        self.render_one_menu_item(
            scaled_icon_surface, current_spritesheet_rect_item_rect, native_surface)

    def input(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos_with_scaled_camera_offset = self.get_mouse_pos_with_scaled_camera_offset()
            mouse_pos_with_scaled = self.get_mouse_pos_with_scaled()
            # right mouse click?
            if event.button == 1:
                # icon click?
                for i, item in enumerate(self.menu_items):
                    item_rect = self.get_one_menu_item_rect(i)
                    if item_rect.collidepoint(mouse_pos_with_scaled):
                        self.on_icon_left_click(
                            item[0], item[1], item[2], item[3])
                        return
                # handle grid click
                self.on_mouse_grid_left_click(
                    mouse_pos_with_scaled_camera_offset)
            # left mouse click?
            elif event.button == 3:
                # handle grid click
                self.on_mouse_grid_right_click(
                    mouse_pos_with_scaled_camera_offset)
