from flask import Flask, render_template, request, send_from_directory
import os
from pytube import YouTube

app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = os.path.join(app.root_path, 'downloads')
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            yt = YouTube(video_url)
            video = yt.streams.get_highest_resolution()

            video_title = yt.title
            video_filename = f"{video_title}.mp4"
            video_path = os.path.join(app.config['DOWNLOAD_FOLDER'], video_filename)

            video.download(output_path=app.config['DOWNLOAD_FOLDER'])

            return send_from_directory(app.config['DOWNLOAD_FOLDER'], video_filename, as_attachment=True)
        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)