import os
import subprocess
import shutil

# Set the source (SD card) and destination folder
source = "D:/record/"  # Change this to your SD card path
destination = "C:/RobotVideos/"  # Change to your desired folder

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

