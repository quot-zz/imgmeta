import datetime as DT
import os
import platform
import json
import argparse
from typing import Dict, List
from exif import Image
import logging

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger("imgmeta")

EXIF_MAPPING = {
    "orientation": "orientation",
    "datetime_original": "capture_time",
    "model": "camera_model",
    "body_serial_number": "camera_serial",
}


def process_files(files: List, results_file: str):
    file_set: set = {s for s in files}

    results: list = []

    logger.info(f"Processing {len(files)} files. Found {len(file_set)} unique files.")

    success: int = 0

    for file in file_set:
        try:
            results.append({"file": file, "result": process_image(file), "error": ""})

            success += 1
        except Exception as e:
            logger.exception(f"Error occurred processing {file}")
            results.append({"file": file, "result": "Failure", "error": e})

    logger.info(f"{success} out of {len(file_set)} unique files were successfully processed.")

    if results_file:
        with open(results_file, "w") as results_file:
            results_file.write(f"File, Result, Error {os.linesep}")
            for result in results:
                results_file.write(
                    f"{result['file']}, {result['result']}, {result['error']} {os.linesep}"
                )


def process_image(image_location: str) -> str:

    if not os.path.exists(image_location):
        raise Exception("File does not exist")

    image_metadata: dict = extract_image_metadata(image_location)

    json_file_path = generate_json_file_path(image_location)

    with open(json_file_path, "w") as json_file:
        json_file.write(json.dumps(image_metadata))

    return "Success"


def extract_image_metadata(image_location: str) -> Dict:
    file_metadata: dict = extract_file_metadata(image_location)
    exif_metadata: dict = extract_exif_metadata(image_location)

    return {**file_metadata, **exif_metadata}


def extract_exif_metadata(image_location: str) -> Dict:
    exif_metadata: dict = {}

    with open(image_location, "rb") as image_file:
        img = Image(image_file)

        existing_exif_attrs: list = img.list_all()

        for mapping in EXIF_MAPPING:
            if mapping in existing_exif_attrs:
                exif_metadata[EXIF_MAPPING[mapping]] = img.get(mapping)

    return exif_metadata


def extract_file_metadata(image_location: str) -> Dict:
    metadata: dict = {}
    metadata["filename"] = os.path.basename(image_location)
    metadata["size"] = os.path.getsize(image_location)

    metadata["created_time"] = convert_epoch_to_iso_8601_utc(
        get_creation_time(image_location)
    )  # This is sometimes incorrect on Unix systems
    metadata["modified_time"] = convert_epoch_to_iso_8601_utc(os.path.getmtime(image_location))

    return metadata


def get_creation_time(image_location: str) -> float:
    if platform.system() == "Windows":
        return os.path.getctime(image_location)
    else:
        stat = os.stat(image_location)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime


def generate_json_file_path(image_location: str) -> str:
    path = os.path.dirname(image_location)
    basename = os.path.basename(image_location)
    split = basename.split(".")

    json_filename = (basename if len(split) == 1 else ".".join(split[:-1])) + ".json"

    return path + os.sep + json_filename


def convert_epoch_to_iso_8601_utc(epoch: float) -> str:
    return DT.datetime.fromtimestamp(epoch, DT.timezone.utc).isoformat().replace("+00:00", "Z")


def main():
    parser = argparse.ArgumentParser(
        prog="metadata-extractor",
        description="Extracts file and image metadata from a provided list of image files",
    )
    parser.add_argument("files", nargs="+")
    parser.add_argument("-rf", "--results-file", dest="results_file", required=False)
    args = parser.parse_args()

    process_files(args.files, args.results_file)


if __name__ == "__main__":
    main()
