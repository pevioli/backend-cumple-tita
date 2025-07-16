from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os, io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import json

app = Flask(__name__)

# Configurar Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'
FOLDER_ID = '1IbrABIQXpxd1xa-qSVvM9T4m9yJj-XBn'  # Reemplazar por tu carpeta en Drive


credentials_info = json.loads(os.environ['GOOGLE_CREDS'])
credentials = service_account.Credentials.from_service_account_info(
    credentials_info, scopes=SCOPES)

drive_service = build('drive', 'v3', credentials=credentials)

@app.route('/upload', methods=['POST'])
def upload_photos():
    files = request.files.getlist("photos")
    if not files:
        return "No se enviaron fotos", 400

    for file in files:
        filename = secure_filename(file.filename)
        file_metadata = {
            'name': filename,
            'parents': [FOLDER_ID]
        }
        media = MediaIoBaseUpload(file.stream, mimetype=file.mimetype)
        drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return jsonify({"message": "Fotos subidas con éxito"}), 200

@app.route('/', methods=['GET'])
def home():
    return "Backend del cumple de Tita activo 🎂"

if __name__ == '__main__':
    app.run()
