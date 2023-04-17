import datetime as DT
import os
import json
from extractor import (
    extract_image_metadata,
    extract_file_metadata,
    extract_exif_metadata,
    convert_epoch_to_iso_8601_utc,
    generate_json_file_path,
    process_image,
)

IMAGE_ONE_LOCATION = "tests/data/JAM19896.jpg"
IMAGE_ONE_JSON_LOCATION = "tests/data/JAM19896.json"
IMAGE_TWO_LOCATION = "tests/data/JAM26284.jpg"
IMAGE_TWO_JSON_LOCATION = "tests/data/JAM26284.json"

NO_EXIF_IMAGE_LOCATION = "tests/data/ducky.jpg"


def test_formats_epoch_to_iso_8601_utc_correctly():
    date_time = convert_epoch_to_iso_8601_utc(1681648664.58)
    assert date_time == "2023-04-16T12:37:44.580000Z"


def test_extracts_and_formats_file_metadata_correctly():

    # ctime/mtime will change whenever someone downloads the project so can't hardcode
    img_one_ctime: str = generate_timestamp(os.path.getctime(IMAGE_ONE_LOCATION))
    img_one_mtime: str = generate_timestamp(os.path.getmtime(IMAGE_ONE_LOCATION))
    img_two_ctime: str = generate_timestamp(os.path.getctime(IMAGE_TWO_LOCATION))
    img_two_mtime: str = generate_timestamp(os.path.getmtime(IMAGE_TWO_LOCATION))

    metadata_one: dict = extract_file_metadata(IMAGE_ONE_LOCATION)
    metadata_two: dict = extract_file_metadata(IMAGE_TWO_LOCATION)

    assert metadata_one["filename"] == "JAM19896.jpg"
    assert metadata_one["size"] == 3014190
    assert metadata_one["created_time"] == img_one_ctime
    assert metadata_one["modified_time"] == img_one_mtime
    assert metadata_two["filename"] == "JAM26284.jpg"
    assert metadata_two["size"] == 2444055
    assert metadata_two["created_time"] == img_two_ctime
    assert metadata_two["modified_time"] == img_two_mtime


def test_extracts_and_formats_exif_metadata_correctly():
    img_one_exif_metadata: dict = extract_exif_metadata(IMAGE_ONE_LOCATION)
    img_two_exif_metadata: dict = extract_exif_metadata(IMAGE_TWO_LOCATION)

    assert img_one_exif_metadata["orientation"] == 1
    assert img_one_exif_metadata["capture_time"] == "2019:07:26 13:25:33"
    assert img_one_exif_metadata["camera_model"] == "Canon EOS 5D Mark IV"
    assert img_one_exif_metadata["camera_serial"] == "025021000537"

    assert img_two_exif_metadata["orientation"] == 1
    assert img_two_exif_metadata["capture_time"] == "2020:01:30 09:28:07"
    assert img_two_exif_metadata["camera_model"] == "Canon EOS 5D Mark IV"
    assert img_two_exif_metadata["camera_serial"] == "025021000535"


def test_correctly_extracts_all_metadata():
    # ctime/mtime will change whenever someone downloads the project so can't hardcode
    img_one_ctime: str = generate_timestamp(os.path.getctime(IMAGE_ONE_LOCATION))
    img_one_mtime: str = generate_timestamp(os.path.getmtime(IMAGE_ONE_LOCATION))
    img_two_ctime: str = generate_timestamp(os.path.getctime(IMAGE_TWO_LOCATION))
    img_two_mtime: str = generate_timestamp(os.path.getmtime(IMAGE_TWO_LOCATION))

    img_one_metadata = extract_image_metadata(IMAGE_ONE_LOCATION)
    img_two_metadata = extract_image_metadata(IMAGE_TWO_LOCATION)

    assert img_one_metadata["orientation"] == 1
    assert img_one_metadata["capture_time"] == "2019:07:26 13:25:33"
    assert img_one_metadata["camera_model"] == "Canon EOS 5D Mark IV"
    assert img_one_metadata["camera_serial"] == "025021000537"
    assert img_one_metadata["filename"] == "JAM19896.jpg"
    assert img_one_metadata["size"] == 3014190
    assert img_one_metadata["created_time"] == img_one_ctime
    assert img_one_metadata["modified_time"] == img_one_mtime

    assert img_two_metadata["orientation"] == 1
    assert img_two_metadata["capture_time"] == "2020:01:30 09:28:07"
    assert img_two_metadata["camera_model"] == "Canon EOS 5D Mark IV"
    assert img_two_metadata["camera_serial"] == "025021000535"
    assert img_two_metadata["filename"] == "JAM26284.jpg"
    assert img_two_metadata["size"] == 2444055
    assert img_two_metadata["created_time"] == img_two_ctime
    assert img_two_metadata["modified_time"] == img_two_mtime


def test_handles_missing_exif_values():
    # ctime/mtime will change whenever someone downloads the project so can't hardcode
    no_exif_img_ctime: str = generate_timestamp(os.path.getctime(NO_EXIF_IMAGE_LOCATION))
    no_exif_img_mtime: str = generate_timestamp(os.path.getmtime(NO_EXIF_IMAGE_LOCATION))

    no_exif_img_metadata = extract_image_metadata(NO_EXIF_IMAGE_LOCATION)

    assert "orientation" not in no_exif_img_metadata
    assert "capture_time" not in no_exif_img_metadata
    assert "camera_model" not in no_exif_img_metadata
    assert "camera_serial" not in no_exif_img_metadata
    assert no_exif_img_metadata["filename"] == "ducky.jpg"
    assert no_exif_img_metadata["size"] == 7475
    assert no_exif_img_metadata["created_time"] == no_exif_img_ctime
    assert no_exif_img_metadata["modified_time"] == no_exif_img_mtime


def test_generates_json_file_path():
    image_one_file_path: str = generate_json_file_path(IMAGE_ONE_LOCATION)
    assert image_one_file_path == "tests/data/JAM19896.json"


def test_writes_json_to_path():
    img_one_ctime: str = generate_timestamp(os.path.getctime(IMAGE_ONE_LOCATION))
    img_one_mtime: str = generate_timestamp(os.path.getmtime(IMAGE_ONE_LOCATION))

    if os.path.exists(IMAGE_ONE_JSON_LOCATION):
        os.remove(IMAGE_ONE_JSON_LOCATION)

    process_image(IMAGE_ONE_LOCATION)

    with open(IMAGE_ONE_JSON_LOCATION, "rb") as json_file:
        image_dict = json.load(json_file)

        assert image_dict["orientation"] == 1
        assert image_dict["capture_time"] == "2019:07:26 13:25:33"
        assert image_dict["camera_model"] == "Canon EOS 5D Mark IV"
        assert image_dict["camera_serial"] == "025021000537"
        assert image_dict["filename"] == "JAM19896.jpg"
        assert image_dict["size"] == 3014190
        assert image_dict["created_time"] == img_one_ctime
        assert image_dict["modified_time"] == img_one_mtime


def test_handles_bad_file_names():
    pass


def test_handles_duplicate_file_names():
    pass


def generate_timestamp(epoch: float):
    return DT.datetime.fromtimestamp(epoch, tz=DT.timezone.utc).isoformat().replace("+00:00", "Z")
