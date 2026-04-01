import yt_dlp
import os
import shutil
import uuid

BASE_TEMP_FOLDER = os.path.join(os.getcwd(), "temp")
os.makedirs(BASE_TEMP_FOLDER, exist_ok=True)

def getBaseTemp():
    return BASE_TEMP_FOLDER

def create_temps():
    rnd_hex = uuid.uuid4().hex
    folder_name = f"temp_{rnd_hex}"
    path = os.path.join(BASE_TEMP_FOLDER, folder_name)
    os.makedirs(path, exist_ok=True)
    return path


def download_audio(url):
    temp_path = create_temps()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_path,'%(title)s.%(ext)s'),
        'restrictfilenames': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',

            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

        if ydl_opts.get("postprocessors"):
            file_path = os.path.splitext(file_path)[0] + ".mp3"

    return file_path, temp_path

def delete_temp(path):
    if os.path.exists(path):
        shutil.rmtree(path)

