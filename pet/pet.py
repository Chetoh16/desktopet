import tkinter as tk
import time


default_idle_frames = ["assets/default_idle/spr_idle_default_det1.png", "assets/default_idle/spr_idle_default_det2.png"]
crossed_arms_idle_frames = ["assets/crossed_arms_idle/spr_idle_detective1.png", "assets/crossed_arms_idle/spr_idle_detective2.png"]
walking_left_frames = ["assets/walking_left/spr_walking_left.1.png", "assets/walking_left/spr_walking_left2.png",  "assets/walking_left/spr_walking_left3.png", "assets/walking_left/spr_walking_left4.png", "assets/walking_left/spr_walking_left5.png", "assets/walking_left/spr_walking_left6.png", "assets/walking_left/spr_walking_left7.png"]
walking_right_frames = ["assets/walking_right/spr_walking_right1.png", "assets/walking_right/spr_walking_right2.png", "assets/walking_right/spr_walking_right3.png", "assets/walking_right/spr_walking_right4.png", "assets/walking_right/spr_walking_right5.png", "assets/walking_right/spr_walking_right6.png", "assets/walking_right/spr_walking_right7.png"]

# self.frames = ["frame1.png", "frame2.png"]
class Pet():
    # constructor for pet
    def __init__(self):

        # create a window
        self.window = tk.Tk()

        # placeholder
        self.img = tk.PhotoImage(file="assets/default_idle/spr_idle_default_det1.png")

        # set focushighlight to black when the window does not have focus
        self.window.config(highlightbackground='black')

        # make window frameless
        self.window.overrideredirect(True)

        # make window draw over all others
        self.window.attributes('-topmost', True)

        # turn black into transparency
        self.window.wm_attributes('-transparentcolor', 'black')

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg='black')

        # create a window of size 128x128 pixels, at coordinates 0,0

        self.x = 0
        self.window.geometry('64x64+{x}+0'.format(x=str(self.x)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()

    def update(self):

        # create the window
        self.window.geometry('64x64+{x}+0'.format(x=str(self.x)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

        # call update after 10ms
        self.window.after(10, self.update)


