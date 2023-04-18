
# imgmeta

Script that extracts metadata from a list of provided jpeg images

## Description

This script takes in a list of file locations, extracts file and specific EXIF metadata if it exists and outputs a JSON formatted file for each of the specified files. The following metadata is extracted:

* filename
* size (Bytes)
* created_time
* modified_time
* orientation ( Exif.Image.Orientation )
* capture_time ( Exif.Image.DateTimeOriginal )
* camera_model ( Exif.Image.Model )
* camera_serial ( Exif.Image.BodySerialNumber )

## Requirements

This project requires [Poetry](https://python-poetry.org/docs/) to run and install. Follow the instructions in the link provided. If you have Poetry already installed you may have to switch between Python versions if your default is not 3.9

```poetry env use python3.9```
  
## Running the Script

1. Install poetry dependencies using the command below

```poetry install```

2. Run the script

```poetry run python imgmeta/extractor.py tests/data/ducky.jpg ```

### Flags

|Flag|Description  |
|--|--|
| -rf --results-file | Specifies a file to write the results of the operation to in CSV format |

## Installation

1. Build the project

```poetry build```

2. Install from the .whl file

```pip install dist/imgmeta-0.1.0-py3-none-any.whl```

3. You can now run from the command line

```imgmeta tests/data/ducky.jpg```

## Development

1. Install poetry dependencies using the command below

```poetry install```

2. Install the git pre-commit hooks

```poetry run pre-commit install```

## Testing

```poetry run pytest```
