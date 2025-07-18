
 Project: YouTube Downloader (MP3 & MP4 Converter)
 Description: Flask-based web app for downloading YouTube videos as MP3 or MP4 using yt-dlp. Since I was bored, I decided to make something unique.
## FEATURES:
 - Convert YouTube videos to high-quality MP3 audio
 - Download videos in MP4 format with selectable resolution
 - Shows video quality options with file size estimates
 - Simple and clean frontend using HTML/CSS
 - Easy to deploy and run locally

## DEPENDENCIES:
 Python 3.8+
Flask
 yt-dlp
 ffmpeg (must be installed separately)

## INSTALLATION:

install:
	pip install flask yt-dlp

ffmpeg:
# Ubuntu/Debian
sudo apt install ffmpeg
 
# macOS (using brew)
brew install ffmpeg
 
# Windows - Download and add to PATH
 https://ffmpeg.org/download.html

## USAGE:

run:
python app.py

App will start on http://localhost:5000

## HOW TO USE:
 1. Enter a YouTube link in the input box.
 2. Press "Fetch Formats" to see available MP4 options.
 3. Choose between MP3 (audio) or MP4 (video) download.
 4. File will be downloaded to your system.

## DISCLAIMER:
 This tool is intended for educational purposes only.
 Let's respect YouTube’s Terms of Service and do not use this app to download copyrighted content.

