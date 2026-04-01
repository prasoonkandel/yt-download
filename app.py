from flask import Flask, render_template, jsonify, request, send_file
import os
import json
import yt_dlp 
from download import download_audio, create_temps, delete_temp, getBaseTemp

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Hello, World!"}),200

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

        return jsonify({"status":"success", "filename": filename, "folder_id": folder_id, "download": f"/api/mp3/download/{folder_id}/{filename}"}), 200

    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": "Failed to download audio. Please check the URL and try again."}), 400
    
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
        return send_file(file_path, as_attachment = True)    

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
        return send_file(file_path, as_attachment= False)
    
    except Exception as e:
        return jsonify({"error": str(e)},), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)