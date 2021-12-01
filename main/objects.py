import pygame as pg
from random import choice,randint
from tilemap import collide_hit_rect,text
from random import choice
import pickle
vec = pg.math.Vector2

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 196
    BAR_HEIGHT = 40
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, (173,38,38), fill_rect)

def draw_player_stamina(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, (0,255,0), fill_rect)
    pg.draw.rect(surf, (41,41,41), outline_rect, 5)



def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def draw_text(level,text,font_name,size,color,x,y):
    font=pg.font.Font(font_name,size)
    text_surface = font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.center = (x,y)
    level.screen.blit(text_surface,text_rect)

class Player(pg.sprite.Sprite):
    def __init__(self,level,x,y):
        self._layer = 3
        self.groups = level.all_sprites,level.player
        pg.sprite.Sprite.__init__(self,self.groups)
        self.level=level
        self.images = level.player_imgs
        self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.hit_rect = pg.Rect(0, 0, 64, 96)
        self.hit_rect.center = self.rect.center
        self.curent_dir = 0
        self.last_dir = 0
        self.nextFrame = pg.time.get_ticks()
        self.frame = 0
        self.changepic = False
        self.last_dir_dict ={0:[1,8,9],1:[10,18,19],2:[20,28,29],3:[32,38,39]}
        self.speed_mul=1
        self.controls=level.controls
        #------------------------------------------
        self.health=1
        self.stamina= 100
        self.has_sword=True
        self.sword_hit = False
        self.sword_damage=10
        self.can_attack=True
        self.sworddebouncestate=0
        self.has_bow=True
        self.can_fire_bow=True
        self.bowdebouncestate=0
        self.bow_damage=100
        self.Fire_arrow = False
        #------------------------------------------

    def get_keys(self):
        self.vel = vec(0,0)
        PLAYER_SPEED = 280*self.speed_mul
        self.keypressed= False
        keys = pg.key.get_pressed()

        if (not self.sword_hit and not self.Fire_arrow):
            if keys[self.controls[(3,1)][1]] or keys[self.controls[(3,2)][1]]:
                self.vel = vec(-PLAYER_SPEED,0)
                self.curent_dir= 1
                self.last_dir = 1 
                self.keypressed = True
            if keys[self.controls[(4,1)][1]] or keys[self.controls[(4,2)][1]]:
                self.vel = vec(PLAYER_SPEED,0)
                self.curent_dir= 2
                self.last_dir = 2
                self.keypressed = True
            if keys[self.controls[(1,1)][1]] or keys[self.controls[(1,2)][1]]:
                self.vel = vec(0,-PLAYER_SPEED)
                self.curent_dir= 3
                self.last_dir = 3
                self.keypressed = True
            if keys[self.controls[(2,1)][1]] or keys[self.controls[(2,2)][1]]:
                self.curent_dir=0
                self.last_dir = 0
                self.keypressed = True
                self.vel = vec(0,+PLAYER_SPEED)
            if keys[self.controls[(8,1)][1]] or keys[self.controls[(8,2)][1]]:
                self.speed_mul = 1.3
                if self.stamina>0:    
                    self.stamina-=1
            else:
                self.speed_mul= 1
                if self.stamina<100:
                    self.stamina+=0.5
            if self.stamina<0:
                self.stamina=0
            if self.stamina==0:
                self.speed_mul= 1

        if  self.keypressed:
            self.changepic = True
        else:
            self.changepic = False

    def update(self):
        if pg.time.get_ticks() > self.nextFrame:
            self.frame = (self.frame+1)%8
            self.nextFrame += 80
        if self.changepic:
            self.image = self.images[self.curent_dir*10+self.frame]
        else:
            if self.sword_hit:
                self.image = self.images[self.last_dir_dict[self.last_dir][1]]
            elif self.Fire_arrow:
                self.image = self.images[self.last_dir_dict[self.last_dir][2]]
            else: 
                self.image = self.images[self.last_dir_dict[self.last_dir][0]]

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = pg.Rect(0, 0, 64, 96)
        self.hit_rect.center = self.rect.center

        self.get_keys()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.level.dt*self.speed_mul
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.level.barrier, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.level.barrier, 'y')
        self.rect.center = self.hit_rect.center

        self.sworddebouncestate+=1
        if self.sworddebouncestate>30:
            self.can_attack=True
            self.sworddebouncestate=0
        self.bowdebouncestate+=1
        if self.bowdebouncestate>50:
            self.can_fire_bow=True
            self.bowdebouncestate=0

class Barrier(pg.sprite.Sprite):
    def __init__(self,level,x,y,w,h):
        self.groups=level.barrier
        pg.sprite.Sprite.__init__(self, self.groups)
        self.level=level
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class switchlevel(pg.sprite.Sprite):
    def __init__(self,level,x,y,w,h,tolvl,newn):
        self.groups=level.switch_level
        pg.sprite.Sprite.__init__(self, self.groups)
        self.level=level
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.tolvl = tolvl
        self.newn=newn

