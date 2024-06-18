import numpy as np
from environment import SnakeGame, UP, DOWN, LEFT, RIGHT
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Q-Learning parameters
LEARNING_RATE = 0.001
DISCOUNT = 0.95
EPSILON = 1.0
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.01
EPISODES = 1000

# Build the model
def build_model(input_size, output_size):
    model = Sequential()
    model.add(Dense(24, input_shape=(input_size,), activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(output_size, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(learning_rate=LEARNING_RATE))
    return model

# Choose action
def choose_action(state, model):
    if np.random.rand() < EPSILON:
        return np.random.choice([UP, DOWN, LEFT, RIGHT])
    q_values = model.predict(state)
    return np.argmax(q_values[0])

# Train the model
def train():
    global EPSILON
    game = SnakeGame()
    input_size = len(game.get_state())
    output_size = 4  # 4 possible actions
    model = build_model(input_size, output_size)

    for episode in range(EPISODES):
        state = game.reset()
        state = np.reshape(state, [1, input_size])
        total_reward = 0

        while True:
            action = choose_action(state, model)
            next_state, reward, done = game.step(action)
            next_state = np.reshape(next_state, [1, input_size])
            total_reward += reward

            target = reward
            if not done:
                target = reward + DISCOUNT * np.amax(model.predict(next_state)[0])
            target_f = model.predict(state)
            target_f[0][action] = target

            model.fit(state, target_f, epochs=1, verbose=0)
            state = next_state

            if done:
                print(f"Episode: {episode+1}/{EPISODES}, Score: {game.score}, Epsilon: {EPSILON:.2}")
                break

        EPSILON = max(MIN_EPSILON, EPSILON * EPSILON_DECAY)

        if (episode + 1) % 10 == 0:
            model.save(f"snake_ai_{episode+1}.keras")

train()
