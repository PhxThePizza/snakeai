import pygame
import numpy as np
from tensorflow.keras.models import load_model
from environment import SnakeGame, init_pygame, render

# Load the model
model = load_model(input("Path to model: "))

# Choose action
def choose_action(state, model):
    q_values = model.predict(state)
    return np.argmax(q_values[0])

# Main function to play the game
def play():
    screen = init_pygame()
    game = SnakeGame()
    input_size = len(game.get_state())

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        state = game.get_state()
        state = np.reshape(state, [1, input_size])
        action = choose_action(state, model)
        next_state, reward, done = game.step(action)

        if done:
            game.reset()  # Reset the game if done
            continue

        render(screen, game)
        clock.tick(10)

    pygame.quit()

play()
