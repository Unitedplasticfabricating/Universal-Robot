# This is a program that takes the programs from the usb drive\programs and copies them into local\programs
# and extracts them into origfilename_extracted.urp files
import shutil
import os
from pathlib import Path

def main():
    user_input = input('Copy Journal? (Y/N): ')
    if isUserInputYes(user_input):
        copyJournal()
    user_input = input('Copy Files From Flash Drive? (Y/N): ')
    if isUserInputYes(user_input):
        copyFilesFromFlashDrive()
    
def isUserInputYes(input_string):
    # Convert input string to lowercase for case-insensitive comparison
    normalized_input = input_string.lower()
    # List of possible variations of "yes"
    yes_variations = ['yes', 'y']
    # Check if the normalized input is in the list of variations
    ret = normalized_input in yes_variations
    return ret
    
def copyJournal():
    documents_folder = Path.home() / "Documents"
    copy_file(documents_folder, 'robotprojectjournal.txt', 'C:\\dev\\universal-robot')
    
    
def copy_file(source_location, filename, destination_location):
    try:
        # Form the complete paths for source and destination files
        src_file = os.path.join(source_location, filename)
        dst_file = os.path.join(destination_location, filename)
        
        # Copy src_file to dst_file, replacing existing file if necessary
        shutil.copy2(src_file, dst_file)
        print(f"Successfully copied '{src_file}' to '{dst_file}'")
    except FileNotFoundError:
        print(f"Error: '{src_file}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied while copying '{src_file}' to '{dst_file}'")
    except Exception as e:
        print(f"Error: Failed to copy '{src_file}' to '{dst_file}'. Error: {e}")
        
def copy_folder(source_folder, destination_folder):
    try:
        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        # Iterate through all files and subdirectories in the source folder
        for item in os.listdir(source_folder):
            source_item = os.path.join(source_folder, item)
            destination_item = os.path.join(destination_folder, item)
            
            # Recursively copy subdirectories and their contents
            if os.path.isdir(source_item):
                copy_folder(source_item, destination_item)
            else:
                # Copy file from source to destination, overwriting if necessary
                shutil.copy2(source_item, destination_item)
                print(f"Copied '{source_item}' to '{destination_item}'")
        
        print(f"Successfully copied folder '{source_folder}' to '{destination_folder}'")
        return True
    except FileNotFoundError:
        print(f"Error: Source folder '{source_folder}' not found.")
        return False
    except PermissionError:
        print(f"Error: Permission denied while copying folder '{source_folder}' to '{destination_folder}'")
        return False
    except Exception as e:
        print(f"Error: Failed to copy folder '{source_folder}' to '{destination_folder}'. Error: {e}")
        return False

        
def copyFilesFromFlashDrive():
    source_folder = 'D:\\programs'
    destination_folder = os.path.join('C:\\Dev\\universal-robot', 'programs')
    # delete destination folder if it exists and if source_folder exists
    if os.path.isdir(source_folder):
        shutil.rmtree(destination_folder)
        copied = copy_folder(source_folder, destination_folder)
        if copied == True:
            shutil.rmtree(destination_folder)
    else:
        print(f"Error: Source folder '{source_folder}' not found.")
        
    




if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    main()