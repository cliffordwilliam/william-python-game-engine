import pygame as pg


class Group(pg.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, native_surface, camera_position=pg.Vector2(0, 0)):
        for sprite in self:
            sprite.draw(native_surface, camera_position)
