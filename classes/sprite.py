import pygame as pg


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
        self.ignore_camera = ignore_camera
        # self.rect = surface.get_frect()
        self.rect = pg.Rect((0, 0), (self.frame_width, self.frame_height))

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
        # render rect outline
        pg.draw.rect(native_surface, (255, 0, 0),
                     self.rect.move(-camera_position.x, -camera_position.y), 1)
