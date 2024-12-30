import os
import subprocess
import sys

def main():
    # Get the absolute path to the Streamlit script
    script_path = os.path.join(os.path.dirname(__file__), "youtube_downloader.py")

    # Run Streamlit and ensure logs are displayed
    process = subprocess.run(
        [sys.executable, "-m", "streamlit", "run", script_path],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    # Check for errors
    if process.returncode != 0:
        print("Streamlit failed to start.")

if __name__ == "__main__":
    main()
