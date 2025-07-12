import pandas as pd
import os
from typing import List, Tuple

from utils.load_csv import load_csv


def text_output(data: List[Tuple[str, int]]) -> str:
    """Creates text table from grouped unique applicant counts."""
    output = []
    
    for group, count in data:
        output.append(f"Группа направлений: {group}")
        output.append(f"\nКол-во уникальных абитуриентов: {count}")
        output.append("—" * 19)
    
    return "\n".join(output)


def analyze_unique_applicants(dir_path: str) -> List[Tuple[str, int]]:
    """Analyzes CSV files grouped by first two digits of filename prefix."""
    
    groups = {}  # Dictionary to store unique codes per group
    
    # Process all CSV files in the directory
    for filename in os.listdir(dir_path):
        if not filename.endswith('.csv'):
            continue
            
        # Extract first part of filename (before first dot)
        base_part = filename.split('.')[0]
        
        # Get first two characters of filename prefix
        if len(base_part) >= 2:
            group_key = base_part[:2]
        else:
            # Fallback for short filenames
            group_key = filename[:2]
        
        file_path = os.path.join(dir_path, filename)
        
        try:
            # Load CSV and get unique applicant codes
            df = load_csv(file_path)
            unique_codes = df['Уникальныйкод'].unique()
            
            # Initialize or update group data
            if group_key not in groups:
                groups[group_key] = set()
            
            groups[group_key].update(unique_codes)
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    # Convert sets to counts and sort groups
    result = sorted([(group, len(codes)) for group, codes in groups.items()])
    return result


def run_analysis(dir_path: str = 'data/csv/mpu') -> Tuple[str, None]:
    """Main analysis function for unique applicant counting."""
    
    data = analyze_unique_applicants(dir_path)
    text = text_output(data)
    
    return text