class enterhouse(pg.sprite.Sprite):
    def __init__(self,level,x,y,w,h,tolvl,newn):
        self.groups=level.enter_house
        pg.sprite.Sprite.__init__(self, self.groups)
        self.level=level
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.tolvl = tolvl
        self.newn=newn

class mob(pg.sprite.Sprite):
    def __init__(self,level,x,y):
        self.layer = 1
        self.groups = level.all_sprites, level.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.level=level
        self.image = level.mob_img
        self.rect = self.image.get_rect()
        self.rect.center =(x,y)
        self.hit_rect = pg.Rect(0, 0, 64, 64).copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = 200
        self.speed = choice([150,100,75,125,150])
        self.target= level.player
        self.stright_walk=0
        self.dir={1:[180,(-1.5,0)],2:[270,(0,1.5)],3:[0,(1.5,0)],4:[90,(0,-1.5)]}
        self.track_player=False
        self.think=False
        self.think_timer=0
        self.dir_list=[1,2,3,4]
        self.curent_dir=choice(self.dir_list)

    def update(self):
        DETECT_RADIUS=300

        target_dist=self.target.pos - self.pos

        if target_dist.length_squared()< DETECT_RADIUS**2:
            self.track_player=True

        if self.track_player and target_dist.length_squared()>160000:
            self.track_player=False
            self.think=True

        if self.think:
            self.think_timer+=1
            if self.think_timer<30:
                self.rot=self.dir[1][0]
                self.image = pg.transform.rotate(self.level.mob_img, self.rot)
                self.rect.center = self.pos
            elif self.think_timer<60:
                self.rot=self.dir[2][0]
                self.image = pg.transform.rotate(self.level.mob_img, self.rot)
                self.rect.center = self.pos
            elif self.think_timer<90:
                self.rot=self.dir[3][0]
                self.image = pg.transform.rotate(self.level.mob_img, self.rot)
                self.rect.center = self.pos
            elif self.think_timer<120:
                self.rot=self.dir[4][0]
                self.image = pg.transform.rotate(self.level.mob_img, self.rot)
                self.rect.center = self.pos
            else:
                self.think=False
                self.think_timer=0
        else:
            if self.track_player:
                self.rot = (target_dist).angle_to(vec(1, 0))
                self.image = pg.transform.rotate(self.level.mob_img, self.rot)
                self.rect.center = self.pos
                self.acc = vec(1, 0).rotate(-self.rot)
                self.avoid_mobs()
                self.acc.scale_to_length(self.speed+0.001)
                self.acc += self.vel * -1
                self.vel += self.acc * self.level.dt
                self.pos += self.vel * self.level.dt + 0.5 * self.acc * self.level.dt ** 2
                self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.level.barrier, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.level.barrier, 'y')
                self.rect.center = self.hit_rect.center
                templist=list(self.dir_list)
                templist.remove(self.curent_dir)
                self.curent_dir=choice(templist)

            else:#npc random motion
                self.rot=self.dir[self.curent_dir][0]
                self.image = pg.transform.rotate(self.level.mob_img, self.rot)
                self.rect.center = self.pos
                self.avoid_mobs()
                self.pos += self.dir[self.curent_dir][1] 

                self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.level.barrier, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.level.barrier, 'y')
                self.rect.center = self.hit_rect.center
                self.stright_walk+=1

                if self.stright_walk>randint(200,350):
                    templist=list(self.dir_list)
                    templist.remove(self.curent_dir)
                    self.curent_dir=choice(templist)
                    self.stright_walk=0

        if self.health <=0:
            self.kill()

    def avoid_mobs(self):
        AVOID_RADIUS = 50

        for mob in self.level.mobs:
            if mob != self:
                dist = self.pos -mob.pos
                if 0< dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def draw_health(self):
        if self.health > 60:
            col = (0,255,0)
        elif self.health > 30:
            col = (255, 255, 0)
        else:
            col = (255,0,0)
        width = int(self.rect.width * self.health / 200)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < 200:
            pg.draw.rect(self.image, col, self.health_bar)

