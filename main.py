import argparse
#from pytube import YouTube
from pytubefix import YouTube
from tqdm import tqdm
import validators
import os

# Create parser object
parser = argparse.ArgumentParser(description="Download YouTube videos")

# Add arguments
parser.add_argument('--url', help='Provide a valid YouTube url', required=True)
parser.add_argument('-o', '--output', help='Provide a download directory', required=False, default='downloads')
parser.add_argument('-r', '--resolution', help='Select a desired resolution', default='360p') #720p

# Parse arguments
args = parser.parse_args()

# on-progress function that updates the download progress
def on_progress(stream, chunk, bytes_remaining):
    # Set total_size variable using .filesize method 
    total_size = stream.filesize

    # Calculate bytes downloaded by subtracting bytes remaining from total size
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100

    # Print download progress
    print(f"Downloaded: {percentage:.2f}%")

# Set download_directory variable using input from -o/--output or use 
# default downloads
download_directory = args.output

# Check if directory exists using isdidr method
if not os.path.isdir(download_directory):

    # Print status
    print("Directory does not exist.  Creating it now...")

    # Make the directory
    os.mkdir(download_directory)

# Check if url is valid using validators.url package
if not validators.url(args.url):
    # Print status of check
    print("This is not a valid url. Please try again with a valid url.")
    # If the url is invalid, exit the program
    os._exit(1)

# Create YouTube object and assign it to ytObj variable
ytObj = YouTube(args.url, on_progress_callback=on_progress)

# Create an empty set
streams = set()

# Iterate through streams and filter user or default value.  Filter for
# for progressive streams
for stream in ytObj.streams.filter(res=args.resolution, progressive=True):
    # Add resolution to selected streams
    streams.add(stream.resolution)

# Print selected stream resolution
print("Resolution: ", streams)

# Assign highest available stream to ytObj object variable
ytObj = ytObj.streams.get_highest_resolution()

# Check if selected resolution is equal to user provied resolution
if ytObj.resolution != args.resolution:
    # Print which resolution is assigned to ytObj object
    print("Sorry, ", ytObj.resolution, "is the highest available resolution.")

# Print video title from ytObj.title method
print("Title: ", ytObj.title)

# Print resolution assigned to ytObj object 
print("Highest available resolution: ", ytObj.resolution)

# Print file size using .filesize method
print("File size: ", ytObj.filesize)

# Try to run below code in try block
try:    
        # Iterate through progress process
        with tqdm(total=ytObj.filesize) as pbar:
            # Download video to provided directory
             ytObj.download(output_path=args.output)

             # Update the progress code
             # with new filesize
             pbar.update(ytObj.filesize)
except:
    print("An error has occurred")
    # Above try block failed, so exit program
    os._exit(1)

# Print final message
print("Download completed successfully")

#Fourth commit