#!/usr/bin/env python3

# I know this could probably all be done in ahkpy, but keyboard/mouse 
# make it so simple & this didn't slow things down
import ahkpy, screeninfo, time, keyboard, mouse
import signal

# Adjustables
EDGE_PIXELS = 20
TITLE_SEARCH = "Factorio"
RELATIVE_TO = "screen"

# Init values
MIDDLE = False
BUTTONS = "wasd"
MOUSE_LOCK = False

def get_info():
    '''grab monitor height/width'''
    monitor = screeninfo.get_monitors()[0]
    return {
        "bottom": monitor.height,
        "right": monitor.width
    }

def get_thresholds(monitor):
    '''do the edge border calculations'''
    return {
        "bottom": monitor["bottom"] - EDGE_PIXELS,
        "top":    EDGE_PIXELS,
        "right":  monitor["right"] - EDGE_PIXELS,
        "left":   EDGE_PIXELS
    }

def build_thresholds(thresholds):
    '''build an object reporting on whether or not thresholds were met (this allows easier corner handling)'''
    mouse_x, mouse_y = ahkpy.get_mouse_pos(relative_to=RELATIVE_TO)
    left = right = top = bottom = False
    # mutually exclusive values lead to a string of weird if/else
    if mouse_x < thresholds["left"]: left = True
    elif mouse_x > thresholds["right"]: right = True
    if mouse_y < thresholds["top"]: top = True
    elif mouse_y > thresholds["bottom"]: bottom = True
    return {"bottom": bottom, "top": top, "right": right, "left": left}

def set_button_state(button, press_type):
    '''ahk function to perform the keyup/down event'''
    ahkpy.send_event("{" + button + " " + press_type + "}", level=10)

def unpress_pressed_buttons(buttons):
    '''for any of the buttons in flight (BUTTONS) make sure they are up'''
    [set_button_state(i, "up") for i in buttons if keyboard.is_pressed(i)]

def button_iterator(buttons):
    '''loop through the pressed buttons and perform the up/down action'''
    [ set_button_state(i, "down") if i in buttons else set_button_state(i, "up") for i in BUTTONS ]

def buttons_press(cur_buttons):
    '''sort of a director function that assures we don't rerun the button-up code, which allows for arrows to continue to be used for navigation'''
    global MIDDLE
    if len(cur_buttons) == 0 and MIDDLE:
        pass
    elif len(cur_buttons) == 0 and not MIDDLE:
        MIDDLE = True
        unpress_pressed_buttons(BUTTONS)
    else:
        MIDDLE = False
        button_iterator(cur_buttons)

def mouse_lock_module():
    '''made this idea of a module so that hotkeys can be expanded if wanted, this one handles right click lock for mining'''
    # couldn't figure out how to use right mb in this hotkey
    if mouse.is_pressed(button="left"):
        print("toggle on")
        mouse.press(button="right")

def key_management(state):
    '''this assures that we only press (or pull up) BUTTONS if shift isn't held and the correct window is active'''
    keys = []
    active_window_title = ahkpy.Windows.get_active(ahkpy.windows, match="contains").title
    if TITLE_SEARCH in str(active_window_title):
        if keyboard.is_pressed("Shift"):
            mouse_lock_module()
            unpress_pressed_buttons(BUTTONS)
        else:
            if state["left"]: keys.append("a")
            if state["right"]: keys.append("d")
            if state["top"]: keys.append("w")
            if state["bottom"]: keys.append("s")
            buttons_press(keys)

def key_state_loop(thresholds):
    state = build_thresholds(thresholds)
    key_management(state)

def sigint_handler(_, __):
    print("exiting...")
    exit(0)

def main():
    signal.signal(signal.SIGINT, sigint_handler)
    print("starting....")
    monitor = get_info()
    thresholds = get_thresholds(monitor)
    while True:
        key_state_loop(thresholds)

main()