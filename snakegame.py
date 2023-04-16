import pygame
import random
import time
from pygame.locals import *

pygame.init()
pygame.font.init()

WIDTH = 1280
HEIGHT = 720
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

FONT = pygame.font.SysFont("Arial", 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Snake:
    def __init__(self):
        self.segments = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)
        self.grow = False
        self.speed = 1

    def update(self):
        new_head = (self.segments[0][0] + self.direction[0], self.segments[0][1] + self.direction[1])
        if self.grow:
            self.segments.insert(0, new_head)
            self.grow = False
        else:
            self.segments.pop()
            self.segments.insert(0, new_head)

    def grow_snake(self):
        self.grow = True

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def set_direction(self, direction):
        self.direction = direction

    def collides_with_itself(self):
        return self.segments[0] in self.segments[1:]

    def is_out_of_bounds(self):
        x, y = self.segments[0]
        return x < 0 or y < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT

class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def generate_new_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

class PowerUp:
    def __init__(self):
        self.position = None
        self.spawn_time = None
        self.active = False
        self.next_spawn = random.randint(10, 40)

    def spawn(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.spawn_time = time.time()
        self.active = True

    def despawn(self):
        self.position = None
        self.active = False
        self.next_spawn = random.randint(10, 40)

def draw_snake(surface, snake):
    for segment in snake.segments:
        pygame.draw.rect(surface, WHITE, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_food(surface, food):
    pygame.draw.circle(surface, GREEN, (food.position[0] * GRID_SIZE + GRID_SIZE // 2, food.position[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2)

def draw_power_up(surface, power_up):
    if power_up.active:
        pygame.draw.rect(surface, RED, (power_up.position[0] * GRID_SIZE, power_up.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_score(surface, score):
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    power_up = PowerUp()
    last_power_up_spawn = time.time()
    score = 0

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == KEYDOWN:
                if event.key == K_w and snake.direction != (0, 1):
                    snake.set_direction((0, -1))
                elif event.key == K_s and snake.direction != (0, -1):
                    snake.set_direction((0, 1))
                elif event.key == K_a and snake.direction != (1, 0):
                    snake.set_direction((-1, 0))
                elif event.key == K_d and snake.direction != (-1, 0):
                    snake.set_direction((1, 0))

        snake.update()

        if snake.segments[0] == food.position:
            snake.grow_snake()
            food.generate_new_position()
            score += 1

        if snake.segments[0] == power_up.position and power_up.active:
            snake_speed = snake.get_speed()
            snake.set_speed(snake_speed * 1.5)
            power_up.despawn()

        if not power_up.active and time.time() - last_power_up_spawn > power_up.next_spawn:
            power_up.spawn()
            last_power_up_spawn = time.time()

        if snake.collides_with_itself() or snake.is_out_of_bounds():
            break

        draw_snake(screen, snake)
        draw_food(screen, food)
        draw_power_up(screen, power_up)
        draw_score(screen, score)

        pygame.display.update()
        clock.tick(10 * snake.get_speed())

    pygame.quit()

if __name__ == "__main__":
    main()

