from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
import os
import traceback
import random
from dotenv import load_dotenv
load_dotenv()
from libraries import gen

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
API_UPLOAD_FOLDER = "./api-uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['API_UPLOADS_FOLDER'] = API_UPLOAD_FOLDER
AUTH_KEY = os.environ["AUTH_KEY"]
APP_URL = os.environ["APP_URL"]
FAVICON = "https://cdn.a3d.pro/uploads/iawzhqbq8ssi-xxckj0k57-wh-pb493hxib-i6sojywwwr22a7uyhi-lj15xgv5pxtc3uyp7lagvfdbadmdx-j1qv98x2-w-8-jyiynxzsnnvrlx6tg-0it-q9en9p6y9p12wxpneopm9eqw8l86ef.png"

@app.route("/")
def index_redirect():
    return render_template("index.html", app_name=os.environ["APP_NAME"], favicon=FAVICON)

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
    return jsonify({'success': 'File uploaded successfully', 'filename': file.filename, 'url': APP_URL + "/uploads/" + filename})

@app.route('/api/upload', methods=['POST'])
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
        file.save(os.path.join(app.config['API_UPLOADS_FOLDER'], filename))
        return jsonify({'success': 'File uploaded successfully', 'filename': filename, 'url': APP_URL + "/api/uploads/" + filename})
  except Exception:
      print(traceback.format_exc)

@app.route('/api/uploads/<filename>', methods=['GET'])
def get_api_image(filename):
    return send_from_directory(app.config['API_UPLOADS_FOLDER'], filename)

@app.route('/uploads/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', text="404 Not Found", favicon=FAVICON), 404

@app.errorhandler(405)
def method_not_allowed(error):
  return render_template("error.html", text="Method Not Allowed", favicon=FAVICON), 405

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(API_UPLOAD_FOLDER):
        os.makedirs(API_UPLOAD_FOLDER)
    app.run(host="0.0.0.0",debug=True,port=8032)