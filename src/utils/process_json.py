import json

FILE_PATH = "data/raw/mpu"
JSON_PATH = "data/mpu_urls.json"


def process_json() -> dict[str, str]:
    """Process MPU URLs from json file."""
    
    json_data = load_json()
    pairs = {}

    for faculty in json_data["faculties"]:
        faculty_code = faculty["code"]

        for _, study_type_info in faculty["study_forms"].items():
            study_type_title = study_type_info["title"]

            for _, form_info in study_type_info["forms"].items():
                form_title = form_info["title"]
                url = form_info["url"]

                file_name = f"{faculty_code}_{study_type_title}_{form_title}.txt"
                file_prefix = f"{FILE_PATH}/{file_name}"

                pairs[file_prefix] = url

    return pairs


def load_json() -> str:
    with open(JSON_PATH, encoding="utf-8") as f:
        json_data = json.load(f)
    
    return json_data