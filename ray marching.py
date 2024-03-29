import pygame
import sys
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
fps = 120
running = True

startpos = (400, 400)

circle_list = []
for i in range(5):
    circle_list.append(((random.randint(0, 800), random.randint(0, 800)), random.randint(10, 40)))

rect_list = []
for i in range(5):
    rect_list.append(
        ((random.randint(0, 800), random.randint(0, 800)), (random.randint(10, 40), random.randint(10, 40))))


def sdf_circle(start, pos, r):
    delta_x = start[0] - pos[0]
    delta_y = start[1] - pos[1]
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2) - r
    return distance


def sdf_rect(start, pos, size):
    delta_x = abs(start[0] - pos[0])
    delta_y = abs(start[1] - pos[1])
    x_distance = max(delta_x - size[0], 0)
    y_distance = max(delta_y - size[1], 0)
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance


def return_max_distance(start):
    distances = []
    for circle in circle_list:
        pos, r = circle
        distance = sdf_circle(start, pos, r)
        distances.append(distance)
    for rect in rect_list:
        pos, size = rect
        distance = sdf_rect(start, pos, size)
        distances.append(distance)
    return min(distances)


def render():
    screen.fill((10, 10, 30))
    render_obstacles()
    ray_march(get_mouse_angle(pygame.mouse.get_pos()))
    pygame.display.flip()


def render_obstacles():
    for circle in circle_list:
        pos, r = circle
        pygame.draw.circle(screen, (50, 125, 100), pos, r)

    for rect in rect_list:
        pos, size = rect
        rect = pygame.Rect(0, 0, size[0] * 2, size[1] * 2)
        rect.center = pos
        pygame.draw.rect(screen, (75, 100, 150), rect)


def ray_march(direction):
    ray_march_circles = []
    length = 0
    new_pos = startpos
    for j in range(40):
        step = return_max_distance(new_pos)
        length += step

        ray_march_circles.append((new_pos, step))

        new_pos = (math.cos(direction) * length + startpos[0], math.sin(direction) * length + startpos[1])

        if step < 0.01 or length > 1000:
            break
    end_pos = (math.cos(direction) * length + startpos[0], math.sin(direction) * length + startpos[1])
    pygame.draw.line(screen, (255, 0, 0), startpos, end_pos)

    for circle in ray_march_circles:
        pos, r = circle
        pygame.draw.circle(screen, (225, 208, 50), pos, r, 1)

    distance_text = font.render(str(int(length)), True, (100, 100, 100))
    distance_rect = distance_text.get_rect()
    distance_rect.topright = (795, 5)
    screen.blit(distance_text, distance_rect)


def get_mouse_angle(pos):
    x = pos[0] - startpos[0]
    y = pos[1] - startpos[1]
    angle = math.atan2(y, x)
    return angle


def move_start_pos(x_movement, y_movement):
    global startpos
    x, y = startpos
    x += x_movement
    y += y_movement
    startpos = (x, y)


def key_handler(keys):
    global running, startpos
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        move_start_pos(0, -3)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        move_start_pos(0, 3)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        move_start_pos(-3, 0)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        move_start_pos(3, 0)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            startpos = pygame.mouse.get_pos()

    key_handler(pygame.key.get_pressed())

    render()
    clock.tick(120)

pygame.quit()
sys.exit()
