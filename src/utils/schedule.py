import os
from datetime import datetime
import asyncio
from functools import partial
from utils.prepare_data import prepare_data

UPDATE_TIME_FILE = "data/update_time.txt"


def set_last_update() -> None:
    os.makedirs(os.path.dirname(UPDATE_TIME_FILE), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(UPDATE_TIME_FILE, "w") as f:
        f.write(now)


def get_last_update() -> str:
    try:
        with open(UPDATE_TIME_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Данные еще не обновлялись."


async def periodic_update():
    """Periodically runs prepare_data() every N seconds."""

    while True:
        print("Running scheduled data update...")
        try:
            await asyncio.get_event_loop().run_in_executor(None, partial(asyncio.run, prepare_data()))
            set_last_update()
            print("Data updated successfully.")
        except Exception as e:
            print(f"Error during data update: {e}")

        # Run every 20 minutes (1200 secs)
        await asyncio.sleep(1200)