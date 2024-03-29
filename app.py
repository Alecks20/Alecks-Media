from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
import os
import traceback
import random
from dotenv import load_dotenv
load_dotenv()
from libraries import gen

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
AUTH_KEY = os.environ["AUTH_KEY"]
APP_URL = os.environ["APP_URL"]

@app.route('/gui/upload', methods=['POST'])
def upload_gui():
    authorization_token = request.form.get('authorization')
    if authorization_token != AUTH_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    file = request.files['file']
    final_code = []
    for i in range(20):
      final_code.append(random.choice(gen))
    filename = "".join(final_code)
    filename = filename.replace(", ", "")
    filename = filename + "-" + file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(APP_URL + "/uploads/" + filename)

@app.route('/upload', methods=['POST'])
def upload_file():
  try:
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    if 'Authorization' not in request.headers or request.headers['Authorization'] != f"Bearer {AUTH_KEY}":
        return jsonify({'error': 'Unauthorized'}), 401
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:

        final_code = []
        for i in range(20):
           final_code.append(random.choice(gen))
        filename = "".join(final_code)
        filename = filename.replace(", ", "")

        filename = filename + "-" + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': 'File uploaded successfully', 'filename': filename, 'url': APP_URL + "/api/uploads/" + filename})
  except Exception:
      print(traceback.format_exc)

@app.route('/uploads/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host="0.0.0.0",debug=True,port=8032)