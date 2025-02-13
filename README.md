# FileStructureToolbox
Usefull tools for filesystem structuring
# README: File Organizer Script

## Overview
This script organizes files by copying or moving them from a source directory to a destination directory, based on specified file extensions. Additionally, it can clean up empty folders if files are moved.

## Features
- Supports **copying** (default) or **moving** files.
- Allows filtering files by **extensions**.
- Provides an option to **overwrite existing files** in the destination.
- Automatically **removes empty folders** after moving files.
- Works recursively through **subdirectories**.

## Usage
### Command-line Arguments
```sh
python script.py <source_directory> <destination_directory> [OPTIONS]
```

### Arguments:
| Argument         | Description |
|-----------------|-------------|
| `source`        | Source directory to search for files. |
| `destination`   | Destination directory to store files. |
| `--extensions`  | Space-separated list of file extensions to filter (default: `.pdf .xml .jpg .tif .png .txt .md .json`). |
| `--overwrite`   | Enables overwriting files in the destination directory. |
| `--move`        | Moves files instead of copying them. |

### Examples
#### 1. **Copy files (default behavior)**
```sh
python script.py /path/to/source /path/to/destination
```

#### 2. **Move files instead of copying**
```sh
python script.py /path/to/source /path/to/destination --move
```

#### 3. **Copy only `.txt` and `.pdf` files**
```sh
python script.py /path/to/source /path/to/destination --extensions .txt .pdf
```

#### 4. **Move all specified files and overwrite existing ones**
```sh
python script.py /path/to/source /path/to/destination --move --overwrite
```

## Requirements
- Python 3.x

## Installation
1. Clone or download the script.
2. Ensure you have Python installed (`python --version`).
3. Run the script using the command-line examples above.

## Notes
- If `--move` is used, empty directories in the source folder will be deleted.
- Ensure you have the correct permissions to access source and destination directories.

## License
MIT License
