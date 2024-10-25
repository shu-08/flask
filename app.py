from flask import Flask, render_template, request, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

# 動画の保存先
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            # ダウンロードされたファイルのフルパスを生成
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_info['title']}.{video_info['ext']}")
        
        return render_template('index.html', download_link=file_path)
    
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(host='10.7.48.56')
