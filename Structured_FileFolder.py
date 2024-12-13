import os
import shutil
import argparse

def organize_files(source_dir, destination_dir, overwrite=False):
    """
    Organizes files by moving them to the destination and cleaning up empty folders.
    Args:
        source_dir (str): Root directory to search for files.
        destination_dir (str): Destination directory for storing files.
        overwrite (bool): Flag to allow overwriting files in the destination.
    """
    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Walk through all subdirectories and files
    for root, dirs, files in os.walk(source_dir):
        # Filter for PDF files in the current directory
        pdf_files = [file for file in files if file.lower().endswith('.pdf')]

        # Move each PDF found to the destination directory
        for pdf in pdf_files:
            pdf_source_path = os.path.join(root, pdf)
            pdf_destination_path = os.path.join(destination_dir, pdf)

            if os.path.exists(pdf_destination_path):
                if overwrite:
                    print(f"Overwriting existing file: {pdf_destination_path}")
                    shutil.move(pdf_source_path, pdf_destination_path)
                else:
                    print(f"File already exists at destination: {pdf_destination_path}. Skipping.")
                    continue
            else:
                shutil.move(pdf_source_path, pdf_destination_path)
                print(f"Moved: {pdf_source_path} to {pdf_destination_path}")

        # After processing files, check if the directory is empty and delete it
        if not os.listdir(root):
            os.rmdir(root)
            print(f"Deleted empty folder: {root}")

if __name__ == "__main__":
    # Argument parser for CLI usage
    parser = argparse.ArgumentParser(description="Organize files and clean up empty folders.")
    parser.add_argument("source", help="Source directory to search for files.")
    parser.add_argument("destination", help="Destination directory for storing files.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting files in the destination directory."
    )
    args = parser.parse_args()

    # Call the main function
    organize_files(args.source, args.destination, args.overwrite)
