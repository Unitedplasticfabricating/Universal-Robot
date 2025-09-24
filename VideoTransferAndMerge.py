import os
import subprocess
import shutil
import cv2 # pip3 install opencv-python
import numpy as np
from collections import deque
# install ffmpeg from https://www.gyan.dev/ffmpeg/builds/ (ffmpeg-release-full.7z)

SDletter = 'D:\\' # SDcard drive letter
RVletter = 'H:\\' # RobotVideos folder drive letter
PermLoc = 'K:\\calvin\\robotvideos\\' # Permanent location for saving the processed files

def main():
    user_input = input('Do All? (Not Including Copy To Permanent) (Y/N): ')
    if isUserInputYes(user_input):
        deleteBSfromFlash()
        copyVideosFromMicroSD()
        mergeVideoFiles()
        deleteRaw()
    else:
        user_input = input('Delete BS from Flash? (Y/N): ')
        if isUserInputYes(user_input):
            deleteBSfromFlash()
        user_input = input('Copy Videos From MicroSD? (Y/N): ')
        if isUserInputYes(user_input):
            copyVideosFromMicroSD()
        user_input = input('Merge Video Files? (Y/N): ')
        if isUserInputYes(user_input):
            mergeVideoFiles()
        user_input = input('Delete Raw? (Y/N): ')
        if isUserInputYes(user_input):
            deleteRaw()
    user_input = input('Copy To Permanent? (Y/N): ')
    if isUserInputYes(user_input):
        sendProcessedToPermanentLocation()
        
def isUserInputYes(input_string):
    # Convert input string to lowercase for case-insensitive comparison
    normalized_input = input_string.lower()
    # List of possible variations of "yes"
    yes_variations = ['yes', 'y']
    # Check if the normalized input is in the list of variations
    ret = normalized_input in yes_variations
    return ret

def deleteBSfromFlash():
    '''
    deletes .ota folder, log folder, time_lapse folder. 
    goes into record and deletes things before 2025, deletes things from hours < 5 or > 17
    '''
    otafolder = os.path.join(SDletter, '.ota')
    logfolder = os.path.join(SDletter, 'log')
    timelapsefolder = os.path.join(SDletter, 'time_lapse')
    if os.path.isdir(otafolder):
        print(f"Deleting '{otafolder}' ... ")
        shutil.rmtree(otafolder) 
        print(f"All files and folders in '{otafolder}' deleted. ")
    if os.path.isdir(logfolder):
        print(f"Deleting '{logfolder}' ... ")
        shutil.rmtree(logfolder) 
        print(f"All files and folders in '{logfolder}' deleted. ")
    if os.path.isdir(timelapsefolder):
        print(f"Deleting '{timelapsefolder}' ... ")
        shutil.rmtree(timelapsefolder) 
        print(f"All files and folders in '{timelapsefolder}' deleted. ")
    # part 2
    recordfolder = os.path.join(SDletter, 'record')
    for item in os.listdir(recordfolder):
        source_item = os.path.join(recordfolder, item)
        if os.path.isdir(source_item):
            datestring = item
            year = datestring[0:4]
            month = datestring[4:6]
            day = datestring[6:8]
            for hour1 in os.listdir(source_item):
                hourfolderpath = os.path.join(source_item, hour1) # once per hour
                iyear = int(year)
                ihour = int(hour1)
                if iyear < 2025 or ihour < 5 or ihour > 17:
                    # delete hourfolderpath
                    print(f"Deleting '{hourfolderpath}' ... ")
                    shutil.rmtree(hourfolderpath)
                    print(f"All files and folders in '{hourfolderpath}' deleted. ")
    

def copyVideosFromMicroSD():
    '''
    deletes destination folder. then recursively copies source folder into destination folder. then deletes source folder. 
    '''
    root_source_folder = SDletter
    source_folder = os.path.join(root_source_folder, 'record')
    destination_folder = os.path.join(RVletter, r"RobotVideos\Raw") 
    # delete destination folder if it exists and if source_folder exists
    if os.path.isdir(source_folder):
        if os.path.isdir(destination_folder):
            print(f"Deleting '{destination_folder}' ... ")
            shutil.rmtree(destination_folder)
            print(f"All files and folders in '{destination_folder}' deleted. ")
        copied = copy_folder(source_folder, destination_folder)
        if copied == True:
            # the code below was deleted
            '''
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
            '''
            # delete the record folder
            print(f"Deleting source folder '{source_folder}' from SD source...")
            shutil.rmtree(source_folder)
        else:
            print(f"Not Deleting source folder '{source_folder}' from SD source.")
    else:
        print(f"Error: Source folder '{source_folder}' not found.")
        
