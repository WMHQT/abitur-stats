import asyncio
import os

from utils.download_table import download_all_tables
from utils.process_json import process_json
from parsers.mpu_parser import convert_to_csv

OUTPUT_DIR = "data/raw/mpu"


async def prepare_data() -> None:
    """Async data preparation pipeline for analytics."""

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pairs = process_json()
    await download_all_tables(pairs)
    convert_to_csv()


if __name__ == "__main__":
    asyncio.run(prepare_data())