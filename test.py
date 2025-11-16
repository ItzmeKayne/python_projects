from flask import Flask, render_template
import os
import glob

app = Flask(__name__)

@app.route('/')
def test():
    upload_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    print(f"Looking in: {upload_path}")
    
    all_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
        files = glob.glob(os.path.join(upload_path, ext))
        if files:
            all_files.extend([os.path.basename(f) for f in files])
            
    print(f"Found files: {all_files}")
    
    return f"""
    <h1>Files in uploads folder:</h1>
    <pre>{upload_path}</pre>
    <ul>
        {''.join(f'<li><img src="/static/uploads/{f}" style="max-width:300px"><br>{f}</li>' for f in all_files)}
    </ul>
    <hr>
    <h2>No files? Add them here:</h2>
    <p>Put your photos in this folder:<br>
    {upload_path}</p>
    <p>Name them like this:<br>
    - Romantic photos: r_photo1.jpg, r_date.jpg, etc.<br>
    - Playful photos: p_fun.jpg, p_beach.jpg, etc.</p>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5001)