from __future__ import unicode_literals
import yt_dlp as youtube_dl
import os
import streamlit as st
import re
import platform
import subprocess

# Function to validate YouTube URL
def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    return bool(youtube_regex.match(url))

# Function to open a file or folder
def open_file(filepath):
    if platform.system() == "Windows":
        os.startfile(filepath)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", filepath])
    else:  # Linux
        subprocess.call(["xdg-open", filepath])

# Streamlit App
def main():
    st.title("YouTube Downloader")

    # Input YouTube link
    url = st.text_input("Enter YouTube URL:")

    # Validate URL
    if url and not is_valid_youtube_url(url):
        st.error("Invalid YouTube URL")

    # If valid URL, show options
    if is_valid_youtube_url(url):
        # Toggle for video or audio
        download_audio = st.checkbox("Download Audio Only")

        # Select destination folder
        default_folder = os.path.expanduser("~/Downloads")
        dest_folder = st.text_input(
            "Destination Folder:", value=default_folder)

        # Download button
        if st.button("Download"):
            try:
                # Create folder if it doesn't exist
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)

                # Define options for yt-dlp
                ydl_opts = {
                    'outtmpl': os.path.join(dest_folder, '%(title)s-%(id)s.%(ext)s'),
                }
                if download_audio:
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    })
                else:
                    ydl_opts.update({'format': 'best'})

                # Download the content
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    downloaded_file = ydl.prepare_filename(info_dict)
                    if download_audio:
                        downloaded_file = os.path.splitext(downloaded_file)[0] + ".mp3"

                st.success(f"Download completed! File saved to: {downloaded_file}")
                open_file(downloaded_file)

            except Exception as e:
                st.error(f"An error occurred: {e}")