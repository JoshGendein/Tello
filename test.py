from pynput import keyboard

def keyboard_down(input):
    try:
        key = input.char
    except AttributeError:
        key = input
    if key == 't':
        return True

def keyboard_release(input):
    try:
        key = input.char
    except AttributeError:
        key = input
    if key == 't':
        print(key)
    elif key == keyboard.Key.esc:
        return False

if __name__ == "__main__":

    with keyboard.Listener(
            on_press=keyboard_down,
            on_release=keyboard_release) as listener:
        listener.join()
