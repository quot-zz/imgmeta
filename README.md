
# image_metadata_extractor

Script that extracts metadata from a list of provided jpeg images

## Requirements

This project requires [Poetry](https://python-poetry.org/docs/) to run and install. Follow the instructions in the link provided.
  
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