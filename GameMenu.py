import tkinter as tk
import os
import sys
from threading import Timer

window_width = 1000
window_height = 1000
BackgroundColor = "#C4A484"
BackBlockColor = "#add8e6"
dir_path = os.path.dirname(os.path.realpath(__file__))

class CustomButton:
    btn = None
    ButtonDown = None
    ButtonUp = None
    action = None
    def __init__(self,buttonImage,pressedButtonImage,parent,x,y,action):
        self.ButtonDown = tk.PhotoImage(file=dir_path+"/Images/"+pressedButtonImage+".png")
        self.ButtonUp = tk.PhotoImage(file=dir_path+"/Images/"+buttonImage+".png")


        self.btn = tk.Label(parent,bd=0,bg=BackBlockColor)
        
        self.btn.config(image=self.ButtonUp)

        self.btn.place(relx=x,rely=y,anchor="s")
        self.btn.bind('<ButtonPress-1>',self.press)
        
        self.btn.bind('<ButtonRelease-1>',self.release)

        self.action = action

    def press(self,event):
        self.btn.config(image=self.ButtonDown)
        t = Timer(0.2, self.action)
        t.start()


    def release(self,event):
        self.btn.config(image=self.ButtonUp)
#exit app
def quitApp():

    os._exit(1)
#MainFinction
def ShowMenu():
    window = tk.Tk()
    window.title("Vrhcáby")
    #set background color
    window.config(bg=BackgroundColor)
    #set size of window
    window.geometry(str(window_width) + "x" + str(window_height))


    greeting = tk.Label(text=dir_path)



    #Load Images
    backImage = tk.PhotoImage(file=dir_path+"/Images/Back.png")
    MenuImage = tk.PhotoImage(file=dir_path+"/Images/MenuLabel.png")
    #Set Menu
    Title = tk.Label(window,bd=0,bg=BackgroundColor,text="Vrhcáby",font=("Courier", 60))
    Title.place(relx=0.5,rely=0.1,anchor="center")
    back = tk.Label(window,bd=0,bg=BackgroundColor)
    back.config(image=backImage)
    back.place(relx=0.5,rely=0.6,anchor="center")
    MenuLabel = tk.Label(window,bd=0,bg=BackBlockColor)
    MenuLabel.config(image=MenuImage)
    MenuLabel.place(relx=0.5,rely=0.33,anchor="center")
    PlayButton =  CustomButton("PlayButton","PlayButtonDown",window,0.5,0.55,None)
    PlayButton =  CustomButton("SettingsButton","SettingsButtonDown",window,0.5,0.70,None)
    PlayButton =  CustomButton("QuitButton","QuitButtonDown",window,0.5,0.85,quitApp)

    window.mainloop()


ShowMenu()















































