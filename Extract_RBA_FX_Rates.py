import requests
import pandas as pd
from io import BytesIO

url = "https://www.rba.gov.au/statistics/tables/xls-hist/2023-current.xls"

response = requests.get(url)
response.raise_for_status()

excel_data = BytesIO(response.content)

df = pd.read_excel(excel_data, sheet_name=None)

for sheet_name, sheet_df in df.items():
    sheet_df.to_csv(f"rba_fx_rates_{sheet_name}.csv", index=False)
    print(f"Data saved to rba_fx_rates_{sheet_name}.csv")
