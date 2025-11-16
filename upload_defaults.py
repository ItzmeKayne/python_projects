from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Upload Default Images</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            .form-group { margin: 20px 0; }
            label { display: block; margin-bottom: 5px; }
        </style>
    </head>
    <body>
        <h1>Upload Default Images</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label>Romantic Default Image:</label>
                <input type="file" name="romantic" accept="image/*" required>
            </div>
            <div class="form-group">
                <label>Playful Default Image:</label>
                <input type="file" name="playful" accept="image/*" required>
            </div>
            <button type="submit">Upload Images</button>
        </form>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    upload_folder = 'static/uploads'
    os.makedirs(upload_folder, exist_ok=True)
    
    for tone in ['romantic', 'playful']:
        if tone in request.files:
            file = request.files[tone]
            if file:
                filename = f'default_{tone}.jpg'
                file.save(os.path.join(upload_folder, filename))
    
    return 'Images uploaded successfully! You can close this window.'

if __name__ == '__main__':
    app.run(port=5001)