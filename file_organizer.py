import os
import shutil
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename=f'file_organizer_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define file type categories
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.html', '.css', '.java', '.c', '.cpp'],
    'Others': []  # Fallback for uncategorized files
}

def get_category(extension):
    """Return the category for a given file extension."""
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return 'Others'

def ensure_unique_filename(dest_path):
    """Generate a unique filename by appending a number if the file exists."""
    if not os.path.exists(dest_path):
        return dest_path
    base, ext = os.path.splitext(dest_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def organize_files(directory):
    """Organize files in the specified directory into categorized folders."""
    directory = Path(directory).expanduser().resolve()
    if not directory.exists():
        logging.error(f"Directory {directory} does not exist.")
        return

    logging.info(f"Starting file organization in {directory}")

    # Create category folders if they don't exist
    for category in FILE_CATEGORIES.keys():
        category_path = directory / category
        category_path.mkdir(exist_ok=True)

    # Iterate through files in the directory
    for item in directory.iterdir():
        if item.is_file():  # Process only files
            extension = item.suffix
            if not extension:  # Skip files without extensions
                logging.warning(f"Skipping {item.name}: No extension")
                continue

            category = get_category(extension)
            dest_folder = directory / category
            dest_path = dest_folder / item.name

            try:
                # Ensure unique filename
                dest_path = ensure_unique_filename(dest_path)
                # Move the file
                shutil.move(str(item), str(dest_path))
                logging.info(f"Moved {item.name} to {dest_path}")
            except Exception as e:
                logging.error(f"Failed to move {item.name}: {str(e)}")

    logging.info("File organization completed.")

if __name__ == '__main__':
    # Specify the directory to organize (e.g., Downloads folder)
    target_directory = "~/Downloads"  # Modify as needed
    try:
        organize_files(target_directory)
        print(f"File organization completed. Check log at file_organizer_{datetime.now().strftime('%Y%m%d')}.log")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"Script failed: {str(e)}")