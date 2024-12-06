import pandas as pd
import numpy as np

# Load the local CSV file into a DataFrame
csv_path = 'weather_prediction_dataset.csv'

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

# Check for null values
print("\nMissing Values Before Handling:")
print(df.isnull().sum())

# Handle missing values
numerical_columns = ['temperature', 'humidity', 'wind_speed', 'precipitation']
for col in numerical_columns:
    if col in df.columns:
        mean_value = df[col].mean()
        df[col].fillna(mean_value, inplace=True)
        print(f"Filled missing values in '{col}' with mean: {mean_value:.2f}")

# Handle remaining nulls by dropping rows
initial_rows = len(df)
df.dropna(inplace=True)
rows_dropped = initial_rows - len(df)
print(f"\nDropped {rows_dropped} rows with missing non-numerical values.")

# Verify missing values are handled
print("\nMissing Values After Handling:")
print(df.isnull().sum())

# Handle extreme values (outliers)
for col in numerical_columns:
    if col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[col] = np.clip(df[col], lower_bound, upper_bound)
        print(f"Handled outliers in '{col}' using bounds: {lower_bound:.2f} - {upper_bound:.2f}")

# Convert date to datetime format
if 'date' in df.columns:
    try:
        df['date'] = pd.to_datetime(df['date'])
        print("\nConverted 'date' column to datetime format.")
    except Exception as e:
        print(f"Error converting 'date' column: {e}")

# Define weather categories
# Update the function to use the correct column for precipitation
def classify_weather(row):
    if row['TOURS_precipitation'] == 0 and row['BASEL_humidity'] < 50:
        return 'Sunny'
    elif row['TOURS_precipitation'] == 0 and row['BASEL_humidity'] >= 50:
        return 'Cloudy'
    elif row['TOURS_precipitation'] > 0 and row['TOURS_temp_mean'] > 0:
        return 'Rainy'
    elif row['TOURS_precipitation'] > 0 and row['TOURS_temp_mean'] <= 0:
        return 'Snowy'
    else:
        return 'Unknown'

# Apply classification
df['weather_category'] = df.apply(classify_weather, axis=1)

# Inspect the categorized data
print("\nWeather Categories Distribution:")
print(df['weather_category'].value_counts())


# Apply classification
df['weather_category'] = df.apply(classify_weather, axis=1)

# Inspect the categorized data
print("\nWeather Categories Distribution:")
print(df['weather_category'].value_counts())

# Save preprocessed data for modeling
output_file = "preprocessed_weather_data.csv"
df.to_csv(output_file, index=False)
print(f"\nPreprocessed data saved to '{output_file}'.")
