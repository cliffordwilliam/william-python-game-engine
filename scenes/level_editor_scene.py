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
        self.grid_color = "gray5"
        self.grid_color_secondary = "gray10"
        self.scale_factor = c.DISPLAY_WIDTH // c.NATIVE_RESOLUTION_WIDTH
        # to be saved
        self.sprites_info = []
        # spritesheet
        self.spritesheet_surface = pg.image.load(join("images", "village.png"))
        # # the current choosen sprite display
        # self.current_sprite = Sprite(
        #     self.spritesheet_surface, self.fixed_layer, 22, 10, True)
        # # set starting frame_index
        # self.current_sprite.frame_index = 0
        # # shift it by 1 tile
        # self.current_sprite.rect.topleft += pg.Vector2(
        #     c.TILE_SIZE, 2 * c.TILE_SIZE)
        # set the starting layer
        self.current_layer = 0
        # font
        self.font = pg.font.Font(join("fonts", "cg-pixel-3x5.ttf"), 5)
        # menu
        # pretend fetch menu data from file - contains all classes - class = tree, house, grass
        # data should contain - icon, the file to be instanced
        # TODO: store this somewhere else
        self.menu_items = [
            pg.Rect(c.TILE_SIZE * 4, c.TILE_SIZE * 5,
                    c.TILE_SIZE * 4, c.TILE_SIZE * 3),
            pg.Rect(c.TILE_SIZE * 0, c.TILE_SIZE * 5,
                    c.TILE_SIZE * 4, c.TILE_SIZE * 3)
        ]
        self.menu_offset = 0
        self.menu_item_icon_width = 12
        self.current_icon_rect = self.menu_items[0]

    def draw_ruler(self, surface):
        # Calculate the position of the ruler relative to the camera
        rel_x = self.camera.position.x % self.grid_size
        rel_y = self.camera.position.y % self.grid_size

        # Calculate the starting number based on the current scroll position
        start_number_x = self.camera.position.x // self.grid_size
        start_number_y = self.camera.position.y // self.grid_size

        # Draw vertical ruler
        for x in range(0, c.NATIVE_RESOLUTION_WIDTH + c.TILE_SIZE, self.grid_size):
            number = int(start_number_x + x // self.grid_size)
            text_surface = self.font.render(str(number), True, "white")
            surface.blit(text_surface, (x - rel_x, 0))

        # Draw horizontal ruler
        for y in range(0, c.NATIVE_RESOLUTION_HEIGHT + c.TILE_SIZE, self.grid_size):
            number = int(start_number_y + y // self.grid_size)
            text_surface = self.font.render(str(number), True, "white")
            surface.blit(text_surface, (0, y - rel_y))

    def draw_grid(self, surface, multiplier=1, color=None):
        # custom color?
        if color is None:
            color = self.grid_color
        # self.camera.position -> rel pos
        rel_x = self.camera.position.x % (self.grid_size*multiplier)
        rel_y = self.camera.position.y % (self.grid_size*multiplier)
        # draw v line as much as native width + offset
        for x in range(0, c.NATIVE_RESOLUTION_WIDTH + c.TILE_SIZE, (self.grid_size*multiplier)):
            pg.draw.line(surface, color, (x - rel_x, 0),
                         (x - rel_x, c.NATIVE_RESOLUTION_HEIGHT))
        # draw h line as much as native width + offset
        for y in range(0, c.NATIVE_RESOLUTION_HEIGHT + c.TILE_SIZE, (self.grid_size*multiplier)):
            pg.draw.line(surface, color, (0, y - rel_y),
                         (c.NATIVE_RESOLUTION_WIDTH, y - rel_y))

    def draw_origin(self, surface):
        pg.draw.circle(surface, "red", (0 - self.camera.position.x,
                       0 - self.camera.position.y), 1)

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
        # new_tile_sprite = Sprite(
        #     self.spritesheet_surface, self.layers[self.current_layer], 22, 10)
        # TODO: save this data somewhere else, fetch it here and create a menu to cycle between the items
        new_tile_sprite = Sprite(
            self.spritesheet_surface, self.layers[self.current_layer], 1, 1, False, self.current_icon_rect)
        # set its position
        new_tile_sprite.rect.topleft = snapped_pos
        # set its frame_index
        # new_tile_sprite.frame_index = self.current_sprite.frame_index
        # update sprites_info
        sprite_info = {
            'topleft': new_tile_sprite.rect.topleft,
            # 'frame_index': new_tile_sprite.frame_index,
            'layer': self.layers[self.current_layer],
        }
        self.sprites_info.append(sprite_info)

    def on_icon_click(self, icon_rect):
        # Implement the logic for handling the click event on the icon here
        self.current_icon_rect = icon_rect

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
        # if Input.is_action_just_pressed(pg.K_d):
        #     self.current_sprite.frame_index += 1

        # if Input.is_action_just_pressed(pg.K_a):
        #     self.current_sprite.frame_index -= 1

        if Input.is_action_just_pressed(pg.K_w):
            self.current_layer += 1

        if Input.is_action_just_pressed(pg.K_s):
            self.current_layer -= 1

        if Input.is_action_just_pressed(pg.K_e):
            self.menu_offset += c.TILE_SIZE

        if Input.is_action_just_pressed(pg.K_q):
            self.menu_offset -= c.TILE_SIZE

        # clamp current_sprite.frame_index and current_layer
        self.current_layer = max(
            0, min(self.current_layer, len(self.layers) - 1))

        # self.current_sprite.frame_index = max(
        #     0, min(self.current_sprite.frame_index, self.current_sprite.total_frames))

    def draw(self, native_surface):
        # render grid at most bottom
        self.draw_grid(native_surface)
        # render sec grid at most bottom
        self.draw_grid(native_surface, 5, self.grid_color_secondary)
        # render origin
        self.draw_origin(native_surface)
        # render the rulers
        self.draw_ruler(native_surface)
        # render the layers from bottom up
        for layer in self.layers:
            layer.draw(native_surface, self.camera.position)
        # render current_layer here for dynamic value
        current_layer_surface = self.font.render(
            'current layer: %s' % self.current_layer, True, "aliceblue")
        native_surface.blit(current_layer_surface, (c.TILE_SIZE, c.TILE_SIZE))
        # render menu items
        for i, icon_rect in enumerate(self.menu_items):
            # create the frame
            item_rect = pg.Rect((0, 0), (c.TILE_SIZE, c.TILE_SIZE))
            item_rect.bottom = c.NATIVE_RESOLUTION_HEIGHT
            item_rect.left += i * c.TILE_SIZE
            item_rect.left += self.menu_offset
            # get icon
            icon_surface = self.spritesheet_surface.subsurface(
                icon_rect).copy()
            current_width = icon_surface.get_width()
            current_height = icon_surface.get_height()
            desired_width = self.menu_item_icon_width
            scale_factor = desired_width / current_width
            desired_height = int(current_height * scale_factor)
            scaled_icon_surface = pg.transform.scale(
                icon_surface, (desired_width, desired_height))
            # items center justify center
            y_offset = int((16 - desired_height) // 2)
            x_offset = int((16 - desired_width) // 2)
            shifted_rect = item_rect.move(x_offset, y_offset)
            pg.draw.rect(native_surface, "grey0", item_rect)
            pg.draw.rect(native_surface, (255, 0, 0), item_rect, 1)
            native_surface.blit(scaled_icon_surface, shifted_rect)
        # render the current_icon_rect
        # create the frame
        item_rect = pg.Rect((0, 0), (c.TILE_SIZE, c.TILE_SIZE))
        item_rect.topleft += pg.Vector2(c.TILE_SIZE, 2 * c.TILE_SIZE)
        icon_surface = self.spritesheet_surface.subsurface(
            self.current_icon_rect).copy()
        current_width = icon_surface.get_width()
        current_height = icon_surface.get_height()
        desired_width = self.menu_item_icon_width
        scale_factor = desired_width / current_width
        desired_height = int(current_height * scale_factor)
        scaled_icon_surface = pg.transform.scale(
            icon_surface, (desired_width, desired_height))
        # items center justify center
        y_offset = int((16 - desired_height) // 2)
        x_offset = int((16 - desired_width) // 2)
        shifted_rect = item_rect.move(x_offset, y_offset)
        pg.draw.rect(native_surface, "grey0", item_rect)
        pg.draw.rect(native_surface, (255, 0, 0), item_rect, 1)
        native_surface.blit(scaled_icon_surface, shifted_rect)

    def input(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # right mouse click
            if event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                # handle icon click
                for i, icon_rect in enumerate(self.menu_items):
                    # Calculate the position and dimensions of the scaled icon
                    item_rect = pg.Rect((0, 0), (c.TILE_SIZE, c.TILE_SIZE))
                    item_rect.bottom = c.NATIVE_RESOLUTION_HEIGHT
                    item_rect.left += i * c.TILE_SIZE
                    item_rect.left += self.menu_offset
                    # Check if the mouse click occurred within the boundaries of the scaled icon
                    scaled_pos = (
                        mouse_pos[0] // self.scale_factor, mouse_pos[1] // self.scale_factor)
                    if item_rect.collidepoint(scaled_pos):
                        # Execute callback function for the clicked icon
                        self.on_icon_click(icon_rect)
                        return
                # handle grid click
                self.on_mouse_grid_left_click()
                # TODO: buy a mouse - add a delete feature with the other button
