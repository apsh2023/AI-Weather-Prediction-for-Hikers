import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# Load the preprocessed dataset
csv_path = 'preprocessed_weather_data.csv'  # Ensure the path is correct

try:
    df = pd.read_csv(csv_path)
    print("\nDataset loaded successfully.")
except FileNotFoundError:
    print("Error: Dataset file not found. Please check the file path and try again.")
    exit()

# Inspect the dataset
print("\nFirst 5 rows of the dataset:")
print(df.head())
print("\nDataset Information:")
print(df.info())

# Define features and target
features = ['TOURS_precipitation', 'TOURS_temp_mean', 'TOURS_temp_min', 'TOURS_temp_max', 'BASEL_humidity', 'BASEL_pressure']
target = 'weather_category'

# Select the features and target from the DataFrame
X = df[features]
y = df[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features (optional but recommended)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize and train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred = model.predict(X_test_scaled)

# Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model and the scaler
joblib.dump(model, 'weather_prediction_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("\nModel and scaler saved.")
