# This is a program that takes the programs from the usb drive\programs and copies them into local\programs
# and extracts them into origfilename_extracted.urp files
import shutil
import os
from pathlib import Path
import gzip

def main():
    robot_number = input('Enter Robot Number: ')
    user_input = input('Copy Journal? (Y/N): ')
    if isUserInputYes(user_input):
        copyJournal()
    user_input = input('Copy Files From Flash Drive? (Y/N): ')
    if isUserInputYes(user_input):
        copyFilesFromFlashDrive(robot_number)
    user_input = input('Extract .unc files? (Y/N): ')
    if isUserInputYes(user_input):
        extractUncFiles(robot_number)
    user_input = input('Delete .bak and .old files? (Y/N): ')
    if isUserInputYes(user_input):
        delete_bak_old_files(robot_number)
    
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
    '''
    recursive copying of the entire folder. returns true if there is no error in copying files in any place, and false if it did. if there is an error, it does try to continue copying though. sometimes. 
    '''
    ret = True
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
                ret2 = copy_folder(source_item, destination_item)
                ret = ret and ret2
            else:
                # Copy file from source to destination, overwriting if necessary
                shutil.copy2(source_item, destination_item)
                print(f"Copied '{source_item}' to '{destination_item}'")
        
        print(f"Successfully copied folder '{source_folder}' to '{destination_folder}'")
    except FileNotFoundError:
        print(f"Error: Source folder '{source_folder}' not found.")
        return False
    except PermissionError:
        print(f"Error: Permission denied while copying folder '{source_folder}' to '{destination_folder}'")
        return False
    except Exception as e:
        print(f"Error: Failed to copy folder '{source_folder}' to '{destination_folder}'. Error: {e}")
        return False
    return ret

def copyFilesFromFlashDrive(robot_number):
    '''
    deletes destination folder. then recursively copies source folder into destination folder. then deletes source folder. 
    '''
    source_folder = 'E:\\programs'
    robotnumberstring = 'robot' + robot_number
    destination_folder = os.path.join('C:\\Dev\\universal-robot', robotnumberstring, 'programs')
    # delete destination folder if it exists and if source_folder exists
    if os.path.isdir(source_folder):
        if os.path.isdir(destination_folder):
            print(f"Deleting '{destination_folder}' ... ")
            shutil.rmtree(destination_folder)
            print(f"All files and folders in '{destination_folder}' deleted. ")
        copied = copy_folder(source_folder, destination_folder)
        if copied == True:
            print(f"Deleting '{source_folder}' ... ")
            shutil.rmtree(source_folder)
            print(f"All files and folders in '{source_folder}' deleted. ")
    else:
        print(f"Error: Source folder '{source_folder}' not found.")

def extractUncFiles(robot_number):
    '''
    Takes the .unc files in the Universal-Robot/programs folder and extracts them into other .urp files in the extracted folder.
    Currently does nothing for nested folders. 
    '''
    robotnumberstring = 'robot' + robot_number
    source_folder = os.path.join('C:\\Dev\\universal-robot', robotnumberstring, 'programs')
    destination_folder = os.path.join('C:\\Dev\\universal-robot', robotnumberstring, 'extracted')
    # first, delete the extacted folder
    if os.path.isdir(destination_folder):
        shutil.rmtree(destination_folder)
    # create the extracted folder
    os.makedirs(destination_folder)
    
    # iterate through the contents of the source folder
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        ###destination_item = os.path.join(destination_folder, item)
        if os.path.isdir(source_item):
            extractUncFilesNested(item)
        filename, file_extension = os.path.splitext(source_item)
        if ((file_extension != '.urp') and (file_extension != '.installation') and (file_extension != '.variables')):
            continue # do nothing
        # at this point, the file is a .unc file
        #debug output string
        print(f"extracting '{source_item}' .")
        gzip_file = source_item
        extract_folder = destination_folder
        decompress_gzip(gzip_file, extract_folder)
        
def extractUncFilesNested(subfolderName):
    '''
    If there is one layer of nest, this function also extracts those files from inside a single layer of nest
    '''
    # first, get the modified folder names (source and dest)
    source_folder1 = os.path.join('C:\\Dev\\universal-robot', 'programs')
    source_folder = os.path.join(source_folder1, subfolderName)
    destination_folder1 = os.path.join('C:\\Dev\\universal-robot', 'extracted')
    destination_folder = os.path.join(destination_folder1, subfolderName)
    # then, do the exact same thing as extractUncFiles()
    
    # first, delete the extacted folder
    if os.path.isdir(destination_folder):
        shutil.rmtree(destination_folder)
    # create the extracted folder
    os.makedirs(destination_folder)
    
    # iterate through the contents of the source folder
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        ###destination_item = os.path.join(destination_folder, item)
        if os.path.isdir(source_item):
            continue # do nothing
        filename, file_extension = os.path.splitext(source_item)
        if ((file_extension != '.urp') and (file_extension != '.installation') and (file_extension != '.variables')):
            continue # do nothing
        # at this point, the file is a .unc file
        #debug output string
        print(f"extracting '{source_item}' .")
        gzip_file = source_item
        extract_folder = destination_folder
        decompress_gzip(gzip_file, extract_folder)
    
        
def decompress_gzip(gzip_file, extract_folder):
    '''
    In summary, the actual decompression from GZIP format to the decompressed format happens during the execution of shutil.copyfileobj(f_in, f_out). 
    This line reads the compressed data from the GZIP file (f_in) and writes the decompressed data to the output file (f_out), effectively achieving the extraction process.
    '''
    try:
        # Check if the file is a valid GZIP file
        with gzip.open(gzip_file, 'rb') as f:
            f.read(1)  # Try to read one byte from the file
            f.seek(0)  # Reset file pointer to the beginning
            
        with gzip.open(gzip_file, 'rb') as f_in:
            # Extract the filename from the path
            filename = os.path.basename(gzip_file)
            # Remove the .gz extension from the filename
            filename = filename.replace('.unc', '')
            # Construct the output path
            output_path = os.path.join(extract_folder, filename)
            # Open the output file
            with open(output_path, 'wb') as f_out:
                # Copy data from input to output
                shutil.copyfileobj(f_in, f_out)
        print(f"Successfully decompressed '{gzip_file}' to '{output_path}'")
    except FileNotFoundError:
        print(f"Error: '{gzip_file}' not found.")
    except gzip.BadGzipFile:
        print(f"Error: '{gzip_file}' is not a valid GZIP file.")
    except Exception as e:
        print(f"Error: Failed to decompress '{gzip_file}'. Error: {e}")
        
        
def delete_bak_old_files(robot_number, folder1 = ""):
    '''
    Deletes all files in Universal-Robot/programs folder and nested folders that contain .bak or .old
    '''
    robotnumberstring = 'robot' + robot_number
    if folder1 == "":
        source_folder = os.path.join('C:\\Dev\\universal-robot', robotnumberstring, 'programs')
    else:
        source_folder = folder1 
    # Iterate through all files and subdirectories in the source folder
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        # if this is a folder, skip for now
        if os.path.isdir(source_item):
            delete_bak_old_files(robot_number, source_item)
            continue
        # find the extension
        filename, file_extension = os.path.splitext(source_item)
        file_ext_short = file_extension[:4]
        if file_ext_short == ".bak" or file_ext_short == ".old":
            # delete file
            print(f"removing '{source_item}' ")
            os.remove(source_item)
        


if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    main()