from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import os
import json
import yt_dlp 
import time
import threading
from download import download_audio, create_temps, delete_temp, getBaseTemp
TEMP_LIFETIME = 60 * 15

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_file(os.path.join(app.root_path, 'templates', 'favicon.ico'))

@app.route('/api/mp3', methods=['POST'])
def convert():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if not "url" in data:
        return jsonify({"error": "No URL provided"}), 400
    
    url = data["url"]

    try:
        file_path, temp_path = download_audio(url)

        filename = os.path.basename(file_path)
        folder_id = os.path.basename(temp_path)

        return jsonify({"status":"success", "filename": filename, "folder_id": folder_id, "download": f"/api/mp3/download/{folder_id}/{filename}", "preview": f"/api/mp3/preview/{folder_id}/{filename}"}), 200

    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": "Failed to download audio. The URL might be invalid or the video is restricted."}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/mp3/download/<folder_id>/<filename>')
def download(folder_id, filename):
    BASE_TEMP_FOLDER = getBaseTemp()
    temp_path = os.path.join(BASE_TEMP_FOLDER, folder_id)
    file_path = os.path.join(temp_path, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "Oops file not found"}),404

    try:
        return send_file(file_path, as_attachment = True, mimetype="audio/mpeg")    

    except Exception as e:
        return jsonify({"error":str(e)}),400    

@app.route('/api/mp3/preview/<folder_id>/<filename>')
def preview(folder_id, filename):
    BASE_TEMP_FOLDER = getBaseTemp()
    temp_path = os.path.join(BASE_TEMP_FOLDER, folder_id)
    file_path = os.path.join(temp_path, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "Oops file not found"}), 404

    try:
        return send_file(file_path, as_attachment=False, mimetype="audio/mpeg")
    
    except Exception as e:
        return jsonify({"error": str(e)},), 400
    

@app.route('/api/cleanup/<folder_id>', methods=['POST'])
def cleanup(folder_id):
    BASE_TEMP_FOLDER = getBaseTemp()
    temp_path = os.path.join(BASE_TEMP_FOLDER, folder_id)

    if not os.path.exists(temp_path):
        return jsonify({"error": "Folder not found"}), 404
    
    try:
        delete_temp(temp_path)
        return jsonify({"status": "success", "message": "Temp files cleaned up successfully."}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
def temp_death():    
    while True:
        BASE_TEMP_FOLDER = getBaseTemp()
        now = time.time()
        for folder in os.listdir(BASE_TEMP_FOLDER):
            folder_path = os.path.join(BASE_TEMP_FOLDER, folder)
            if os.path.isdir(folder_path):
                creation_time = os.path.getctime(folder_path)
                if now - creation_time > TEMP_LIFETIME:
                    delete_temp(folder_path)
        time.sleep(60)     

if __name__ == '__main__':
    threading.Thread(target=temp_death, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=False)