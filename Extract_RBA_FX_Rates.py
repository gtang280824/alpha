import requests
import pandas as pd
from io import BytesIO

url = "https://www.rba.gov.au/statistics/tables/xls-hist/2023-current.xls"

response = requests.get(url)
response.raise_for_status()

excel_data = BytesIO(response.content)

# Read only the first sheet and skip rows above row 11 (row 12 in Excel, as it's zero-indexed)
df = pd.read_excel(excel_data, sheet_name=0, skiprows=10)

# Keep only the first column and the column labeled "FXRNZD"
df = df.iloc[:, [0, df.columns.get_loc("FXRNZD")]]

# Save the filtered data to a CSV file
df.to_csv("rba_fx_rates_filtered_data.csv", index=False)
print("Filtered data saved to rba_fx_rates_filtered_data.csv")
