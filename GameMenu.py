import tkinter as tk
import os
import sys
from threading import Timer

window_width = 1000
window_height = 1000
background_color = "#C4A484"
back_block_color = "#add8e6"
dir_path = os.path.dirname(os.path.realpath(__file__))


class CustomButton:
    button = None
    button_down = None
    button_up = None
    action = None
    def __init__(self, button_image, pressed_button_image, parent, x, y, action):
        self.button_down = tk.PhotoImage(file=dir_path+"/Images/"+pressed_button_image+".png")
        self.button_up = tk.PhotoImage(file=dir_path+"/Images/"+button_image+".png")
        self.button = tk.Label(parent, bd=0, bg=back_block_color)
        self.button.config(image=self.button_up)
        self.button.place(relx=x, rely=y, anchor="s")
        self.button.bind('<ButtonPress-1>', self.press)
        self.button.bind('<ButtonRelease-1>', self.release)
        self.action = action


    def press(self, event):
        self.button.config(image=self.button_down)
        timer = Timer(0.2, self.action)
        timer.start()



    def release(self,event):
        self.button.config(image=self.button_up)


#exit app
def quit_app():
    os._exit(1)

def save_game():
    print("Saving game...")

def load_game():
    print("Loading game...")

def show_menu():
    # initialize window
    window = tk.Tk()
    window.title("Vrhcáby")
    window.resizable(False, False)
    # set background color
    window.config(bg=background_color)
    # set size of window
    window.geometry(f"{window_width}x{window_height}")
    # create a menubar
    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)
    # create the file_menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    # add menu items to the File menu
    file_menu.add_command(label='Save',command=save_game)
    file_menu.add_command(label='Load',command=load_game)
    file_menu.add_separator()
    file_menu.add_command(label='Close')
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=window.quit)

    # create the Help menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)

        # add menu items to the Help menu
    help_menu.add_command(label='Welcome')
    help_menu.add_command(label='About...')


    file_menu.entryconfig(0,state=tk.DISABLED)

    # Load Images
    back_image = tk.PhotoImage(file=dir_path + "/Images/Back.png")
    menu_image = tk.PhotoImage(file=dir_path + "/Images/MenuLabel.png")

    # Set Menu
    title_label = tk.Label(window, bd=0, bg=background_color, text="Vrhcáby", font=("Courier", 60))
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    back_label = tk.Label(window, bd=0, bg=background_color, image=back_image)
    back_label.place(relx=0.5, rely=0.6, anchor="center")

    menu_label = tk.Label(window, bd=0, bg=background_color, image=menu_image)
    menu_label.place(relx=0.5, rely=0.33, anchor="center")

    # Create Buttons
    buttons = [("PlayButton", "PlayButtonDown", 0.55, None),
            ("SettingsButton", "SettingsButtonDown", 0.70, None),
            ("QuitButton", "QuitButtonDown", 0.85, quit_app)]

    for button in buttons:
        custom_button = CustomButton(button[0], button[1], window, 0.5, button[2], button[3])


    window.mainloop()


show_menu()















































