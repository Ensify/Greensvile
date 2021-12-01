import pygame as pg
import pytmx
import pickle

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)
    
def text(text,font,size,colour,x,y,surf):
    Font= pg.font.Font(font,size)
    textbox=Font.render ( text,True,colour)
    textRect=textbox.get_rect()
    textRect=(x,y)
    surf.blit(textbox,textRect)


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        with open("config.dat",'rb') as file:
            res=pickle.load(file)
            w_w,w_h=res[0]
        x = -target.rect.centerx + int(w_w / 2)
        y = -target.rect.centery + int(w_h / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - w_w), x)  # right
        y = max(-(self.height - w_h), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)