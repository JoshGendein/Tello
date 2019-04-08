import keyboard

def keyboard_down(input):
    print('Down: ', input.name)

def keyboard_release(input):
    print('Release: ', input.name)

if __name__ == "__main__":

    keyboard.on_press(keyboard_down)
    keyboard.on_release(keyboard_release)

    keyboard.wait('esc')
