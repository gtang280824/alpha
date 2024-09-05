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

# Ensure the first column is treated as dates
df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors='coerce')

# Filter for valid dates and FXRNZD column
df_filtered = df[['Series ID', 'FXRNZD']].dropna()

# Get the current date and determine the previous month
current_date = datetime.now()
previous_month = current_date.month - 1 if current_date.month > 1 else 12
previous_year = current_date.year if current_date.month > 1 else current_date.year - 1

# Filter the data for the previous month
df_last_month = df_filtered[
    (df_filtered['Series ID'].dt.month == previous_month) &
    (df_filtered['Series ID'].dt.year == previous_year)
]

# Calculate the average value of the FXRNZD column for last month
average_last_month = df_last_month['FXRNZD'].mean()

# Extract the last FXRNZD rate for the previous month
last_fx_rate = df_last_month['FXRNZD'].iloc[-1] if not df_last_month.empty else None

# Output the results
print(f"Last month's average FXRNZD rate: {average_last_month:.4f}")
print(f"Last month's end FXRNZD rate: {last_fx_rate:.4f}" if last_fx_rate else "No data for last month's end FXRNZD rate.")
