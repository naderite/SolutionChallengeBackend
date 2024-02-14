import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tensorflow.keras.models import load_model
import logging

# Set up logging configuration
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load your trained TensorFlow model
best_model = load_model("./dqn_model_final.h5")


# Define a Pydantic model for input data


class InputData(BaseModel):
    Current_Score: int
    Correct_Questions: int
    User_Feedback: float
    Current_Streak: int


@app.post("/predict")
def predict(input_data: InputData):
    try:
        # Prepare the input data for prediction
        input_features = np.array(
            [
                [
                    input_data.Current_Score,
                    input_data.Correct_Questions,
                    input_data.User_Feedback,
                    input_data.Current_Streak,
                ]
            ]
        )
        # Make predictions using your best TensorFlow model
        predictions = best_model.predict(input_features)

        # Assuming predictions is a NumPy array, you can extract the result
        result = float(predictions.flatten()[0])

        return {"prediction": result // 1000}

    except Exception as e:
        # Log the exception for debugging
        logger.exception("Prediction failed.")
        # Handle exceptions appropriately
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
