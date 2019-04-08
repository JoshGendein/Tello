import pygame
from TelloControl import TelloControl

a = 0
b = 0
c = 0
d = 0
speed = 60

if __name__ == '__main__':
    drone = TelloControl()
    drone.connect()
    drone.streamon()

    pygame.init()
    pygame.display.set_mode((500, 500))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drone.stop()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    drone.stop()
                    pygame.quit()
                elif event.key == pygame.K_SPACE:
                    print('space')
                    drone.takeoff()
                elif event.key == pygame.K_BACKSPACE:
                    print('back-space')
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
                # print('Sending RC command: ', (a, b, c, d))
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
                # print('Sending RC command: ', (a, b, c, d))
                drone.send_rc((a, b, c, d))
    print('Drone is stopping...')
    drone.stop()