def mergeVideoFiles():
    '''
    first it finds all the video files of the first hour
    then it copies the files into the robotvideos / Processing folder. 
    then it creates a filelist of those files, in the robotvideos folder
    then it runs ffmpeg on those files, and puts each video in its correct spot in the processed folder. 
    then it continues with all the other hours. 
    then it deletes the raw and processing folders. (not in this function, in the next function
    '''
    source_folder = os.path.join(RVletter, r"RobotVideos\Raw") 
    temp_folder = os.path.join(RVletter, r"RobotVideos\Processing")
    destination_folder = os.path.join(RVletter, r"RobotVideos\Processed")
    for date1 in os.listdir(source_folder):
        datefolderpath = os.path.join(source_folder, date1) # once per day
            
        if os.path.isdir(datefolderpath):
            datestring = date1
            year = datestring[0:4]
            month = datestring[4:6]
            day = datestring[6:8]
            for hour1 in os.listdir(datefolderpath):
                hourfolderpath = os.path.join(datefolderpath, hour1) # once per hour
                copied = copy_folder(hourfolderpath, temp_folder) # copy this hour's files to temp
                
                # delete things that are corrupted
                print("Checking for corrupted files ... ")
                lists = delete_corrupted_mp4_files_in_directory(temp_folder)
                print(f"Deleted '{lists}' because they were corrupt")
                
                # make the destination folder if it doesn't already exist
                dest_string = os.path.join(destination_folder, year)
                dest_string = os.path.join(dest_string, month)
                dest_string = os.path.join(dest_string, day)
                print(f"dest_string '{dest_string}' ")
                if not os.path.isdir(dest_string):
                    os.makedirs(dest_string)

                # if the current hour already has a video, move it from the destination folder to the temp folder. this will merge the video in with the rest, not delete/replace it
                videoname = "cobot-cam-1_" + hour1 + "-oclock.mp4"
                videofilename = os.path.join(dest_string, videoname)
                videotempfilename = os.path.join(temp_folder, videoname)
                if os.path.isfile(videofilename):
                    print(f"Copying '{videofilename}' to '{videotempfilename}' for merge ...")
                    shutil.copy(videofilename, videotempfilename)
                    print(f"Deleting '{videofilename}' ...")
                    os.remove(videofilename)

                # Step 3: Create a list of video files for FFmpeg
                # this is based on all the videos that are currently in the temp folder
                print("Creating file list for merging...")
                file_list = [f"file '{os.path.join(temp_folder, file)}'" for file in os.listdir(temp_folder) if file.endswith(".mp4")]

                # Write the file list to a text file
                with open("filelist.txt", "w") as f:
                    for file in file_list:
                        f.write(f"{file}\n")
                
                # Step 4: Merge the video files using FFmpeg
                print("Merging video files...")
                videoname = "cobot-cam-1_" + hour1 + "-oclock.mp4"
                subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "filelist.txt", "-c", "copy", os.path.join(dest_string, videoname)])

                # delete processing folder
                print(f"Deleting '{temp_folder}' ...")
                shutil.rmtree(temp_folder)
                print(f"All files and folders in '{temp_folder}' deleted. ")

def deleteRaw():
    rawfolder = os.path.join(RVletter, r"\RobotVideos\Raw")
    processingfolder = os.path.join(RVletter, r"RobotVideos\Processing")
    filelistfile = os.path.join(RVletter, r"RobotVideos\filelist.txt")

    print(f"Deleting '{rawfolder}' ... ")
    shutil.rmtree(rawfolder)
    print(f"All files and folders in '{rawfolder}' deleted. ")
    os.remove(filelistfile)
    print(f"File '{filelistfile}' deleted. ")

def sendProcessedToPermanentLocation():
    processedfolder = os.path.join(RVletter, r"RobotVideos\Processed")
    permanentStorageFolder = os.path.join(PermLoc, r"Processed")
    move_folder_without_overwriting(processedfolder, permanentStorageFolder)

            


def check_video_file(file_path):
    try:
        # Run ffmpeg to probe the file
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-i', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # If ffmpeg exits without error, the file is valid
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return False

def delete_corrupted_mp4_files_in_directory(directory):
    corrupted_files = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.mp4'):
            file_path = os.path.join(directory, filename)
            if not check_video_file(file_path):
                corrupted_files.append(filename)
                # now delete the files
                deletethisfile = os.path.join(directory, filename)
                os.remove(deletethisfile)
    return corrupted_files

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

def move_folder_without_overwriting(source_folder, destination_folder):
    """
    Recursively moves a folder from source to destination without overwriting existing files.
    Files that already exist in the destination (same path and name) are skipped and not deleted from source.
    After copying, source files that were copied are deleted. Empty folders are removed.

    Args:
        source_folder (str): Path to the folder to move.
        destination_folder (str): Path to move the folder into.
    
    Returns:
        True if successful, False if any errors occurred (but it continues as much as possible).
    """
    success = True

    for root, dirs, files in os.walk(source_folder, topdown=False):
        # Construct relative path from source base
        rel_path = os.path.relpath(root, source_folder)
        dest_root = os.path.join(destination_folder, rel_path)

        # Ensure destination subdirectory exists
        os.makedirs(dest_root, exist_ok=True)

        # Copy files
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)

            try:
                if os.path.exists(dest_file):
                    print(f"Skipped (already exists): {dest_file}")
                    continue
                shutil.copy2(src_file, dest_file)
                os.remove(src_file)
                print(f"Copied and deleted: {src_file} -> {dest_file}")
            except Exception as e:
                print(f"Error copying {src_file} to {dest_file}: {e}")
                success = False

        # Attempt to remove the directory if empty after processing
        try:
            if not os.listdir(root):  # If empty
                os.rmdir(root)
                print(f"Removed empty folder: {root}")
        except Exception as e:
            print(f"Error removing folder {root}: {e}")
            success = False

    return success


if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    main()
