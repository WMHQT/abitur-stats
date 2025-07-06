from bs4 import BeautifulSoup
import pandas as pd

def clean_cell(text):
    return text.replace('\xa0', '').replace('&nbsp;', '').strip()

# Read file
with open('ps_search_results.txt', 'r', encoding='utf-8') as f:
    raw_html = f.read()

# Wrap in table tags
fake_table_html = f"<table>{raw_html}</table>"
soup = BeautifulSoup(fake_table_html, 'html.parser')
table = soup.find('table')

rows = table.find_all('tr')

all_data = []
headers = []

for i, row in enumerate(rows):
    cols = row.find_all(['td', 'th'])
    if not cols:
        continue

    row_data = [clean_cell(col.get_text()) for col in cols]

    # Try to detect header row (contains №, Уникальный код, Математика, etc.)
    if "№" in row_data or "Уникальный код" in row_data or "Математика" in row_data:
        headers = row_data
    else:
        if len(row_data) > 0:
            all_data.append(row_data)

# If no headers were found, generate default ones based on first row
if not headers:
    if all_data:
        headers = [f"Col_{j}" for j in range(len(all_data[0]))]
    else:
        raise ValueError("No header or data rows found in the table.")

# Ensure all rows match header count
valid_data = []
for row in all_data:
    if len(row) == len(headers):
        valid_data.append(row)
    else:
        print(f"Skipping row with mismatched length: expected {len(headers)}, got {len(row)}")

# Create DataFrame
df = pd.DataFrame(valid_data, columns=headers)

# Save CSV
df.to_csv('parsed_ps_search_results.csv', index=False, encoding='utf-8-sig')
print("Table saved to parsed_ps_search_results.csv")