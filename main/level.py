import pygame as pg
import pickle
import sys
import time
from tilemap import *
from objects import *

#--------------------------------------------

class Level:
        def __init__(self,levelid,cur,con):
                with open("config.dat",'rb') as file:
                        res=pickle.load(file)
                        w_w,w_h=res[0]
                        w_full_screen=res[1]
                pg.init()
                if w_full_screen:
                        self.screen=pg.display.set_mode((w_w,w_h),pg.FULLSCREEN)
                else:
                        self.screen=pg.display.set_mode((w_w,w_h))
                pg.display.set_caption("GreensVile")
                self.w_w=w_w
                self.w_h=w_h
                self.clock=pg.time.Clock()
                self.level_id=levelid
                self.gotolvl=''
                cur.execute("select * from playerdata")
                playerdata=list(cur.fetchone())
                self.playerdata=playerdata
                self.cur=cur
                self.con=con
                self.gameend=False

        def load_data(self):
                #map------
                with open('levelmaps.dat','rb') as file:
                        levelmaps=pickle.load(file)
                lvl_map=levelmaps[self.level_id]	        
                self.map = TiledMap('map//'+lvl_map)
                self.map_img = self.map.make_map()
                self.map_rect = self.map_img.get_rect()
                #---------
                with open('controls.dat','rb') as f:
                        self.controls = pickle.load(f)
                #player---
                self.player_imgs=[]
                for i in ['down','left','right','up']:
                        for x in ['1','2','3','4','5','6','7','8','sword','bow']:
                                self.player_imgs.append(pg.image.load(f'player/{i}{x}.png'))

                #---------

                #game_objects
                self.font="img/HyliaSerifBeta-Regular.otf"
                self.dim_bg=pg.Surface(self.screen.get_size()).convert_alpha()
                self.dim_bg.fill((0,0,0,180))
                self.Arrow_imgs=[pg.image.load('img/arrowr.png'),pg.image.load('img/arrowl.png'),pg.image.load('img/arrowu.png'),pg.image.load('img/arrowd.png')]
                self.checkpointstatic=pg.image.load('img/checkpointstatic.png')
                self.checkpoint_active_imgs=[pg.image.load('img/checkpointactive1.png'),pg.image.load('img/checkpointactive2.png'),pg.image.load('img/checkpointactive3.png'),pg.image.load('img/checkpointactive4.png'),pg.image.load('img/checkpointactive5.png')]
                self.openchest=pg.image.load('img/openchest.png')
                self.openchestcoin=pg.image.load('img/openchestcoin.png')
                self.closedchest=pg.image.load('img/closedchest.png')
                self.mob_img = pg.image.load('img/mob.png').convert_alpha()
                self.BOSS_img = pg.image.load('img/BOSS.png').convert_alpha()
                #---------
                self.hud_use=False #FOR FUTURE ENHANCEMENTS
                self.healthbar_img= pg.image.load('img/healthbar.png')
                #---------

        def new(self):

                #sprite_groups--------
                self.all_sprites = pg.sprite.LayeredUpdates()
                self.player = pg.sprite.Group()
                self.playersword = pg.sprite.Group()
                self.Arrows=pg.sprite.Group()
                self.mobs = pg.sprite.Group()
                self.barrier = pg.sprite.Group()
                self.switch_level= pg.sprite.Group()
                self.enter_house= pg.sprite.Group()
                #---------------------

                #map_objects----------
                for tile_object in self.map.tmxdata.objects:
                        if tile_object.name == 'barrier':
                                Barrier(self,tile_object.x, tile_object.y,tile_object.width, tile_object.height)
                        if tile_object.name == 'checkpoint':
                                if tile_object.n==self.playerdata[0]:
                                        self.player = Player(self, tile_object.x+30, tile_object.y+2)
                                        self.player.health=self.playerdata[1]
                                        self.player.last_dir=self.playerdata[2]
                                        self.player.has_sword=self.playerdata[4]#FOR FUTURE ENHANCEMENTS
                                        self.player.has_bow=self.playerdata[5]#FOR FUTURE ENHANCEMENTS
                                        self.player.arrows=self.playerdata[6]#FOR FUTURE ENHANCEMENTS
                        if tile_object.name == 'mob':
                                mob(self,tile_object.x,tile_object.y)
                        if tile_object.name == 'boss':
                                BOSS(self,tile_object.x,tile_object.y)
                        if tile_object.name == 'shift':
                                switchlevel(self,tile_object.x, tile_object.y,tile_object.width, tile_object.height,tile_object.tolvl,tile_object.newn)
                        
                        if tile_object.name == 'shifth':
                                enterhouse(self,tile_object.x, tile_object.y,tile_object.width, tile_object.height,tile_object.tolvl,tile_object.newn)
                #---------------------
                self.paused = False
                self.camera = Camera(self.map.width,self.map.height)

        def run(self):
                
                self.playing = True
                self.gameover = False
                while self.playing:
                        self.dt = self.clock.tick(60)/1000
                        self.events()
                        if not self.paused:
                                self.update()
                        self.draw()

                if self.gameend:
                        self.cur.execute("update playerdata set checkpoint = 1")
                        self.cur.execute("update playerdata set health = 100")
                        self.cur.execute("update playerdata set lastdir = 0")
                        self.cur.execute("update playerdata set tolvl = '1'")
                        '''
                        --------------FOR FUTURE ENHANCEMENTS----------------
                        self.cur.execute("update playerdata set hassword = 1")
                        self.cur.execute("update playerdata set hasbow = 1")
                        self.cur.execute("update playerdata set arrow = 20")
                        '''
                        self.con.commit()
                        return '1'

                if not self.gameover:
                        self.cur.execute(f"update playerdata set checkpoint = {self.playerdata[0]}")
                        self.cur.execute(f"update playerdata set health = {self.playerdata[1]}")
                        self.cur.execute(f"update playerdata set lastdir = {self.playerdata[2]}")
                        self.cur.execute(f"update playerdata set tolvl = '{self.playerdata[3]}'")
                        self.cur.execute(f"update playerdata set hassword = {self.playerdata[4]}")#FOR FUTURE ENHANCEMENTS
                        self.cur.execute(f"update playerdata set hasbow = {self.playerdata[5]}")#FOR FUTURE ENHANCEMENTS
                        self.cur.execute(f"update playerdata set arrow = {self.playerdata[6]}")#FOR FUTURE ENHANCEMENTS
                        self.con.commit()
                        return self.gotolvl
                else:
                        return self.level_id

        def update(self):
                #---------------------
                self.all_sprites.update()
                self.playersword.update()
                self.camera.update(self.player)
                #---------------------
                hits = pg.sprite.spritecollide(self.player,self.switch_level,False,False)
                for hit in hits:
                        self.gotolvl=str(hit.tolvl)
                        self.playerdata[0]=hit.newn
                        self.playerdata[1]=self.player.health
                        self.playerdata[2]=self.player.last_dir
                        self.playerdata[3]=str(hit.tolvl)
                        self.playing = False
                #---------------------
                hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
                for hit in hits:
                    self.player.health -= 5
                    hit.vel = vec(0, 0) - vec(20, 0).rotate(-hits[0].rot)
                    if self.player.health <= 0:
                        self.playing = False
                        self.gameover= True
                #---------------------
                hits = pg.sprite.groupcollide(self.mobs,self.playersword,False,False)
                for hit in hits:
                    hit.health -= self.player.sword_damage
                    hit.vel = vec(0, 0)
                hits = pg.sprite.groupcollide(self.mobs,self.Arrows,False,True)
                for hit in hits:
                        hit.health -= self.player.bow_damage
                        hit.vel = vec(0,0)
                #---------------------
                keys = pg.key.get_pressed()
                hits = pg.sprite.spritecollide(self.player,self.enter_house,False,False)
                if hits:
                        self.hud_use=True
                else:
                        self.hud_use=False
                for hit in hits:
                        if keys[self.controls[(5,1)][1]] or keys[self.controls[(5,2)][1]]:
                                self.gotolvl=str(hit.tolvl)
                                self.playerdata[0]=hit.newn
                                self.playerdata[1]=self.player.health
                                self.playerdata[2]=self.player.last_dir
                                self.playerdata[3]=str(hit.tolvl)
                                self.playing = False
                                
                #---------------------
                if self.gameend:
                        self.playing=False

        def draw(self):
                pg.display.set_caption("GreensVile")
                self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
                for sprite in self.all_sprites:
                        if isinstance(sprite, mob):
                                sprite.draw_health()
                        if isinstance(sprite, BOSS):
                                sprite.draw_health()

                        self.screen.blit(sprite.image, self.camera.apply(sprite))
                
                if self.hud_use:
                        # FOR FUTURE DEVELEPMENT OF GAME HUD AND GUI FOR INTERACTING WITH GAME OBJECTS
                        pass
                #-------------------------------------------------------------------
                draw_player_health(self.screen,58,20,self.player.health/100)
                draw_player_stamina(self.screen,45,63,self.player.stamina/100)
                self.screen.blit(self.healthbar_img,(0,1))
                #-------------------------------------------------------------------
                if self.paused:
                        self.screen.blit(self.dim_bg,(0,0))
                        draw_text(self,"Paused",self.font,100,(255,255,255),self.w_w/2,self.w_h/2)
                pg.display.update()

        def events(self):
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                                sys.exit()
                        if event.type == pg.KEYDOWN:
                                if event.key == pg.K_ESCAPE:
                                        pg.quit()
                                        sys.exit()
                                if self.player.has_sword and self.player.can_attack:
                                        if event.key == self.controls[(6,1)][1] or event.key == self.controls[(6,2)][1]:
                                                self.player.sword_hit = True
                                                self.player.sword = Sword(self,self.player.pos,self.player.last_dir)
                                                self.player.run = False
                                                self.player.can_attack=False
                                if self.player.has_bow and self.player.can_fire_bow:
                                        if event.key == self.controls[(7,1)][1] or event.key == self.controls[(7,2)][1]:
                                                self.player.Fire_arrow = True
                                                self.player.arrow = Arrow(self, self.player.pos, self.player.last_dir)
                                                #self.player.inventory['arrows']-=1
                                                self.player.run = False
                                                self.player.can_fire_bow=False
                                if event.key == pg.K_p:
                                        self.paused = not self.paused

                        if event.type == pg.KEYUP:
                                if self.player.has_sword:
                                        if event.key == self.controls[(6,1)][1] or event.key == self.controls[(6,2)][1]:
                                                self.player.sword_hit = False
                                if self.player.has_bow:
                                        if event.key == self.controls[(7,1)][1] or event.key == self.controls[(7,2)][1]:
                                                self.player.Fire_arrow = False

        def Gameover(self):
                self.screen.fill((0,0,0))
                draw_text(self,"GAME OVER",self.font,100,(255,0,0),self.w_w/2,self.w_h/2)
                draw_text(self,"Press E to reload from last checkpoint",self.font,20,(255,255,255),self.w_w/2,self.w_h*0.75)
                pg.display.flip()
                waiting = True
                while waiting:
                        self.clock.tick(60)
                        for event in pg.event.get():
                                if event.type == pg.QUIT:
                                        waiting = False
                                        pg.quit()
                                        sys.exit()
                                if event.type == pg.KEYUP:
                                        if event.key == pg.K_e:
                                                waiting = False

        def Gameend(self):
                self.screen.fill((0,0,0))
                draw_text(self,"YOU WON",self.font,100,(255,0,0),self.w_w/2,self.w_h/2)
                draw_text(self,"Press E to replay the game",self.font,20,(255,255,255),self.w_w/2,self.w_h*0.75)
                pg.display.flip()
                waiting = True
                while waiting:
                        self.clock.tick(60)
                        for event in pg.event.get():
                                if event.type == pg.QUIT:
                                        waiting = False
                                        pg.quit()
                                        sys.exit()
                                if event.type == pg.KEYUP:
                                        if event.key == pg.K_e:
                                                waiting = False

