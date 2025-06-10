from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_video():
    if 'video' not in request.files:
        return 'No video file uploaded', 400
    
    video = request.files['video']
    if video.filename == '':
        return 'No selected file', 400

    filename = secure_filename(video.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video.save(video_path)

    # Convert video to audio
    try:
        video_clip = VideoFileClip(video_path)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f'audio_{filename}.mp3')
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()

        # Clean up video file
        os.remove(video_path)

        return send_file(audio_path, as_attachment=True)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)