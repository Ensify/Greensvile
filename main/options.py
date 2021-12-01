from tkinter import *
import pickle

widthlabel1,widthentry1,heightlabel1,heightentry1=0,0,0,0
Fullscreenvalue=False
exitvalues=([800,600],Fullscreenvalue)

def options_func():

    def disablethings():
        global widthlabel1,widthentry1,heightlabel1,heightentry1
        if defaultrescheck.get()==1:
            widthlabel1 = Label(customresframe, text="Width:",state="disabled")
            widthlabel1.grid(row=0,column=0,padx=5)
            heightlabel1 = Label(customresframe, text="Height:",state="disabled")
            heightlabel1.grid(row=1,column=0,padx=5)
            widthentry1=Entry(customresframe,state="disabled")
            widthentry1.grid(row=0,column=1,padx=5)
            widthentry1.insert(0,"1024")
            heightentry1=Entry(customresframe,state="disabled")
            heightentry1.grid(row=1,column=1,padx=5)
            heightentry1.insert(0,"768")
            Radiobutton(defaultresframe,text="1920 x 1080",variable=defaultresolutionid,value=1).grid(row=0,sticky=W)
            Radiobutton(defaultresframe,text="1600 x 900 ",variable=defaultresolutionid,value=2).grid(row=1,sticky=W)
            Radiobutton(defaultresframe,text="1366 x 768 ",variable=defaultresolutionid,value=3).grid(row=2,sticky=W)
            Radiobutton(defaultresframe,text="1280 x 800 ",variable=defaultresolutionid,value=4).grid(row=3,sticky=W)
        else:
            widthlabel1 = Label(customresframe, text="Width:")
            widthlabel1.grid(row=0,column=0,padx=5)
            heightlabel1 = Label(customresframe, text="Height:")
            heightlabel1.grid(row=1,column=0,padx=5)
            widthentry1=Entry(customresframe)
            widthentry1.grid(row=0,column=1,padx=5)
            widthentry1.insert(0,"1024")
            heightentry1=Entry(customresframe)
            heightentry1.grid(row=1,column=1,padx=5)
            heightentry1.insert(0,"768")
            Radiobutton(defaultresframe,text="1920 x 1080",variable=defaultresolutionid,value=1,state="disabled").grid(row=0,sticky=W)
            Radiobutton(defaultresframe,text="1600 x 900 ",variable=defaultresolutionid,value=2,state="disabled").grid(row=1,sticky=W)
            Radiobutton(defaultresframe,text="1366 x 768 ",variable=defaultresolutionid,value=3,state="disabled").grid(row=2,sticky=W)
            Radiobutton(defaultresframe,text="1280 x 800 ",variable=defaultresolutionid,value=4,state="disabled").grid(row=3,sticky=W)

    root = Tk()
    root.title('OPTIONS')
    res_mainframe = LabelFrame(root,text="Resolution",padx=10,pady=5)
    res_mainframe.grid(row=0,sticky=W,padx=10,pady = 5)
    defaultrescheck = IntVar()
    checkdefaultres = Checkbutton(res_mainframe,text="Use Default Resolutions", variable = defaultrescheck,onvalue=1,offvalue=0,command=disablethings)
    checkdefaultres.select()
    checkdefaultres.grid(row=0,column=0,sticky=W)
    defaultresframe = LabelFrame(res_mainframe,text="Choose a Resolution")
    defaultresframe.grid(row=1,column=0,sticky=W)

    defaultresolutionid = IntVar()
    Radiobutton(defaultresframe,text="1920 x 1080",variable=defaultresolutionid,value=1).grid(row=0,sticky=W)
    Radiobutton(defaultresframe,text="1600 x 900 ",variable=defaultresolutionid,value=2).grid(row=1,sticky=W)
    Radiobutton(defaultresframe,text="1366 x 768 ",variable=defaultresolutionid,value=3).grid(row=2,sticky=W)
    Radiobutton(defaultresframe,text="1280 x 800 ",variable=defaultresolutionid,value=4).grid(row=3,sticky=W)

    customresframe = LabelFrame(res_mainframe,text="Enter a Resolution")
    customresframe.grid(row=2,sticky=W)
    widthlabel = Label(customresframe, text="Width:",state="disabled")
    widthlabel.grid(row=0,column=0,padx=5)
    heightlabel = Label(customresframe, text="Height:",state="disabled")
    heightlabel.grid(row=1,column=0,padx=5)
    widthentry=Entry(customresframe,state="disabled")
    widthentry.grid(row=0,column=1,padx=5)
    widthentry.insert(0,"1024")
    heightentry=Entry(customresframe,state="disabled")
    heightentry.grid(row=1,column=1,padx=5  )
    heightentry.insert(0,"768")

    def Fullscreen():
        global Fullscreenvalue
        if fullscreencheck.get()==1:
            Fullscreenvalue=True
        else:
            Fullscreenvalue=False

    fullscreencheck = IntVar()
    checkfullscreen = Checkbutton(res_mainframe,text="Fullscreen", variable = fullscreencheck,onvalue=1,offvalue=0,command=Fullscreen)
    checkfullscreen.deselect()
    checkfullscreen.grid(row=3,column=0,sticky=W)

    def getres(text=True):
        if defaultrescheck.get()==1:
            if defaultresolutionid.get()==1:
                res=[1920,1080]
            elif defaultresolutionid.get()==2:
                res=[1600,900]
            elif defaultresolutionid.get()==3:
                res=[1366,768]
            else:
                res=[1280,800]
        else:
            x=int(widthentry1.get())
            y=int(heightentry1.get())
            res=[x,y]
        if text==True:
            return str(res[0])+' x '+str(res[1])
        else:
            return res

    def curres():
        with open("config.dat",'rb') as file:
            return pickle.load(file)

    currentres=Label(root,text=f"Current Resolution is {curres()[0][0]}x{curres()[0][1]}")
    currentres.grid(row=3)

    def Applyresget():
        global exitvalues
        Applyres= getres(text=False)
        exitvalues=(Applyres,Fullscreenvalue)
        with open("config.dat",'wb') as file:
            pickle.dump(exitvalues,file)
        root.destroy()

    Applyresbutton=Button(root,text="Apply selected Resolution",command=Applyresget)
    Applyresbutton.grid(row=4)
    root.resizable(0,0)
    root.mainloop()
