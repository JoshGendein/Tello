from pynput import keyboard
from TelloControl import TelloControl

if __name__ == '__main__':
    drone = TelloControl()
    drone.connect()
    drone.streamon()

    with keyboard.Listener(
            on_press=drone.keyboard_down,
            on_release=drone.keyboard_release) as listener:
        listener.join()

    drone.stop()