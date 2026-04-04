# YouTube to MP3

A web application to convert YouTube videos to MP3 audio files and download/preview them.

## Notice

YouTube connection may be blocked in some environments. Run this project
locally to use the converter.

## Features

- Convert YouTube videos into MP3 files.
- In-browser audio preview before downloading.
- Simple, responsive web interface.

## Tech Stack

- Backend: Python (`app.py`, `download.py`)
- Frontend: HTML templates in `templates/` and static assets in `static/`

## Installation & Setup

1. Install the FFmpeg binary (required):
   - **Ubuntu/Debian**

     ```bash
     sudo apt update && sudo apt install -y ffmpeg
     ```

   - **Fedora**

     ```bash
     sudo dnf install -y ffmpeg
     ```

   - **Arch Linux**

     ```bash
     sudo pacman -S ffmpeg
     ```

   - **macOS (Homebrew)**

     ```bash
     brew install ffmpeg
     ```

   - **Windows**

     Install FFmpeg from the official site and make sure `ffmpeg` is available in your system `PATH`.

2. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the application server:

   ```bash
   python app.py
   ```

4. Open your web browser and navigate to the local server address provided in the terminal.

The app is served by Flask, so the main page and assets should be opened through the local server.

## Usage

1. Paste a valid YouTube URL into the input field.
2. Click the "Convert" button.
3. Wait for the server to process the video.
4. Preview the resulting audio in the browser or click "Download MP3" to save the file.
