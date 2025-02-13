import os
import shutil
import argparse

def organize_files(source_dir, destination_dir, extensions, overwrite=False, move=False):
    """
    Organizes files by copying or moving them to the destination, and cleans up empty folders if moving.

    Args:
        source_dir (str): Root directory to search for files.
        destination_dir (str): Destination directory for storing files.
        extensions (list): List of file extensions to include.
        overwrite (bool): Flag to allow overwriting files in the destination.
        move (bool): Flag to move files instead of copying them.
    """
    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Walk through all subdirectories and files
    for root, dirs, files in os.walk(source_dir, topdown=False):  # Bottom-up to safely remove empty folders
        # Filter for specified file extensions in the current directory
        selected_files = [file for file in files if file.lower().endswith(tuple(extensions))]

        # Process each selected file
        for selected_file in selected_files:
            source_path = os.path.join(root, selected_file)
            destination_path = os.path.join(destination_dir, selected_file)

            if os.path.exists(destination_path):
                if overwrite:
                    print(f"Overwriting existing file: {destination_path}")
                    if move:
                        shutil.move(source_path, destination_path)
                    else:
                        shutil.copy2(source_path, destination_path)
                else:
                    print(f"File already exists at destination: {destination_path}. Skipping.")
                    continue
            else:
                if move:
                    shutil.move(source_path, destination_path)
                    print(f"Moved: {source_path} → {destination_path}")
                else:
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied: {source_path} → {destination_path}")

        # If moving files, delete empty folders after processing
        if move and not os.listdir(root):  # Ensures the folder is empty before deletion
            os.rmdir(root)
            print(f"Deleted empty folder: {root}")

if __name__ == "__main__":
    # Argument parser for CLI usage
    parser = argparse.ArgumentParser(description="Organize specified file types by copying (default) or moving them.")
    parser.add_argument("source", help="Source directory to search for files.")
    parser.add_argument("destination", help="Destination directory for storing files.")
    parser.add_argument(
        "--extensions", nargs="+", default=[".pdf", ".xml", ".jpg", ".tif", ".png", ".txt", ".md", ".json"],
        help="List of file extensions to include. Default: .pdf, .xml, .jpg, .tif, .png, .txt, .md, .json"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting files in the destination directory."
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files instead of copying them."
    )
    args = parser.parse_args()

    # Call the main function
    organize_files(args.source, args.destination, args.extensions, args.overwrite, args.move)
