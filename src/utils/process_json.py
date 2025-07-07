FILE_PATH = "src/data/raw/mpu"


def process_json(json_data: str) -> dict[str, str]:
    """Process MPU URLs from json file."""

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
