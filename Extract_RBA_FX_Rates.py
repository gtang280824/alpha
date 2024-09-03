import requests
import pandas as pd
from io import BytesIO

url = "https://www.rba.gov.au/statistics/tables/xls-hist/2023-current.xls"

response = requests.get(url)
response.raise_for_status()

excel_data = BytesIO(response.content)

# Read only the first sheet
df = pd.read_excel(excel_data, sheet_name=0)

# Save the first sheet to a CSV file
df.to_csv("rba_fx_rates_data.csv", index=False)
print("Data saved to rba_fx_rates_data.csv")
