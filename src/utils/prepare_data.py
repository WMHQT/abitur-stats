import json
import asyncio

from process_json import process_json
from download_table import download_table


JSON_PATH = "src/data/mpu_urls.json"


async def prepare_data() -> None:
    """Async data preparation pipeline for analytics."""

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    pairs = process_json(json_data)

    tasks = [download_table(file_prefix, url) for file_prefix, url in pairs.items()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(prepare_data())