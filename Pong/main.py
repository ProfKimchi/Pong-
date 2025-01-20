import pygame
import pymunk
import pymunk.pygame_util

# Play around with default collision handler.
pygame.init()
FPS = 60
DT = 1 / FPS
WIDTH, HEIGHT = 1000, 800
MOVEMENT_SPEED = 500

direction1 = [0, 0]
direction2 = [0, 0]

# GUI setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
icon = pygame.image.load("ping-pong.png")
pygame.display.set_icon(icon)

# FPS adjustments.
clock = pygame.time.Clock()

# Physics adjustments
space = pymunk.Space()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Score text.
score_value_p1 = 0
score_value_p2 = 0
font = pygame.font.Font("digital-7.ttf", 128)
text1_x = 300
text1_y = 100
text2_x = 632
text2_y = 100


# Drawing function for background. Cleans up the program a bit.
def draw(space, screen, draw_options):
    screen.fill((7, 64, 66))
    space.debug_draw(draw_options)
    pygame.draw.line(screen, (255, 255, 255), (500, 800), (500, 0))
    score_p1 = font.render(f"{str(score_value_p1)}", True, (255, 255, 255))
    screen.blit(score_p1, (text1_x, text1_y))
    score_p2 = font.render(f"{str(score_value_p2)}", True, (255, 255, 255))
    screen.blit(score_p2, (text2_x, text2_y))
    pygame.display.update()


# Collision handler for paddles
def reflect_ball_kinematic(arbiter, space, data):
    return True


# Collision handler for walls
def reflect_ball_static_positive(arbiter, space, data):
    ball_shape, surface_shape = arbiter.shapes
    bx, by = ball_shape.body.velocity
    if bx >= 0:
        ball_shape.body.apply_force_at_local_point((7, 0))  # Adjust to 7.5 if collision issues.
    else:
        ball_shape.body.apply_force_at_local_point((-7, 0))
    return True


# Creates boundaries for the ball
def create_boundaries(space, width, height, collision_type):
    rectangles = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
    ]

    for position, size in rectangles:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = position
        shape = pymunk.Poly.create_box(body, size)
        shape.color = (255, 255, 255, 100)
        shape.elasticity = 1.5
        shape.collision_type = collision_type
        space.add(body, shape)


# Test function for creating a ball.
def create_ball(space, radius, mass):
    body = pymunk.Body()
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 255, 255, 100)
    body.position = (500, 400)
    shape.elasticity = 1
    shape.friction = 1
    shape.collision_type = 0
    space.add(body, shape)
    return shape


# Creating paddles.
def create_paddle(space, position, collision_type):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = position
    x, y = body.position
    shape = pymunk.Poly.create_box(body, (10, 100))
    shape.color = (131, 173, 5, 100)
    shape.elasticity = 1.2
    shape.mass = 10
    shape.friction = 1
    shape.collision_type = collision_type
    space.add(body, shape)
    return shape


# Paddle coordinates
p1_x = 40
p1_y = 400

p2_x = 960
p2_y = 400

# Ball on screen
ball = create_ball(space, 8, 10)
ball.body.velocity = pymunk.Vec2d(0, 0)

# Paddle objects
p1 = create_paddle(space, (p1_x, p1_y), 1)
p2 = create_paddle(space, (p2_x, p2_y), 1)

# Velocities
p1.body.velocity = pymunk.Vec2d(0, 0)
p2.body.velocity = pymunk.Vec2d(0, 0)

# Collision handler
handler1 = space.add_collision_handler(0, 1)
handler1.begin = reflect_ball_kinematic

handler2 = space.add_collision_handler(0, 2)
handler2.post_solve = reflect_ball_static_positive


# Score handlers
def is_score_p1(ball_x):
    if ball_x >= 960:
        return True
    return False


def is_score_p2(ball_x):
    if ball_x <= 40:
        return True
    return False


# Starting condition
start = False

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.body.velocity = pymunk.Vec2d(300, 0)
                start = True

        if start:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p2.body.velocity = pymunk.Vec2d(0, -400)
                if event.key == pygame.K_DOWN:
                    p2.body.velocity = pymunk.Vec2d(0, 400)
                if event.key == pygame.K_w:
                    p1.body.velocity = pymunk.Vec2d(0, -400)
                if event.key == pygame.K_s:
                    p1.body.velocity = pymunk.Vec2d(0, 400)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    p2.body.velocity = pymunk.Vec2d(0, 0)
                if event.key == pygame.K_DOWN:
                    p2.body.velocity = pymunk.Vec2d(0, 0)
                if event.key == pygame.K_w:
                    p1.body.velocity = pymunk.Vec2d(0, 0)
                if event.key == pygame.K_s:
                    p1.body.velocity = pymunk.Vec2d(0, 0)

    # Paddle position control
    p1_x, p1_y = p1.body.position
    p2_x, p2_y = p2.body.position

    if p1_y <= 60:
        p1.body.position = (40, 60)
    if p1_y >= 740:
        p1.body.position = (40, 740)
    if p2_y <= 60:
        p2.body.position = (960, 60)
    if p2_y >= 740:
        p2.body.position = (960, 740)

    # Ball velocity control
    ball_vx, ball_vy = ball.body.velocity
    if ball_vx >= 750:
        ball.body.velocity = pymunk.Vec2d(600, ball_vy)
    if ball_vy >= 750:
        ball.body.velocity = pymunk.Vec2d(ball_vx, 600)
    if ball_vx <= -750:
        ball.body.velocity = pymunk.Vec2d(-600, ball_vy)
    if ball_vy <= -750:
        ball.body.velocity = pymunk.Vec2d(ball_vx, -600)

    # Scoring system
    ball_x, ball_y = ball.body.position
    if is_score_p1(ball_x):
        ball.body.velocity = pymunk.Vec2d(0, 0)
        score_value_p1 += 1
    if is_score_p2(ball_x):
        ball.body.velocity = pymunk.Vec2d(0, 0)
        score_value_p2 += 1
    if is_score_p2(ball_x) or is_score_p1(ball_x):
        p1.body.position = (40, 400)
        p2.body.position = (960, 400)
        ball.body.position = (500, 400)
        start = False

    draw(space, screen, draw_options)
    create_boundaries(space, WIDTH, HEIGHT, 2)

    space.step(DT)
    clock.tick(FPS)

pygame.quit()
