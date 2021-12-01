import pygame as pg
import sqlite3
from options import options_func
from level import *
import pickle
#------------------------------------------
w_w=600
w_h=800
#------------------------------------------

pg.init()
Launcher_window=pg.display.set_mode((w_w,w_h))
pg.display.set_caption('GreensVile Launcher')
clock= pg.time.Clock()
con=sqlite3.connect("playerdata.db")
cur=con.cursor()
#-------------------------------------------
Launcher_background = pg.transform.scale(pg.image.load("launcher_screen.png"),(w_w,w_h))
controls_screen_bg=pg.image.load("Controls_screen.png")

play_img=pg.image.load("play.png")
play_img_rect=play_img.get_rect()
play_img_rect.center=(300,300)

controls_img=pg.image.load("controls.png")
controls_img_rect=controls_img.get_rect()
controls_img_rect.center=(300,400)

options_img=pg.image.load("options.png")
options_img_rect=options_img.get_rect()
options_img_rect.center=(300,500)

exit_img=pg.image.load("exit.png")
exit_img_rect=exit_img.get_rect()
exit_img_rect.center=(300,600)

pointer_img=pg.image.load("pointer.png")
pointer_img_rect=pointer_img.get_rect()
pointer_img_rect.center=(200,300)

controls_selector_img=pg.image.load("Controls_selector.png")
controls_selector_img_rect=controls_selector_img.get_rect()
controls_selector_img_rect.center=(486,203)
#-------------------------------------------
def text(text,font,size,colour,x,y,surf):
    Font= pg.font.Font(font,size)
    textbox=Font.render ( text,True,colour)
    textRect=textbox.get_rect()
    textRect.center=(x,y)
    surf.blit(textbox,textRect)
def display(image,x,y):
    Launcher_window.blit(image,(x,y))
def displayr(image,rect):
    Launcher_window.blit(image,rect)
#--------------------------------------------

def main():
    #--------------------------------------------------------
    def play():
        cur.execute("select * from playerdata")
        playerdata=list(cur.fetchone())
        current_level=playerdata[3]
        while True:
            l=Level(current_level,cur,con)
            l.load_data()
            l.new()
            current_level=l.run()
            if l.gameover:
                l.Gameover()
            if l.gameend:
                l.Gameend()

    #--------------------------------------------------------
    def controls():
        c_selector=(1,1)
        c_select_pos={(1,1):(340,130),(1,2):(486,130),
        			  (2,1):(340,203),(2,2):(486,203),
        			  (3,1):(340,271),(3,2):(486,271),
        			  (4,1):(340,340),(4,2):(486,340),
        			  (5,1):(340,410),(5,2):(486,410),
        			  (6,1):(340,482),(6,2):(486,482),
        			  (7,1):(340,560),(7,2):(486,560),
        			  (8,1):(340,634),(8,2):(486,634),
        			  (9,1):(523,765),(9,2):(523,765)}
        with open("controls.dat","rb") as file:
                controls_dict=pickle.load(file)  
        
        active=False
        run_controls=True
        display_selector=True

        while run_controls:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                	if not active:
	                	if event.key==pg.K_UP or event.key==pg.K_w:
	                		if c_selector[0]!=1:
	                			c_selector=(c_selector[0]-1,c_selector[1])
	                	elif event.key==pg.K_DOWN or event.key==pg.K_s:
	                		if c_selector[0]!=9:
	                			c_selector=(c_selector[0]+1,c_selector[1])
	                	elif event.key in [pg.K_LEFT,pg.K_a]:
	                		if c_selector[1]!=1:
	                			c_selector=(c_selector[0],c_selector[1]-1)
	                	elif event.key in [pg.K_RIGHT,pg.K_d]:
	                		if c_selector[1]!=2: 
	                			c_selector=(c_selector[0],c_selector[1]+1)
	                	elif event.key in [pg.K_e,pg.K_RETURN,pg.K_SPACE]:
	                		if c_selector[0]==9:
	                			run_controls=False
	                			with open("controls.dat",'wb') as file:
	                				pickle.dump(controls_dict,file)

	                		else:
	                			active = True
	                			blink=0
	                else:
	                	controls_dict[c_selector]=[pg.key.name(event.key).upper(),event.key]
	                	active=False
	                	blink=0
	                	display_selector=True
            if active:
            	blink+=1
            	if blink>60:
            		blink=0
            	if blink<30:
            		display_selector=True
            	else:
            		display_selector=False

            controls_selector_img_rect.center=c_select_pos[c_selector]
            display(controls_screen_bg,0,0)
            if display_selector:
            	displayr(controls_selector_img,controls_selector_img_rect)

            for i in c_select_pos:
            	if i[0]!=9:
            		x,y=c_select_pos[i][0],c_select_pos[i][1]
            		textstring=controls_dict[i][0]
            		if len(textstring)>8:
            			text(textstring,'freesansbold.ttf',20,(71,98,128),x,y,Launcher_window)
            		else:
            			text(textstring,'freesansbold.ttf',26,(71,98,128),x,y,Launcher_window)
            	else:
            		pass

            pg.display.update()
    #--------------------------------------------------------
    
    pointer=0
    pointer_pos={0:(200,300),1:(200,400),2:(200,500),3:(200,600)}
    
    #--------------------------------------------------------
    run=True
    while run:
        pointer_img_rect.center=pointer_pos[pointer]   

        display(Launcher_background,0,0)
        displayr(play_img,play_img_rect)
        displayr(controls_img,controls_img_rect)
        displayr(options_img,options_img_rect)
        displayr(exit_img,exit_img_rect)
        displayr(pointer_img,pointer_img_rect)
        
        pg.display.update()        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key==pg.K_UP or event.key==pg.K_w:
                    if pointer !=0:
                        pointer-=1
                elif event.key==pg.K_DOWN or event.key==pg.K_s:
                    if pointer !=3:
                        pointer+=1
                elif event.key in [pg.K_e,pg.K_RETURN,pg.K_SPACE]:
                	if pointer==0:
                		play()
                		pg.quit()
                		run=False
                	elif pointer==1:
                		controls()
                	elif pointer==2:
                		options_func()
                	else:
                		pg.quit()
                		quit()


        clock.tick(60)
    #--------------------------------------------------------

main()