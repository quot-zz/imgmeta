import datetime as DT
import os
import json
import argparse
from typing import Dict, List
from exif import Image


def process_files(files: List):
    for file in files:
        process_image(file)


def process_image(image_location: str):
    image_metadata: dict = extract_image_metadata(image_location)

    json_file_path = generate_json_file_path(image_location)

    with open(json_file_path, "w") as json_file:
        json_file.write(json.dumps(image_metadata))


def extract_image_metadata(image_location: str) -> Dict:
    file_metadata: dict = extract_file_metadata(image_location)
    exif_metadata: dict = extract_exif_metadata(image_location)

    return {**file_metadata, **exif_metadata}


def extract_exif_metadata(image_location: str) -> Dict:
    exif_metadata: dict = {}

    with open(image_location, "rb") as image_file:
        img = Image(image_file)

        existing_exif_attr: list = img.list_all()
        if "orientation" in existing_exif_attr:
            exif_metadata["orientation"] = int(img.orientation)

        if "datetime_original" in existing_exif_attr:
            exif_metadata[
                "capture_time"
            ] = img.datetime_original  # Not local or utc but shouldn't have unknown tz applied.

        if "model" in existing_exif_attr:
            exif_metadata["camera_model"] = img.model

        if "body_serial_number" in existing_exif_attr:
            exif_metadata["camera_serial"] = img.body_serial_number

    return exif_metadata


def extract_file_metadata(image_location: str) -> Dict:
    metadata: dict = {}
    metadata["filename"] = os.path.basename(image_location)
    metadata["size"] = os.path.getsize(image_location)
    metadata["created_time"] = convert_epoch_to_iso_8601_utc(os.path.getctime(image_location))
    metadata["modified_time"] = convert_epoch_to_iso_8601_utc(os.path.getmtime(image_location))

    return metadata


def generate_json_file_path(image_location: str) -> str:
    path = os.path.dirname(image_location)
    json_filename = os.path.basename(image_location).split(".")[0] + ".json"

    return path + os.sep + json_filename


def convert_epoch_to_iso_8601_utc(epoch: float) -> str:
    return DT.datetime.fromtimestamp(epoch, DT.timezone.utc).isoformat().replace("+00:00", "Z")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    process_files(args.files)


if __name__ == "__main__":
    main()
