import argparse
#from pytube import YouTube
from pytubefix import YouTube
from tqdm import tqdm
import validators
import os

parser = argparse.ArgumentParser(description="Download YouTube videos")
parser.add_argument('--url', help='Provide a valid YouTube url', required=True)
parser.add_argument('-o', '--output', help='Provide a download directory', required=False, default='downloads')
parser.add_argument('-r', '--resolution', help='Select a desired resolution', default='360p') #720p
args = parser.parse_args()

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Downloaded: {percentage:.2f}%")

download_directory = args.output
if not os.path.isdir(download_directory):
    print("Directory does not exist.  Creating it now...")
    os.mkdir(download_directory)

if not validators.url(args.url):
    print("This is not a valid url. Please try again with a valid url.")
    os._exit(1)

ytObj = YouTube(args.url, on_progress_callback=on_progress)

# Create an empty set
streams = set()

for stream in ytObj.streams.filter(res=args.resolution, progressive=True):
    streams.add(stream.resolution)
print("Resolution: ", streams)

ytObj = ytObj.streams.get_highest_resolution()

if ytObj.resolution != args.resolution:
    print("Sorry, ", ytObj.resolution, " is the highest available resolution.")
print("Title: ", ytObj.title)
print("Highest available resolution: ", ytObj.resolution)
print("File size: ", ytObj.filesize)

try:
        #ytObj.download(output_path=args.output)
        with tqdm(total=ytObj.filesize) as pbar:
             #ytObj.download(output_path=arge.output)
             ytObj.download(output_path=args.output)
             pbar.update(ytObj.filesize)
except:
    print("An error has occurred")
    os._exit(1)

print("Download completed successfully")

#print(args.url)
#print(args.output)
#print(args.resolution)
#Third commit,/