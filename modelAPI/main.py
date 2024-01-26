import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
import pandas as pd
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

# Load your trained TensorFlow model
best_model = load_model("./model.h5")

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
        logger.error(f"Prediction failed. Exception: {str(e)}")
        # Handle exceptions appropriately
        raise HTTPException(status_code=500, detail=f"Internal Server Error{str(e)}")
