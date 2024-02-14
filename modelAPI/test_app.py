import pytest
import httpx
import time
import random

from fastapi.testclient import TestClient
from main import app  # Update this import based on your actual app module

# Define the number of requests for testing
NUM_REQUESTS = 10


# Helper function to make requests
def make_request(client, input_data):
    response = client.post("/predict", json=input_data)
    return response


# Test the average response time
def test_average_response_time():
    client = TestClient(app)

    total_elapsed_time = 0

    for _ in range(NUM_REQUESTS):
        # Generate different input data for each request
        input_data = {
            "Current_Score": random.randint(1, 100),
            "Average": random.randint(0, 6),
            "Average_diff": random.randint(1, 100),
        }

        # Measure the time for each request
        start_time = time.time()
        response = make_request(client, input_data)
        end_time = time.time()
        # Ensure the response is successful
        assert response.status_code == 200

        # Accumulate the elapsed time
        total_elapsed_time += end_time - start_time

    # Calculate the average response time
    avg_response_time = total_elapsed_time / NUM_REQUESTS

    assert avg_response_time > 0, f"Average response time: {avg_response_time} seconds"


# Run the tests
if __name__ == "__main__":
    test_average_response_time()
