import pandas as pd

# Load the dataset 
df = pd.read_csv('combined_exchange_rate.csv', parse_dates=['Date'])

# Set the 'Date' column as the index to work with time series data
df.set_index('Date', inplace=True)

# Display the first few rows to check the data structure
print("Original Data:")
print(df.head())

# Fill missing values
# 1. Forward fill (fills missing values with the last known valid value)
df_filled = df.ffill()

# 2. Backward fill (fills remaining missing values with the next known valid value)
df_filled = df_filled.bfill()

# 3. Interpolate (fills any remaining gaps smoothly using linear interpolation)
df_filled = df_filled.interpolate(method='linear')

# Check for remaining null values
print("\nNull values after filling:")
print(df_filled.isnull().sum())

# Display the filled data
print("\nData after filling:")
print(df_filled.head())

# Save the processed data to a new CSV file
df_filled.to_csv('currency_rates_filled.csv')

print("\nData has been filled and saved to 'currency_rates_filled.csv'.")

