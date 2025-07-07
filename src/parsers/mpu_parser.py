import os
import re
import pandas as pd
from bs4 import BeautifulSoup

INPUT_DIR = "data/raw/mpu"
OUTPUT_DIR = "data/csv/mpu"
FILENAME_PATTERN = r'^([\d\.]+)_([^_]+)_([^_]+)\.txt$'


def read_html_content(file_path: str) -> str:
    """Read raw HTML content from a .txt file."""
    
    with open(file_path, encoding='utf-8') as f:
        return f.read()


def parse_html_table(html_content: str) -> list:
    """Parse HTML content and extract table rows."""
    
    fake_table_html = f"<table>{html_content}</table>"
    soup = BeautifulSoup(fake_table_html, 'html.parser')
    
    if not (table := soup.find('table')):
        raise ValueError("No table found in HTML content")
        
    return table.find_all('tr')


def clean_cell(text: str) -> str:
    """Clean cell text by removing non-breaking spaces and trimming."""
    
    return text.replace('\xa0', '').replace('&nbsp;', '').strip()


def extract_rows(table_rows: list) -> tuple[list, list]:
    """Separate header and data rows from parsed table."""
    
    headers = []
    data_rows = []
    
    for row in table_rows:
        cols = [clean_cell(col.get_text()) for col in row.find_all(['td', 'th'])]
        if not cols:
            continue

        if "№" in cols:
            headers = cols
        else:
            data_rows.append(cols)
            
    return headers, data_rows


def validate_rows(headers: list, data_rows: list) -> list:
    """Filter out malformed rows with inconsistent column counts."""
    
    valid_rows = []
    skipped_count = 0
    
    for idx, row in enumerate(data_rows):
        if len(row) == len(headers):
            valid_rows.append(row)
        else:
            skipped_count += 1
            # print(f"Skipped row {idx}: Expected {len(headers)} columns, got {len(row)}")
            
    return valid_rows


def create_dataframe(headers: list, valid_rows: list) -> pd.DataFrame:
    """Create DataFrame from validated table data."""
    
    if not headers or not valid_rows:
        raise ValueError("Cannot create DataFrame: missing headers or data")
        
    return pd.DataFrame(valid_rows, columns=headers)


def map_study_type(study_type_title: str) -> int:
    return {
        "Платная": 0,
        "Бюджетная": 1,
    }[study_type_title]


def map_form(form_title: str) -> int:
    return {
        "Заочная": 0,
        "Очная": 1,
        "Очно-заочная": 2,
    }[form_title]


def process_file(file_name: str) -> tuple[str, pd.DataFrame] | None:
    """Process a single file and return faculty code and DataFrame."""
    
    match = re.match(FILENAME_PATTERN, file_name)
    
    if not match:
        # print(f"Skipping invalid filename: {file_name}")
        return None
        
    faculty_code = match.group(1)
    study_type = map_study_type(match.group(2))
    form = map_form(match.group(3))
    
    file_path = os.path.join(INPUT_DIR, file_name)
    
    try:
        html_content = read_html_content(file_path)
        table_rows = parse_html_table(html_content)
        headers, data_rows = extract_rows(table_rows)
        valid_rows = validate_rows(headers, data_rows)
        df = create_dataframe(headers, valid_rows)
        
        df['Форма обучения'] = study_type
        df['Основа обучения'] = form
        
        return faculty_code, df
        
    except Exception:
        # print(f"Error processing {file_name}: {str(e)}")
        return None


def collect_data() -> dict:
    """Collect and group data by faculty code."""
    
    faculty_groups = {}
    
    for file_name in os.listdir(INPUT_DIR):
        if result := process_file(file_name):
            faculty_code, df = result
            if faculty_code in faculty_groups:
                faculty_groups[faculty_code] = pd.concat(
                    [faculty_groups[faculty_code], df], 
                    ignore_index=True
                )
            else:
                faculty_groups[faculty_code] = df
                
    return faculty_groups


def save_faculty_data(faculty_groups: dict) -> None:
    """Save collected data to CSV files by faculty code."""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for faculty_code, df in faculty_groups.items():
        output_path = os.path.join(OUTPUT_DIR, f"{faculty_code}.csv")
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Saved {len(df)} records to {output_path}")


def convert_to_csv() -> None:
    print("Converting...")
    faculty_data = collect_data()
    save_faculty_data(faculty_data)
    print("Conversion is finished!")