class BOSS(pg.sprite.Sprite):
    def __init__(self,level,x,y):
        self.layer = 1
        self.groups = level.all_sprites, level.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.level=level
        self.image = level.BOSS_img
        self.rect = self.image.get_rect()
        self.rect.center =(x,y)
        self.hit_rect = pg.Rect(0, 0, 200, 200).copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = 2000
        self.speed = 250
        self.target= level.player
        self.stright_walk=0
        self.dir={1:[180,(-1.5,0)],2:[270,(0,1.5)],3:[0,(1.5,0)],4:[90,(0,-1.5)]}
        self.track_player=False
        self.think=False
        self.think_timer=0
        self.dir_list=[1,2,3,4]
        self.curent_dir=choice(self.dir_list)

    def update(self):
        DETECT_RADIUS=1200

        target_dist=self.target.pos - self.pos

        if target_dist.length_squared()< DETECT_RADIUS**2:
            self.track_player=True

        if self.track_player and target_dist.length_squared()>1600000000000:
            self.track_player=False
            self.think=True

        if self.think:
            self.think_timer+=1
            if self.think_timer<30:
                self.rot=self.dir[1][0]
                self.image = pg.transform.rotate(self.level.BOSS_img, self.rot)
                self.rect.center = self.pos
            elif self.think_timer<60:
                self.rot=self.dir[2][0]
                self.image = pg.transform.rotate(self.level.BOSS_img, self.rot)
                self.rect.center = self.pos
            elif self.think_timer<90:
                self.rot=self.dir[3][0]
                self.image = pg.transform.rotate(self.level.BOSS_img, self.rot)
                self.rect.center = self.pos
            elif self.think_timer<120:
                self.rot=self.dir[4][0]
                self.image = pg.transform.rotate(self.level.BOSS_img, self.rot)
                self.rect.center = self.pos
            else:
                self.think=False
                self.think_timer=0
        else:
            if self.track_player:
                self.rot = (target_dist).angle_to(vec(1, 0))
                self.image = pg.transform.rotate(self.level.BOSS_img, self.rot)
                self.rect.center = self.pos
                self.acc = vec(1, 0).rotate(-self.rot)
                self.avoid_mobs()
                self.acc.scale_to_length(self.speed+0.001)
                self.acc += self.vel * -1
                self.vel += self.acc * self.level.dt
                self.pos += self.vel * self.level.dt + 0.5 * self.acc * self.level.dt ** 2
                self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.level.barrier, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.level.barrier, 'y')
                self.rect.center = self.hit_rect.center
                templist=list(self.dir_list)
                templist.remove(self.curent_dir)
                self.curent_dir=choice(templist)

            else:#npc random motion
                self.rot=self.dir[self.curent_dir][0]
                self.image = pg.transform.rotate(self.level.BOSS_img, self.rot)
                self.rect.center = self.pos
                self.avoid_mobs()
                self.pos += self.dir[self.curent_dir][1] 

                self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.level.barrier, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.level.barrier, 'y')
                self.rect.center = self.hit_rect.center
                self.stright_walk+=1

                if self.stright_walk>randint(200,350):
                    templist=list(self.dir_list)
                    templist.remove(self.curent_dir)
                    self.curent_dir=choice(templist)
                    self.stright_walk=0

        if self.health <=0:
            self.kill()
            self.level.gameend=True

    def avoid_mobs(self):
        AVOID_RADIUS = 50

        for mob in self.level.mobs:
            if mob != self:
                dist = self.pos -mob.pos
                if 0< dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def draw_health(self):
        if self.health > 1000:
            col = (0,255,0)
        elif self.health > 500:
            col = (255, 255, 0)
        else:
            col = (255,0,0)
        width = int(self.rect.width * self.health / 2000)
        self.health_bar = pg.Rect(0, 0, width, 20)
        if self.health < 2000:
            pg.draw.rect(self.image, col, self.health_bar)

class Sword(pg.sprite.Sprite):
    def __init__(self,level,pos,dir):
        self.groups = level.playersword
        pg.sprite.Sprite.__init__(self, self.groups)
        self.level = level
        self.created= pg.time.get_ticks()
        self.life=200

        if dir ==2:
            self.x = pos.x
            self.y = pos.y- 10
            self.rect = pg.Rect(self.x,self.y,100,20)
            self.rect.x = self.x
            self.rect.y = self.y
            self.hit_rect = self.rect

        elif dir ==3:
            self.x = pos.x
            self.y = pos.y
            self.rect = pg.Rect(self.x,self.y,30,80)
            self.rect.bottomleft = (self.x,self.y)        
            self.hit_rect = self.rect

        elif dir == 0:
            self.x = pos.x-27
            self.y = pos.y
            self.rect = pg.Rect(self.x,self.y,27,100)
            self.rect.x = self.x
            self.rect.y = self.y
            self.hit_rect = self.rect

        else:
            self.x = pos.x
            self.y = pos.y+10
            self.rect = pg.Rect(self.x,self.y,100,20)
            self.rect.bottomright = (self.x,self.y)
            self.hit_rect = self.rect
    def update(self):
        if pg.time.get_ticks()>self.created+self.life:
            self.kill()
            self.level.player.sword_hit=False

class Arrow(pg.sprite.Sprite):
    def __init__(self, level, pos, direction):
        self._layer = 2
        self.groups = level.all_sprites, level.Arrows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.level = level
        self.images = level.Arrow_imgs
        self.image=self.images[0]
        self.pos = vec(pos)
        self.dir=direction
        if direction==1:
            self.vel=(-10,0)
            self.image=self.images[1]
        elif direction==2:
            self.vel = (10,0)
            self.image=self.images[0]
        elif direction==3:
            self.vel = (0,-10)
            self.image=self.images[2]
        elif direction==0:
            self.vel=(0,10)
            self.image=self.images[3]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel 
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.level.barrier):
            self.vel=(0,0)
        if self.vel==(0,0):
            if pg.time.get_ticks() - self.spawn_time > 3000:
                self.kill()