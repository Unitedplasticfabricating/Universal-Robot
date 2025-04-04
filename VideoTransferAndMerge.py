import os
import subprocess
import shutil

def main():
    user_input = input('Copy Videos From Micro SD? (Y/N): ')
    if isUserInputYes(user_input):
        copyVideosFromMicroSD()
    user_input = input('Merge Files into 1 hour long files? (Y/N): ')
    if isUserInputYes(user_input):
        mergeVideoFiles()
        
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
    root_source_folder = "D:\\" # drive letter
    source_folder = os.path.join(root_source_folder, 'record')
    destination_folder = "C:\\RobotVideos\\Raw\\"
    # delete destination folder if it exists and if source_folder exists
    if os.path.isdir(source_folder):
        if os.path.isdir(destination_folder):
            print(f"Deleting '{destination_folder}' ... ")
            shutil.rmtree(destination_folder)
            print(f"All files and folders in '{destination_folder}' deleted. ")
        copied = copy_folder(source_folder, destination_folder)
        if copied == True:
            # delete all the things on the sd card (cannot delete the sd card itself)
            for item in os.listdir(root_source_folder):
                source_item = os.path.join(root_source_folder, item)
                if item == 'System Volume Information':
                    continue
                if os.path.isdir(source_item):
                    print(f"Deleting '{source_item}' ... ")
                    shutil.rmtree(source_item) # delete entirety of microSD
                    print(f"All files and folders in '{source_item}' deleted. ")
                else:
                    os.remove(source_item)
                    print(f"Deleted '{source_item}' . ")
    else:
        print(f"Error: Source folder '{source_folder}' not found.")
        
def mergeVideoFiles():
    '''
    first it finds all the video files of the first hour
    then it copies the files into the robotvideos\Processing folder. 
    then it creates a filelist of those files, in the robotvideos\ folder
    then it runs ffmpeg on those files, and puts each video in its correct spot in the processed folder. 
    then it continues with all the other hours. 
    then it deletes the raw and processing folders. 
    '''
    source_folder = "C:\\RobotVideos\\Raw\\"
    temp_folder = "C:\\RobotVideos\\Processing\\"
    destination_folder = "C:\\RobotVideos\\Processed\\"
    for date1 in os.listdir(source_folder):
        datefolderpath = os.path.join(source_folder, date1) # once per day
            
        if os.path.isdir(datefolderpath):
            datestring = date1
            year = datestring[0:4]
            month = datestring[4:6]
            day = datestring[6:8]
            for hour1 in os.listdir(datefolderpath):
                hourfolderpath = os.path.join(datefolderpath, hour1) # once per hour
                copied = copy_folder(hourfolderpath, temp_folder)
                
                dest_string = os.path.join(destination_folder, year)
                dest_string = os.path.join(dest_string, month)
                dest_string = os.path.join(dest_string, day)
                print(f"dest_string '{dest_string}' ")
                
                # Step 3: Create a list of video files for FFmpeg
                print("Creating file list for merging...")
                file_list = [f"file '{os.path.join(temp_folder, file)}'" for file in os.listdir(temp_folder) if file.endswith(".mp4")]

                # Write the file list to a text file
                with open("filelist.txt", "w") as f:
                    for file in file_list:
                        f.write(f"{file}\n")
                
            


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
