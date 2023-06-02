import tkinter as tk
import os
from threading import Timer
import datetime
background_color = "#C4A484"
back_block_color = "#add8e6"
dir_path = os.path.dirname(os.path.realpath(__file__))


class WinWindow:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Game Over!")
        self.window.geometry("800x800")
        self.window.config(background=back_block_color)

    def run(self):
        self.window.mainloop()

win_ui = WinWindow()

class CustomButton:
    button = None
    button_down = None
    button_up = None
    action = None

    def __init__(self, button_image, pressed_button_image, parent, x, y, action):
        self.button_down = tk.PhotoImage(file=dir_path + "/Images/" + pressed_button_image + ".png")
        self.button_up = tk.PhotoImage(file=dir_path + "/Images/" + button_image + ".png")
        self.button = tk.Label(parent, bd=0, bg=back_block_color)
        self.button.config(image=self.button_up)
        self.button.place(relx=x, rely=y, anchor="center")
        self.button.bind("<ButtonPress-1>", self.press)
        self.button.bind("<ButtonRelease-1>", self.release)
        self.action = action

    def press(self, event):
        self.button.config(image=self.button_down)
        timer = Timer(0.2, self.action)
        timer.start()

    def release(self, event):
        self.button.config(image=self.button_up)


class Text:

    def __init__(self, parent, height ,text, color, size, font_style, x, y):
        self.label = tk.Label(parent, height=height, fg=color, text=text, font=("Default", size, font_style))
        self.label.pack(padx=20, pady=20)
        self.label.place(relx=x, rely=y, anchor=None)
        self.label.config(background=back_block_color)

                                                # kterej hráč zvítězil
First_level_heading = Text(win_ui.window, 3, "Hráč zvítězil!", "White", 40, "bold", None, None)
text = Text(win_ui.window, 2, "Tentokrát se ti to nepovedlo...", "White", 20, "normal", None, None)
footer = Text(win_ui.window, 2, "Vrhcáby", "Grey", 14, "normal", 0.45, 0.95)
date = Text(win_ui.window, 2, datetime.datetime.now().strftime('%H:%M:%S'), "Grey", 14, "normal", 0.90, 0.95)


btn = CustomButton("PlayButton", "PlaybuttonDown", win_ui.window, 0.30, 0.55, None) #OK button
btn2 = CustomButton("PlayButton", "PlaybuttonDown", win_ui.window, 0.70, 0.55, None) #Repeat button

win_ui.run()