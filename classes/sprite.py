import pygame as pg
from os.path import join  # debug for font rendering


class Sprite(pg.sprite.Sprite):
    def __init__(self, surface, groups, h_frame, v_frame, ignore_camera=False, image_rect=None):
        super().__init__(groups)
        self.image = surface
        if image_rect:
            self.image = surface.subsurface(image_rect).copy()
        self.frame_index = 0  # count from top left, then bottom
        self.frames_dict = {}
        self.frame_width = self.image.get_width() // h_frame
        self.frame_height = self.image.get_height() // v_frame
        self.total_frames = h_frame * v_frame
        for col in range(h_frame):
            for row in range(v_frame):
                frame_x = col * self.frame_width
                frame_y = row * self.frame_height
                self.frames_dict[len(self.frames_dict)] = (
                    frame_x, frame_y, self.frame_width, self.frame_height)
        self.rect = pg.Rect((0, 0), (self.frame_width, self.frame_height))
        self.ignore_camera = ignore_camera

        # DEBUG TODO: remove later
        self.font = pg.font.Font(join("fonts", "cg-pixel-3x5.ttf"), 5)
        self.mask = []
        self.is_autotile = False

    def draw(self, native_surface, camera_position=pg.Vector2(0, 0)):
        # self.frame_index -> frame_rect -> draw a chunk of self.image
        frame_x, frame_y, frame_width, frame_height = self.frames_dict[self.frame_index]
        frame_rect = pg.Rect(frame_x, frame_y, frame_width, frame_height)

        # offset the self.rect by camera position
        if self.ignore_camera:
            offset_pos = self.rect.topleft
        else:
            offset_pos = self.rect.topleft - camera_position

        # render chunk of spritesheet with camera offset
        native_surface.blit(self.image, offset_pos, frame_rect)

        # debug render rect outline
        # self.debug_render_rect_outline(native_surface, camera_position)

        # debug render frame index
        # self.debug_font_draw(native_surface, camera_position, "debug text")

        # debug draw bitmap
        # self.debug_bitmask_draw(native_surface, camera_position, self.mask)

    # TODO: remove later
    def debug_render_rect_outline(self, native_surface, camera_position):
        pg.draw.rect(native_surface, "brown4",
                     self.rect.move(-camera_position.x, -camera_position.y), 1)

    def debug_font_draw(self, native_surface, camera_position, string):
        debug_surface = self.font.render(string, True, "white")
        native_surface.blit(
            debug_surface, self.rect.move(-camera_position.x, -camera_position.y))

    def debug_bitmask_draw(self, native_surface, camera_position, mask):
        #  bitmask surf -> native_surf
        bitmask_surface = pg.Surface((self.frame_width, self.frame_height))
        bitmask_surface.set_alpha(100)

        # check my mask -> draw rect -> bitmask surf
        for y, row in enumerate(mask):
            for x, bit in enumerate(row):
                if bit == 1:
                    size = self.frame_width / 3
                    xpos = x * size
                    ypos = y * size
                    pg.draw.rect(bitmask_surface, "red",
                                 (xpos, ypos, size, size))

        # bitmask surf -> native_surface
        native_surface.blit(
            bitmask_surface, self.rect.move(-camera_position.x, -camera_position.y))
