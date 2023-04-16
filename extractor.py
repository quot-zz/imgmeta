import datetime as DT
import os
from typing import Dict
from exif import Image


def extract_image_data(image_location: str) -> Dict:
    file_metadata: dict = extract_file_metadata(image_location)
    exif_metadata: dict = extract_exif_metadata(image_location)

    return {**file_metadata, **exif_metadata}


def extract_exif_metadata(image_location: str) -> Dict:
    exif_metadata: dict = {}

    with open(image_location, "rb") as image_file:
        img = Image(image_file)

        exif_metadata["orientation"] = int(img.orientation)
        exif_metadata[
            "capture_time"
        ] = img.datetime_original  # Not local or utc but shouldn't have unknown tz applied.
        exif_metadata["camera_model"] = img.model
        exif_metadata["camera_serial"] = img.body_serial_number

    return exif_metadata


def extract_file_metadata(image_location: str) -> Dict:
    metadata: dict = {}
    metadata["filename"] = os.path.basename(image_location)
    metadata["size"] = os.path.getsize(image_location)
    metadata["created_time"] = convert_epoch_to_iso_8601_utc(os.path.getctime(image_location))
    metadata["modified_time"] = convert_epoch_to_iso_8601_utc(os.path.getmtime(image_location))

    return metadata


def convert_epoch_to_iso_8601_utc(epoch: float) -> str:
    return DT.datetime.fromtimestamp(epoch, DT.timezone.utc).isoformat().replace("+00:00", "Z")
