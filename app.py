from flask import Flask, render_template, jsonify, request
import os
import json 

app = Flask(__name__)



@app.route('/')
def index():
    return jsonify({"message": "Hello, World!"}),200

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if not "url" in data:
        return jsonify({"error": "No URL provided"}), 400
    
    url = data["url"]

    
    return jsonify({"message": "Download started!"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)