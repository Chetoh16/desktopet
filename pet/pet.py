import random
import tkinter as tk
import time
from enum import Enum
from PIL import Image, ImageTk




class PetState(Enum):
    IDLE = "idle"
    WAITING = "waiting"
    WALKING_LEFT = "walking_left"
    WALKING_RIGHT = "walking_right"
    RUNNING = "running"



SCALE = 4
BASE_SIZE = 64
PET_SIZE = BASE_SIZE * SCALE 
    

class MovementController:
    SPEED_MAP = {PetState.WALKING_LEFT: 10, PetState.WALKING_RIGHT: 10, PetState.RUNNING: 15}

    def get_speed(self, state):
        # 0 is the default speed if the state is not in the SPEED_MAP
        # therefore do not need to define IDLE speed
        return self.SPEED_MAP.get(state, 0)    

    

class Direction(Enum):
    LEFT = -1
    RIGHT = 1

class StateController:
    # to control state
    def __init__(self, window, on_state_change):
        self.window = window
        self.state = PetState.IDLE
        self.direction = Direction.RIGHT

        # This variable will be used for cancelling actions that will otherwise wrongly override other actions
        self.pending_job = None

        self.on_state_change = on_state_change
    
    # function that cancels pending jobs/actions so that the current one can take place safely without interruptions
    def cancel_pending_job(self):
        if self.pending_job is not None:
            self.window.after_cancel(self.pending_job)
            self.pending_job = None

    # direction is an optional parameter, if it's not passed, the current direction is maintained
    # only place where st
    def set_state(self,new_state, direction = None):

        self.cancel_pending_job()

        self.state = new_state

        if direction is not None:
            self.direction = direction
        
        self.on_state_change(new_state)
        self.enter_loop_state(new_state)

    def enter_loop_state(self, state):
        if self.state in (PetState.IDLE, PetState.WAITING):
            self.schedule_idle_cycle()

    def schedule_idle_cycle(self):
        
        # 5-10 seconds of idling between changing states of idling
        random_time = random.randint(5,10) * 1000

        # switch to the opposite idling pose
        target = PetState.IDLE if self.state == PetState.WAITING else PetState.WAITING
        
        # save it in pending_job so that when user clicks, it can be cancelled to override
        self.pending_job = self.window.after(random_time, lambda: self.set_state(target))

    def start(self):
        # call it once to start the idling loop
        self.schedule_idle_cycle()

    # EXTERNAL EVENTS

    def handle_clicks(self, new_direction):
        
        if self.state in (PetState.IDLE, PetState.WAITING):
            new_state = PetState.WALKING_RIGHT if new_direction == Direction.RIGHT else PetState.WALKING_LEFT
            self.set_state(new_state, direction = new_direction)

        # if pet is clicked during walking, reverse direction
        elif self.state in (PetState.WALKING_RIGHT, PetState.WALKING_LEFT):
            reverse_direction = Direction.RIGHT if self.direction == Direction.LEFT else Direction.LEFT
            new_state = PetState.WALKING_RIGHT if reverse_direction == Direction.RIGHT else PetState.WALKING_LEFT
            self.set_state(new_state, direction= reverse_direction)

    def notify_edge_reached(self):
        # could be expanded later on to include more than just reaching the edge of the screen
        
        if self.state in (PetState.WALKING_RIGHT, PetState.WALKING_LEFT):
            self.go_idle()
    
    def request_halt(self):
        if self.state is not PetState.IDLE:
            self.go_idle()

    def go_idle(self):
        self.set_state(PetState.IDLE)
        


class PetSkin:
    def __init__(self, name, idle_path, idle_prefix, idle_count,
                 walking_left_path, walking_left_prefix, walking_left_count,
                 walking_right_path, walking_right_prefix, walking_right_count,
                 waiting_path = None, waiting_prefix = None, waiting_count = 0):
        self.name = name
        self.idle_set = (idle_path, idle_prefix, idle_count)
        self.walking_left_set = (walking_left_path, walking_left_prefix, walking_left_count)
        self.walking_right_set = (walking_right_path, walking_right_prefix, walking_right_count)     

        if waiting_path and waiting_prefix and waiting_count > 0:
            self.waiting_set = (waiting_path, waiting_prefix, waiting_count)
        else:
            self.waiting_set = None

