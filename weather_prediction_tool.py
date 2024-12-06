import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# Load the dataset
csv_path = 'preprocessed_weather_data.csv'

try:
    df = pd.read_csv(csv_path)
    print("\nDataset loaded successfully.")
except FileNotFoundError:
    print("Error: Dataset file not found. Please check the file path and try again.")
    exit()

# Check the column names to inspect feature names
print("\nColumn Names in Dataset:")
print(df.columns)

# Check the most recent row (latest date)
latest_data = df.tail(1)  # Get the last row for the latest data

# Display the latest row
print("\nLatest Weather Data:")
print(latest_data)

# Assuming you've already trained a model earlier and saved it, you can load the model
model_file = 'weather_prediction_model.pkl'

try:
    model = joblib.load(model_file)
    print(f"\nModel loaded successfully from '{model_file}'.")
except FileNotFoundError:
    print(f"Error: Model file '{model_file}' not found.")
    exit()

# Define the correct features based on dataset inspection
features = ['TOURS_precipitation', 'TOURS_temp_mean', 'TOURS_temp_min', 'TOURS_temp_max', 'BASEL_humidity', 'BASEL_pressure']

# Extract the feature values from the latest row
user_input = latest_data[features].values[0]  # Get values as a list

# Scale the user input using the previously trained scaler (assuming you saved it)
scaler_file = 'scaler.pkl'
try:
    scaler = joblib.load(scaler_file)
    print(f"\nScaler loaded successfully from '{scaler_file}'.")
except FileNotFoundError:
    print(f"Error: Scaler file '{scaler_file}' not found.")
    exit()

# Scale the user input data
user_input_scaled = scaler.transform([user_input])

# Predict using the loaded model
predicted_weather = model.predict(user_input_scaled)

# Print the predicted weather category
print(f"\nPredicted Weather Category for the latest data: {predicted_weather[0]}")
