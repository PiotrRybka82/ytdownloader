from mutagen.flac import FLAC
from mutagen.mp4 import MP4

path = r"C:\repos\yt_download\Front Mission 4 OST - Track 19 - Deserters.flac"
path = r"C:\repos\yt_download\Hands A Dublin Bookbinder.mp4"

# file = FLAC(path)
file = MP4(path)

print(file)