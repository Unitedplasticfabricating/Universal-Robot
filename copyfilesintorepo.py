# This is a program that takes the programs from the usb drive\programs and copies them into local\programs
# and extracts them into origfilename_extracted.urp files
import shutil
import os
from pathlib import Path

def main():
    user_input = input('Copy Journal? (Y/N): ')
    if isUserInputYes(user_input):
        copyJournal()
    
def isUserInputYes(input_string):
    # Convert input string to lowercase for case-insensitive comparison
    normalized_input = input_string.lower()
    # List of possible variations of "yes"
    yes_variations = ['yes', 'y']
    # Check if the normalized input is in the list of variations
    ret = normalized_input in yes_variations
    return ret
    
def copyJournal():
    print('now would copy journal')
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




if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    main()