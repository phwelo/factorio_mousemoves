#!/usr/bin/env python3

from pickle import TRUE
import ahkpy, screeninfo, time, functools, keyboard, mouse

# init values
EDGE_PIXELS = 20
MIDDLE = False
BUTTONS = "wasd"
TITLE_SEARCH = "Factorio"
RELATIVE_TO = "screen"
MOUSE_LOCK = False

print("starting....")

@functools.cache
def get_info():
    monitor = screeninfo.get_monitors()[0]
    return {
        "bottom": monitor.height,
        "right": monitor.width
    }

def get_thresholds(monitor):
    return {
        "bottom": monitor["bottom"] - EDGE_PIXELS,
        "top":    EDGE_PIXELS,
        "right":  monitor["right"] - EDGE_PIXELS,
        "left":   EDGE_PIXELS
    }

def build_thresholds(thresholds):
    mouse_x, mouse_y = ahkpy.get_mouse_pos(relative_to=RELATIVE_TO)
    left = right = top = bottom = False
    if mouse_x < thresholds["left"]: left = True
    elif mouse_x > thresholds["right"]: right = True
    if mouse_y < thresholds["top"]: top = True
    elif mouse_y > thresholds["bottom"]: bottom = True
    return {"bottom": bottom, "top": top, "right": right, "left": left}

def set_button_state(button, press_type):
    ahkpy.send_event("{" + button + " " + press_type + "}", level=10)

def unpress_pressed_buttons(buttons):
    [set_button_state(i, "up") for i in buttons if keyboard.is_pressed(i)]

def button_iterator(buttons):
    [ set_button_state(i, "down") if i in buttons else set_button_state(i, "up") for i in BUTTONS ]

def buttons_press(cur_buttons):
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
    # couldn't figure out how to use right mb in this hotkey
    if mouse.is_pressed(button="left"):
        print("toggle on")
        mouse.press(button="right")

def key_management(state):
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

def key_state_loop():
    monitor = get_info()
    thresholds = get_thresholds(monitor)
    state = build_thresholds(thresholds)
    key_management(state)

def check_for_break():
    if keyboard.is_pressed("Control + C"):
        print("exiting...")
        exit()

def main():
    while True == True:
        check_for_break()
        key_state_loop()

main()