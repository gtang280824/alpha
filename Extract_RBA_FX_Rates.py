import requests
import pandas as pd
from io import BytesIO
from datetime import datetime

# URL to fetch the Excel data
url = "https://www.rba.gov.au/statistics/tables/xls-hist/2023-current.xls"

# Fetch the Excel file from the URL
response = requests.get(url)
response.raise_for_status()

# Load the Excel data into a Pandas DataFrame
excel_data = BytesIO(response.content)
df = pd.read_excel(excel_data, sheet_name=0, skiprows=10)

# Ensure the first column is treated as dates (assuming first column is the date)
df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors='coerce')

# Filter for valid dates and FXRNZD column
df_filtered = df[[df.columns[0], 'FXRNZD']].dropna()

# Get the current date and determine the previous month
current_date = datetime.now()
previous_month = current_date.month - 1 if current_date.month > 1 else 12
previous_year = current_date.year if current_date.month > 1 else current_date.year - 1

# Create a datetime object for the previous month
previous_month_date = datetime(previous_year, previous_month, 1)

# Format the 'Month' value as 'mmm-yy'
formatted_month = previous_month_date.strftime('%b-%y')

# Filter the data for the previous month
df_last_month = df_filtered[
    (df_filtered[df.columns[0]].dt.month == previous_month) &
    (df_filtered[df.columns[0]].dt.year == previous_year)
]

# Calculate the average value of the FXRNZD column for last month
average_last_month = df_last_month['FXRNZD'].mean()

# Extract the last FXRNZD rate for the previous month
last_fx_rate = df_last_month['FXRNZD'].iloc[-1] if not df_last_month.empty else None

# Create a new DataFrame with month, average FX rate, and last FX rate
new_data = {
    'Month': [formatted_month],
    'Average FX Rate': [average_last_month],
    'Last FX Rate': [last_fx_rate]
}
new_df = pd.DataFrame(new_data)

# Define the CSV file path
csv_file = 'rba_fx_rates_summary.csv'  # Adjust the path and file name as needed

# Write the new DataFrame to a CSV file
new_df.to_csv(csv_file, index=False)

print(f"New DataFrame has been saved to {csv_file}")
