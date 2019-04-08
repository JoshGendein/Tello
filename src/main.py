import pygame
import cv2
import time
import numpy as np
from TelloControl import TelloControl
from TelloVideo import TelloVideo

a = 0
b = 0
c = 0
d = 0
speed = 60
FPS = 25

if __name__ == '__main__':
    drone = TelloControl()
    drone.connect()
    drone.streamon()

    pygame.init()
    pygame.display.set_caption("Tello video stream")
    screen = pygame.display.set_mode([960, 720])

    drone_video = TelloVideo()

    frame_read = drone_video.get_frame_read()

    should_stop = False
    while not should_stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drone.stop()
                drone_video.stop()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    drone.stop()
                    drone_video.stop()
                    pygame.quit()
                elif event.key == pygame.K_SPACE:
                    drone.takeoff()
                elif event.key == pygame.K_BACKSPACE:
                    drone.land()
                elif event.key == pygame.K_a:
                    a = -speed
                elif event.key == pygame.K_d:
                    a = speed
                elif event.key == pygame.K_w:
                    b = speed
                elif event.key == pygame.K_s:
                    b = -speed
                elif event.key == pygame.K_UP:
                    c = speed
                elif event.key == pygame.K_DOWN:
                    c = -speed
                elif event.key == pygame.K_RIGHT:
                    d = speed
                elif event.key == pygame.K_LEFT:
                    d = -speed
                drone.send_rc((a, b, c, d))                 
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    a = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    b = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    c = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    d = 0
                drone.send_rc((a, b, c, d))

        if frame_read.stopped:
            frame_read.stop()
            break
        
        screen.fill([0, 0, 0])
        frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))
        pygame.display.update()

        time.sleep(1 / FPS)
        
    print('Drone is stopping...')
    drone.stop()
    drone_video.stop()