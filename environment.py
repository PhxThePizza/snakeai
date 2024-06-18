import pygame
import random
import numpy as np

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 10

# Directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class SnakeGame:
    def __init__(self):
        self.reset()

    def new_food(self):
        while True:
            x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def update_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == UP:
            new_head = (head_x, head_y - CELL_SIZE)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + CELL_SIZE)
        elif self.direction == LEFT:
            new_head = (head_x - CELL_SIZE, head_y)
        elif self.direction == RIGHT:
            new_head = (head_x + CELL_SIZE, head_y)
        self.snake.insert(0, new_head)

    def get_state(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        state = [
            int(food_x < head_x),  # Food is to the left
            int(food_x > head_x),  # Food is to the right
            int(food_y < head_y),  # Food is above
            int(food_y > head_y),  # Food is below
            int((head_x, head_y - CELL_SIZE) in self.snake or head_y - CELL_SIZE < 0),  # Up is blocked
            int((head_x, head_y + CELL_SIZE) in self.snake or head_y + CELL_SIZE >= HEIGHT),  # Down is blocked
            int((head_x - CELL_SIZE, head_y) in self.snake or head_x - CELL_SIZE < 0),  # Left is blocked
            int((head_x + CELL_SIZE, head_y) in self.snake or head_x + CELL_SIZE >= WIDTH),  # Right is blocked
        ]
        return tuple(state)

    def step(self, action):
        self.direction = action
        self.update_snake()
        
        reward = -0.1
        if self.snake[0] == self.food:
            self.food = self.new_food()
            reward = 10
        else:
            self.snake.pop()

        if self.is_collision():
            reward = -10
            self.game_over = True

        new_state = self.get_state()
        self.score = len(self.snake) - 1
        return new_state, reward, self.game_over

    def is_collision(self):
        head = self.snake[0]
        return (head in self.snake[1:] or 
                head[0] < 0 or head[0] >= WIDTH or 
                head[1] < 0 or head[1] >= HEIGHT)

    def reset(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.food = self.new_food()
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.game_over = False
        return self.get_state()

def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake AI')
    return screen

def render(screen, game):
    screen.fill(BLACK)
    for segment in game.snake:
        pygame.draw.rect(screen, WHITE, (*segment, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (*game.food, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()
