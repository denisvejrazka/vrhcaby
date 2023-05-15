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

def SaveGame():
    
    print("Save")
def LoadGame():

    print("Load")
#MainFinction
def ShowMenu():
    #init window
    window = tk.Tk()
    window.title("Vrhcáby")
    #set background color
    window.config(bg=BackgroundColor)
    #set size of window
    window.geometry(str(window_width) + "x" + str(window_height))


    





    # create a menubar
    menubar = tk.Menu(window)
    window.config(menu=menubar)

    # create the file_menu
    file_menu = tk.Menu(
        menubar,
        tearoff=0
    )

    # add menu items to the File menu
    file_menu.add_command(label='Save',command=SaveGame)
    file_menu.add_command(label='Load',command=LoadGame)
    file_menu.add_command(label='Close')
    
    file_menu.add_separator()
    
    # add Exit menu item
    file_menu.add_command(
        label='Exit',
        command=quitApp
    )

    # add the File menu to the menubar
    menubar.add_cascade(
        label="File",
        menu=file_menu
    )
    # create the Help menu
    help_menu = tk.Menu(
        menubar,
        tearoff=0
    )

    help_menu.add_command(label='Welcome')
    help_menu.add_command(label='About...')

    # add the Help menu to the menubar
    menubar.add_cascade(
        label="Help",
        menu=help_menu
    )



    file_menu.entryconfig(0,state=tk.DISABLED)



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















































