import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except FileNotFoundError:
        return f"File {file_path} not found.", None
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='windows-1251')

    return df