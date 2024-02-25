import numpy as np
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = FastAPI()


import numpy as np
import random
from collections import deque  # Import deque from collections module
import tensorflow as tf


# # Define the DQNAgent class
# class DQNAgent:
#     def __init__(self, state_size):
#         self.state_size = state_size
#         self.action_size = 201
#         self.memory = deque(maxlen=2000)  # Use deque here
#         self.gamma = 0.95  # discount rate
#         self.epsilon = 1.0  # exploration rate
#         self.epsilon_min = 0.01
#         self.epsilon_decay = 0.995
#         self.learning_rate = 0.001
#         self.model = self._build_model()

#     def _build_model(self):
#         model = tf.keras.models.Sequential()
#         model.add(
#             tf.keras.layers.Dense(24, input_dim=self.state_size, activation="relu")
#         )
#         model.add(
#             tf.keras.layers.Dropout(0.2)
#         )  # Adding dropout with a rate of 0.2 (20%)
#         model.add(tf.keras.layers.Dense(24, activation="relu"))
#         model.add(
#             tf.keras.layers.Dropout(0.2)
#         )  # Adding dropout with a rate of 0.2 (20%)
#         model.add(tf.keras.layers.Dense(self.action_size, activation="linear"))
#         model.compile(
#             loss="mse", optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate)
#         )
#         return model

#     def remember(self, state, action, reward, next_state, done):
#         self.memory.append((state, action, reward, next_state, done))

#     def act(self, state):
#         if np.random.rand() <= self.epsilon:
#             return random.randrange(
#                 -30, 31
#             )  # Random action between -action_size and action_size
#         act_values = self.model.predict(state)
#         return np.clip(
#             int(np.argmax(act_values[0])) - self.action_size,
#             -self.action_size,
#             self.action_size,
#         )  # Clip the action to the range of -action_size to action_size

#     def replay(self, batch_size):
#         minibatch = random.sample(self.memory, batch_size)
#         for state, action, reward, next_state, done in minibatch:
#             target = reward
#             if not done:
#                 target = reward + self.gamma * np.amax(
#                     self.model.predict(next_state)[0]
#                 )
#             target_f = self.model.predict(state)
#             target_f[0][action] = target
#             self.model.fit(state, target_f, epochs=1, verbose=0)
#         if self.epsilon > self.epsilon_min:
#             self.epsilon *= self.epsilon_decay


# # Define your StudentEnvironment class
# class StudentEnvironment:
#     def __init__(self, max_steps=7):
#         self.state_size = 5
#         self.action_size = 201
#         self.current_streak = 0
#         self.max_steps = max_steps
#         self.steps = 0
#         self.target_score = random.randint(0, 100)

#     def reset(self):
#         self.steps = 0
#         self.current_streak = 0
#         self.target_score = random.randint(0, 100)
#         return np.zeros(self.state_size)

#     def progressive_randomizer(self, score):
#         choices = {
#             range(55, 101): [6],
#             range(35, 55): [6] * 20 + [5] * 16 + [4] * 5 + [3] * 3 + [2] * 2 + [1],
#             range(25, 35): [6] * 15
#             + [5] * 11
#             + [4] * 8
#             + [3] * 4
#             + [2] * 3
#             + [1] * 2
#             + [0],
#             range(15, 25): [6] * 6
#             + [5] * 8
#             + [4] * 6
#             + [3] * 4
#             + [2] * 3
#             + [1] * 2
#             + [0],
#             range(5, 15): [6] * 3
#             + [5] * 5
#             + [4] * 7
#             + [3] * 5
#             + [2] * 3
#             + [1] * 2
#             + [0],
#             range(0, 5): [6] * 2
#             + [5] * 3
#             + [4] * 5
#             + [3] * 7
#             + [2] * 4
#             + [1] * 2
#             + [0],
#             range(-5, 0): [6]
#             + [5] * 2
#             + [4] * 4
#             + [3] * 7
#             + [2] * 5
#             + [1] * 3
#             + [0] * 2,
#             range(-15, -5): [6]
#             + [5] * 2
#             + [4] * 3
#             + [3] * 5
#             + [2] * 7
#             + [1] * 5
#             + [0] * 3,
#             range(-25, -15): [6]
#             + [5] * 2
#             + [4] * 3
#             + [3] * 5
#             + [2] * 6
#             + [1] * 8
#             + [0] * 6,
#             range(-101, -25): [6]
#             + [5] * 2
#             + [4] * 3
#             + [3] * 4
#             + [2] * 8
#             + [1] * 11
#             + [0] * 15,
#         }

#         for key in choices:
#             if score in key:
#                 return random.choice(choices[key])

#     def step(self, state, action):
#         self.steps += 1
#         next_state = state.copy()

#         next_state[0] += action
#         next_state[0] = np.clip(next_state[0], 0, 100)
#         diff = self.target_score - next_state[0]
#         next_state[1] = self.progressive_randomizer(diff)

#         next_state[2] = random.choice([-1, -0.5, 0, 0, 0, 0, 0, 0, 0, 0.5, 1])
#         if next_state[1] == 6 or next_state[1] == 0:
#             self.current_streak += 1
#         else:
#             self.current_streak = 0
#         next_state[3] = self.current_streak
#         next_state[4] = next_state[0]

#         target_correct = 3
#         penalty_multiplier = 0.25

#         if next_state[1] == target_correct:
#             reward = 1
#         elif next_state[1] == target_correct + 1 or next_state[1] == target_correct - 1:
#             reward = 0.25
#         elif next_state[1] == target_correct + 2 or next_state[1] == target_correct - 2:
#             reward = 0
#         else:
#             reward = -0.25

#         reward -= next_state[2] * penalty_multiplier
#         reward = max(-1, reward)
#         if self.steps >= self.max_steps:
#             done = True
#         else:
#             done = False
#         return next_state, reward, done
# # Initialize environment and agent
# env = StudentEnvironment(max_steps=10)
# state_size = env.state_size
# agent = DQNAgent(state_size)

# # Load the trained model weights
# agent.model.load_weights("dqn_model_final_weights_v2.h5")


# Load your trained TensorFlow model
best_model = load_model("./best_model.h5")

# Load your preprocessing functions or logic
scaler = StandardScaler()  # Example: Use StandardScaler for feature scaling

# Load your data from a CSV file
# Replace 'your_data.csv' with the actual file path and name
df = pd.read_csv("./train_dataset.csv")

# Assuming 'X_train' is the feature data and 'y_train' is the target variable
X_train = df[["Current_Score", "Average", "Average_diff"]]
y_train = df["UPrate"]

# Fit the scaler with your training data
scaler.fit(X_train)


# Define a Pydantic model for input data
class InputData(BaseModel):
    Current_Score: int
    Average: int
    Average_diff: int


# Define an endpoint to make predictions
@app.post("/predict")
def predict(input_data: InputData):
    try:
        # Prepare the input data for prediction
        input_features = np.array(
            [[input_data.Current_Score, input_data.Average, input_data.Average_diff]]
        )

        # Scale the input features using the fitted scaler
        scaled_features = scaler.transform(input_features)

        # Make predictions using your best TensorFlow model
        predictions = best_model.predict(scaled_features)

        # Assuming predictions is a NumPy array, you can extract the result
        result = float(predictions.flatten()[0])

        return {"prediction": result}

    except Exception as e:
        # Log the exception for debugging
        logger.exception("Prediction failed.")
        # Handle exceptions appropriately
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
