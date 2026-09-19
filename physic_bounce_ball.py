import math
import pygame

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# class
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = 0  # Velocity in x direction
        self.vy = 0  # Velocity in y direction

    def update(self):
        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

        # Bounce off the walls
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy = -self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class gravity:
    def __init__(self, g):
        self.g = g  # Acceleration due to gravity

    def apply(self, ball):
        ball.vy += self.g  # Apply gravity to the ball's vertical velocity

class friction:
    def __init__(self, coefficient):
        self.coefficient = coefficient  # Friction coefficient

    def apply(self, ball):
        ball.vx *= (1 - self.coefficient)  # Apply friction to the ball's horizontal velocity
        ball.vy *= (1 - self.coefficient)  # Apply friction to the ball's vertical velocity

# define the cursor as a hand that can grab the ball and throw it with a velocity based on the mouse movement
class Cursor:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 20, 20)  # Cursor size

    def update(self):
        self.rect.center = pygame.mouse.get_pos()  # Update cursor position to mouse position

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)  # Draw the cursor as a green square

class walls:
    def __init__(self):
        self.top_wall = pygame.Rect(0, 0, WIDTH, 10)
        self.bottom_wall = pygame.Rect(0, HEIGHT - 10, WIDTH, 10)
        self.left_wall = pygame.Rect(0, 0, 10, HEIGHT)
        self.right_wall = pygame.Rect(WIDTH - 10, 0, 10, HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.top_wall)
        pygame.draw.rect(surface, (255, 255, 255), self.bottom_wall)
        pygame.draw.rect(surface, (255, 255, 255), self.left_wall)
        pygame.draw.rect(surface, (255, 255, 255), self.right_wall)

    def check_collision(self, ball):
        if self.top_wall.collidepoint(ball.x, ball.y - ball.radius):
            ball.vy = -ball.vy
        if self.bottom_wall.collidepoint(ball.x, ball.y + ball.radius):
            ball.vy = -ball.vy
        if self.left_wall.collidepoint(ball.x - ball.radius, ball.y):
            ball.vx = -ball.vx
        if self.right_wall.collidepoint(ball.x + ball.radius, ball.y):
            ball.vx = -ball.vx

# define a class that show a vector from the ball to the cursor when the ball is caught
class Vector:
    def __init__(self, ball, cursor):
        self.ball = ball
        self.cursor = cursor

    def draw(self, surface):
        if self.ball.vx == 0 and self.ball.vy == 0:  # Only draw when the ball is caught
            pygame.draw.line(surface, (255, 255, 0), (self.ball.x, self.ball.y), self.cursor.rect.center, 2)

# define a function that makes the ball bounce off the walls with a certain elasticity
def bounce(ball, elasticity):
    if ball.x - ball.radius < 0 or ball.x + ball.radius > WIDTH:
        ball.vx = -ball.vx * elasticity
    if ball.y - ball.radius < 0 or ball.y + ball.radius > HEIGHT:
        ball.vy = -ball.vy * elasticity

# define a function that makes the ball move with physics in the hand
def move_ball_in_hand(ball, cursor):
    if cursor.rect.collidepoint(ball.x, ball.y):
        ball.vx = 0
        ball.vy = 0
        ball.x = cursor.rect.centerx
        ball.y = cursor.rect.centery

# functions
def catch_ball(ball, cursor):
    # Check if the ball is within the cursor's area
    if cursor.rect.collidepoint(ball.x, ball.y):
        # If caught, stop the ball's movement
        ball.vx = 0
        ball.vy = 0
        return True
    return False

def release_ball(ball, cursor):
    # Release the ball with a velocity based on the cursor's movement
    mouse_dx, mouse_dy = pygame.mouse.get_rel()  # Get the relative movement of the mouse
    ball.vx = mouse_dx * 0.1  # Scale the velocity for better control
    ball.vy = mouse_dy * 0.1

# Main game loop
def main():
    clock = pygame.time.Clock()
    ball = Ball(WIDTH // 2, HEIGHT // 2, 20, (255, 0, 0))
    cursor = Cursor()
    wall = walls()
    gravity_effect = gravity(0.5)
    friction_effect = friction(0.01)
    vector = Vector(ball, cursor)
    elasticity = 0.8  # Elasticity for bouncing

    running = True
    caught = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if catch_ball(ball, cursor):
                    caught = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if caught:
                    release_ball(ball, cursor)
                    caught = False

        # Update game state
        cursor.update()
        if not caught:
            gravity_effect.apply(ball)
            friction_effect.apply(ball)
            ball.update()
            wall.check_collision(ball)
        else:
            move_ball_in_hand(ball, cursor)

        # Draw everything
        screen.fill((0, 0, 0))  # Clear the screen with black
        wall.draw(screen)
        ball.draw(screen)
        cursor.draw(screen)
        vector.draw(screen)

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()