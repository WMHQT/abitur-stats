import json
import asyncio

from parsers.mpu_parser import convert_to_csv
from utils.process_json import process_json
from utils.download_table import download_table


async def prepare_data() -> None:
    """Async data preparation pipeline for analytics."""

    pairs = process_json()

    tasks = [download_table(file_prefix, url) for file_prefix, url in pairs.items()]
    await asyncio.gather(*tasks)

    convert_to_csv()


if __name__ == "__main__":
    asyncio.run(prepare_data())