import joblib
import numpy as np

# Load the trained model
model_path = "battery_model.joblib"  # Update with your model file name if different
model = joblib.load(model_path)

# Input variable
a = 1.14  # Example input value
input_data = np.array([[a]])  # Ensure it's a 2D array for the model

# Predict the lifespan
predicted_lifespan = model.predict(input_data)

# Output the result
print(f"Predicted lifespan for a={a}: {predicted_lifespan[0]}")
