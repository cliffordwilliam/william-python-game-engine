import pygame as pg


class Sprite(pg.sprite.Sprite):
    def __init__(self, surface, groups, h_frame, v_frame):
        super().__init__(groups)
        self.image = surface
        self.rect = surface.get_frect()
        self.frame_index = 0  # count from top left, then bottom
        self.frames_dict = {}
        self.frame_width = surface.get_width() // h_frame
        self.frame_height = surface.get_height() // v_frame
        for col in range(h_frame):
            for row in range(v_frame):
                frame_x = col * self.frame_width
                frame_y = row * self.frame_height
                self.frames_dict[len(self.frames_dict)] = (
                    frame_x, frame_y, self.frame_width, self.frame_height)

    def draw(self, native_surface, camera_position=pg.Vector2(0, 0)):
        # self.frame_index -> frame_rect -> draw a chunk of self.image
        frame_x, frame_y, frame_width, frame_height = self.frames_dict[self.frame_index]
        frame_rect = pg.Rect(frame_x, frame_y, frame_width, frame_height)
        # offset the self.rect by camera position
        offset_pos = self.rect.topleft - camera_position
        # render chunk of spritesheet with camera offset
        native_surface.blit(self.image, offset_pos, frame_rect)
