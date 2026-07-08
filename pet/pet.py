import tkinter as tk
import time


# self.frames = ["frame1.png", "frame2.png"]
class Pet():
    # constructor for pet
    def __init__(self):

        # create a window
        self.window = tk.Tk()

        # by putting self before the variables, we can access them in other functions
        # if not, they only exist in this function
        
        self.default_idle_frames = self.load_frames("assets/default_idle", "idle_default_det", 2)
        self.crossed_arms_idle_frames = self.load_frames("assets/crossed_arms_idle", "idle_detective", 2)
        self.walking_left_frames = self.load_frames("assets/walking_left", "walking_left", 7)
        self.walking_right_frames = self.load_frames("assets/walking_right", "walking_right", 7)

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
    
    # function to load frames for animation
    def load_frames(self,folder,state_name,amount):

        # range starts at 0, so we add 1 to i to get the correct frame number
        for i in range(amount):
            return [tk.PhotoImage(file=f"{folder}/spr_{state_name}{i+1}.png")]