class Pet():
    def __init__(self):

        # create a window
        self.window = tk.Tk()

        # by putting self before the variables, we can access them in other functions
        # if not, they only exist in this function
        
        # load skins
        self.skins = [
            PetSkin(
                name = "human-detective",
                idle_path = "assets/default_idle", idle_prefix="idle_default_det", idle_count=2,
                waiting_path = "assets/crossed_arms_idle", waiting_prefix="idle_detective", waiting_count=2,
                walking_left_path = "assets/walking_left", walking_left_prefix = "walking_left", walking_left_count=7,
                walking_right_path = "assets/walking_right", walking_right_prefix = "walking_right", walking_right_count=7
            )
            # PetSkin(
            #     name = "bird-detective",
            #     idle_path = "assets/", idle_prefix="", idle_count=2,
            #     waiting_path = "assets/", waiting_prefix="", waiting_count=2,
            #     walking_left_path = "assets/", walking_left_prefix = "", walking_left_count=7,
            #     walking_right_path = "assets/", walking_right_prefix = "", walking_right_count=7
            # )
        ]

        self.current_skin_index = 0
        self.load_skin(self.skins[self.current_skin_index])
        
        # current frame of the animation, used to cycle through frames
        self.frame_index = 0

        self.frame_delay = 40
        self.animation_counter = 0
        self.animation_speed = {
            PetState.IDLE: 12,
            PetState.WAITING: 12,
            PetState.WALKING_LEFT: 2,
            PetState.WALKING_RIGHT: 2,
            PetState.RUNNING: 2
        }
        
        self.movement = MovementController()

        # controller own state + direction + transition rules + timers
        self.controller = StateController(self.window, on_state_change=self.on_state_change)

        # use a colour that's not in the sprite in order to make the background transparent
        TRANSPARENT_COLOUR = "#ff00ff"

        self.window.config(bg=TRANSPARENT_COLOUR)

        # make window frameless
        self.window.overrideredirect(True)

        # make window draw over all others
        self.window.attributes('-topmost', True)

        # turn background transparent
        self.window.wm_attributes('-transparentcolor', TRANSPARENT_COLOUR)

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg=TRANSPARENT_COLOUR)

        # create a window -> 64x64+{x}+0 = pixel size 64x64 at coordinates 0,0
        self.x = 0
        self.y = self.window.winfo_screenheight() - PET_SIZE - 20
        self.window.geometry(f'{PET_SIZE}x{PET_SIZE}+{self.x}+{self.y}')

        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        # INTERACTIONS

        # Bind left button events for drag and click distinction
        self.label.bind("<ButtonPress-1>", self.move_pet)
        self.label.bind("<ButtonPress-3>", self.on_right_click)
        #self.label.bind("<B1-Motion>", self.do_drag)
        #self.label.bind("<ButtonRelease-1>", self.stop_drag_or_click)

        # start the IDLE loop
        self.controller.start()

        # run self.update() after the frame delay when mainloop starts
        self.window.after(self.frame_delay, self.update)

        self.window.mainloop() 

    
    # function to load frames for animation
    def load_frames(self,folder,state_name,amount, scale=SCALE):
        frames = []

        # range starts at 0, so we add 1 to i to get the correct frame number
        for i in range(amount):

            path = f"{folder}/spr_{state_name}{i+1}.png"

            # load the image using PIL
            image = Image.open(path)

            # get new size
            new_size = (image.width * scale, image.height * scale)

            # resize image
            image = image.resize(new_size, Image.NEAREST)

            # convert the image to a PhotoImage object
            frames.append(ImageTk.PhotoImage(image))
        return frames
    
    def load_skin(self, skin):
        animations = {
            PetState.IDLE: self.load_frames(*skin.idle_set),
            PetState.WALKING_RIGHT: self.load_frames(*skin.walking_right_set),
            PetState.WALKING_LEFT: self.load_frames(*skin.walking_left_set)
        }

        # if there's no waiting sprites, use default idle sprites
        animations[PetState.WAITING] = (
            self.load_frames(*skin.waiting_config) if skin.waiting_config
            else animations[PetState.IDLE] 
        )
        
        self.animations = animations

    # called by StateController whenever a state changes
    def on_state_change(self, new_state):
        self.frame_index = 0
        self.animation_counter = 0
        self.update_animations()
        
    # pet moves right if there's space, left if not
    def move_pet(self, event):

        # might need to do it the other way since handle_click reverses direction
        move_direction = Direction.RIGHT if self.x < self.window.winfo_screenwidth() - PET_SIZE else Direction.LEFT

        self.controller.handle_clicks(move_direction)

    def on_right_click(self, event):
        self.controller.request_halt()

    
    def update_animations(self):

        # array of frames for the current state
        frames = self.animations[self.controller.state]
        
        # get the current frame to display
        current_frame = frames[self.frame_index]

        # get the next frame index, looping back to 0 if we reach the end of the array
        self.frame_index = (self.frame_index + 1) % len(frames)

        # update the label with the current frame 
        self.label.configure(image=current_frame)

        # update the label's image attribute to the current frame to prevent it from being garbage collected
        # tkinter does not keep a reference to the image, so we need to do it ourselves (bad)
        self.label.image = current_frame 

    def update(self):


        state = self.controller.state
        direction = self.controller.direction
        speed = self.movement.get_speed(self.controller.state)

        # EVENTS - Physics / Rules

        # Walking Right
        if state == PetState.WALKING_RIGHT:
            self.x += speed * direction.value

            if self.x >= self.window.winfo_screenwidth() - PET_SIZE:
                
                # set it to the edge just in case
                self.x = self.window.winfo_screenwidth() - PET_SIZE

                self.controller.notify_edge_reached()
        
        # Walking Left
        elif state == PetState.WALKING_LEFT:
            self.x += speed * direction.value

            if self.x <= 0:
                
                # set it to the edge just in case
                self.x = 0

                self.controller.notify_edge_reached()
        
        self.window.geometry(f'{PET_SIZE}x{PET_SIZE}+{self.x}+{self.y}')
                
        self.animation_counter += 1

        animation_speed = self.animation_speed.get(state, 3)

        if self.animation_counter >= animation_speed:
            self.animation_counter = 0
            self.update_animations()

        # call update again after X ms (for example 100ms = 10fps)
        self.window.after(self.frame_delay, self.update)
        

    

    
