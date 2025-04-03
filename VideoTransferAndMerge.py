import os
import subprocess
import shutil

def main():
    user_input = input('Copy Videos From Micro SD? (Y/N): ')
    if isUserInputYes(user_input):
        copyVideosFromMicroSD()
        
def isUserInputYes(input_string):
    # Convert input string to lowercase for case-insensitive comparison
    normalized_input = input_string.lower()
    # List of possible variations of "yes"
    yes_variations = ['yes', 'y']
    # Check if the normalized input is in the list of variations
    ret = normalized_input in yes_variations
    return ret

def copyVideosFromMicroSD():
    '''
    deletes destination folder. then recursively copies source folder into destination folder. then deletes source folder. 
    '''
    root_source_folder = "D:/" # drive letter
    source_folder = os.path.join(root_source_folder, 'record')
    destination_folder = "C:/RobotVideos/Raw/"
    # delete destination folder if it exists and if source_folder exists
    if os.path.isdir(source_folder):
        if os.path.isdir(destination_folder):
            print(f"Deleting '{destination_folder}' ... ")
            shutil.rmtree(destination_folder)
            print(f"All files and folders in '{destination_folder}' deleted. ")
        copied = copy_folder(source_folder, destination_folder)
        if copied == True:
            print(f"Deleting '{root_source_folder}' ... ")
            shutil.rmtree(root_source_folder) # delete entirety of microSD
            print(f"All files and folders in '{root_source_folder}' deleted. ")
    else:
        print(f"Error: Source folder '{source_folder}' not found.")


def garbage():
    # Step 1: Copy all MP4 files from the SD card to the local folder
    print("Copying files from SD card to local folder...")
    for file_name in os.listdir(source):
        if file_name.endswith(".mp4"):
            shutil.copy(os.path.join(source, file_name), destination)

    # Step 2: Delete the files from the SD card
    print("Deleting files from SD card...")
    for file_name in os.listdir(source):
        if file_name.endswith(".mp4"):
            os.remove(os.path.join(source, file_name))

    # Step 3: Create a list of video files for FFmpeg
    print("Creating file list for merging...")
    file_list = [f"file '{os.path.join(destination, file)}'" for file in os.listdir(destination) if file.endswith(".mp4")]

    # Write the file list to a text file
    with open("filelist.txt", "w") as f:
        for file in file_list:
            f.write(f"{file}\n")

    # Step 4: Merge the video files using FFmpeg
    print("Merging video files...")
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "filelist.txt", "-c", "copy", os.path.join(destination, "merged_video_1hour.mp4")])

    # Step 5: Clean up
    os.remove("filelist.txt")
    print("Process complete!")
    
    
    
    
    # get a list of folders in the \record\ folder
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
            
        # Recursively copy subdirectories and their contents
        if os.path.isdir(source_item):
            datestring = item
            year = datestring[0:4]
            month = datestring[4:6]
            day = datestring[6:8]

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

if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    main()
