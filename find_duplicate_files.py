import os
import hashlib
from collections import defaultdict
import concurrent.futures
import logging
import tempfile
import shutil
import argparse
from progress.bar import Bar

# Setup logging
logging.basicConfig(
    filename='find_duplicates.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def hash_file(filepath, block_size=8192):
    """Compute SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(block_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Error reading file {filepath}: {e}")
        return None

def process_file(filepath, hashes):
    """Hash a file and add its path to the hashes dictionary."""
    file_hash = hash_file(filepath)
    if file_hash:
        hashes[file_hash].append(filepath)

def find_duplicates(directory, file_extensions=None):
    """
    Find duplicate files in a directory.
    - directory: Path to search.
    - file_extensions: List of extensions to filter, e.g., ['.epub', '.pdf'].
    """
    hashes = defaultdict(list)
    temp_dir = None

    # Handle network directories
    if "://" in directory:
        username = os.getenv('NETWORK_USERNAME')
        password = os.getenv('NETWORK_PASSWORD')
        if not (username and password):
            logging.error("Network credentials are missing.")
            return {}
        
        temp_dir = tempfile.mkdtemp()
        mount_cmd = f"mount -t cifs {directory} {temp_dir} -o username={username},password={password}"
        os.system(mount_cmd)
        directory = temp_dir

    # Collect all files
    files = []
    for root, _, filenames in os.walk(directory, followlinks=True):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            # Filter by file extensions if provided
            if file_extensions and not filepath.lower().endswith(tuple(file_extensions)):
                continue
            files.append(filepath)

    # Multithreading and progress bar
    with Bar('Processing', max=len(files), suffix='%(percent)d%%') as bar, concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_file, file, hashes): file for file in files}
        for future in concurrent.futures.as_completed(futures):
            bar.next()

    # Extract duplicates
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}

    # Cleanup temporary mount
    if temp_dir:
        os.system(f"umount {temp_dir}")
        shutil.rmtree(temp_dir)

    return duplicates

def save_duplicates_to_file(duplicates, output_file):
    """Save duplicate results to a text file."""
    with open(output_file, 'w') as f:
        for file_hash, files in duplicates.items():
            f.write(f"Duplicate files with hash {file_hash}:\n")
            for file in files:
                f.write(f"  {file}\n")
            f.write("\n")

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find duplicate files in a directory.')
    parser.add_argument('directory', help='Path to search')
    parser.add_argument('-o', '--output', default='duplicates_report.txt', help='Output file for duplicates report')
    parser.add_argument('-e', '--extensions', nargs='+', default=['.epub', '.pdf', '.mobi'], help='File extensions to filter by')

    args = parser.parse_args()

    directory_to_search = args.directory
    output_file = args.output
    file_extensions = args.extensions

    print(f"Scanning directory: {directory_to_search}")
    duplicates = find_duplicates(directory_to_search, file_extensions)

    if duplicates:
        print(f"\nFound {len(duplicates)} groups of duplicate files.")
        save_duplicates_to_file(duplicates, output_file)
        print(f"Duplicate file report saved to {output_file}")
    else:
        print("No duplicate files found.")
