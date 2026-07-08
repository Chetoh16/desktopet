import tkinter as tk
import time
from enum import Enum



class PetState(Enum):
    IDLE = "idle"
    WAITING = "waiting"
    WALKING_LEFT = "walking_left"
    WALKING_RIGHT = "walking_right"
    

# Add boolean running for increasing speed 

class Pet():
    # constructor for pet
    def __init__(self):

        # create a window
        self.window = tk.Tk()

        # by putting self before the variables, we can access them in other functions
        # if not, they only exist in this function
        
        # load all animation frames for each state
        self.default_idle_frames = self.load_frames("assets/default_idle", "idle_default_det", 2)
        self.crossed_arms_idle_frames = self.load_frames("assets/crossed_arms_idle", "idle_detective", 2)
        self.walking_left_frames = self.load_frames("assets/walking_left", "walking_left", 7)
        self.walking_right_frames = self.load_frames("assets/walking_right", "walking_right", 7)

        self.state = PetState.IDLE

        # current frame of the animation, used to cycle through frames
        self.frame_index = 0

        # dictionary to hold the frames for each state
        self.animations = {
            PetState.IDLE: self.default_idle_frames,
            PetState.WAITING: self.crossed_arms_idle_frames,
            PetState.WALKING_LEFT: self.walking_left_frames,
            PetState.WALKING_RIGHT: self.walking_right_frames
        }
        

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

        # create a window of size 64x64 pixels, at coordinates 0,0
        self.x = 0
        self.window.geometry('64x64+{x}+0'.format(x=str(self.x)))

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop() 

    def update(self):
        
        # array of frames for the current state
        frames = self.animations[self.state]
        print("Current state:", self.state, "Frame index:", self.frame_index, "Total frames:", len(frames))

        # get the next frame index, looping back to 0 if we reach the end of the array
        self.frame_index = (self.frame_index+1) % len(frames)

        # get the current frame to display
        current_frame = frames[self.frame_index]

        # update the label with the current frame 
        self.label.configure(image=current_frame)

        # update the label's image attribute to the current frame to prevent it from being garbage collected
        # tkinter does not keep a reference to the image, so we need to do it ourselves (bad)
        self.label.image = current_frame 


        # create the window
        self.window.geometry('64x64+{x}+0'.format(x=str(self.x)))

        self.window.after(3000, lambda: self.set_state(PetState.WAITING))

        # call update again after X ms (for example 100ms = 10fps)
        self.window.after(100, self.update)
    
    # function to load frames for animation
    def load_frames(self,folder,state_name,amount):
        frames = []
        # range starts at 0, so we add 1 to i to get the correct frame number
        for i in range(amount):
            frames.append(tk.PhotoImage(file=f"{folder}/spr_{state_name}{i+1}.png"))
        return frames
    
    def set_state(self, new_state):
        if (new_state != self.state):

            self.state = new_state

             # reset frame index when state changes so that the animation starts from the beginning
            self.frame_index = 0 
    
    

    
