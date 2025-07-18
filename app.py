from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Helper function to map resolution to standard "p" value
def map_resolution_to_p(resolution):
    mapping = {
        "256x144": "144p",
        "426x240": "240p",
        "640x360": "360p",
        "854x480": "480p",
        "1280x720": "720p",
        "1920x1080": "1080p",
        "2560x1440": "1440p",
        "3840x2160": "2160p",  # 4K
    }
    return mapping.get(resolution, resolution)  # Return the mapped "p" value or original resolution if not found

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formats', methods=['POST'])
def formats():
    url = request.form['url']
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
        
        unique_formats = {}
        for f in formats:
            resolution = f.get('resolution', 'Unknown')
            filesize = f.get('filesize', 0)
            filesize_approx = f.get('filesize_approx', 0)
            vcodec = f.get('vcodec', 'none')

            if f['ext'] == 'mp4' and f.get('vcodec') != 'none':
                # Map the resolution to "p" value
                quality = map_resolution_to_p(resolution)

                # Use either exact filesize or approximate size
                size_in_bytes = filesize or filesize_approx
                size_in_mb = f"{round(size_in_bytes / (1024 * 1024), 2)} MB" if size_in_bytes else "Unknown size"

                unique_formats[quality] = {
                    'format_id': f['format_id'],
                    'quality': quality,
                    'size': size_in_mb
                }

        # Convert to list
        mp4_formats = list(unique_formats.values())

        return jsonify(mp4_formats)

    except yt_dlp.DownloadError:
        return jsonify({'error': 'Invalid URL or video not available'}), 400

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_id = request.form.get('format_id')
    download_type = request.form.get('download_type')  # 'video' or 'audio'

    if download_type == 'audio':  # Handle MP3 download
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # Set the MP3 quality to 192 kbps
            }],
            'postprocessor_args': [
                '-ar', '44100',  # Set the audio sample rate to 44.1 kHz (CD quality)
                '-b:a', '192k',  # Set the audio bitrate to 192 kbps (same as used for videos)
            ],
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save as MP3 file
        }
    else:  # Handle MP4 video download
        ydl_opts = {
            'format': f'{format_id}+bestaudio',
            'outtmpl': 'downloads/%(title)s-%(format_id)s.%(ext)s',  # Save with title and format ID
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)  # Get the filename with title

        # Handle MP3 download case
        if download_type == 'audio':
            filename_mp3 = f"{os.path.splitext(filename)[0]}.mp3"  # Ensure we use the correct mp3 file.
            return send_file(filename_mp3, as_attachment=True, download_name=info['title'] + ".mp3", mimetype='audio/mpeg')

        # Handle video downloads (MP4)
        if download_type == 'video' and not filename.endswith('.mp4'):
            filename_mp4 = f"{os.path.splitext(filename)[0]}.mp4"
            os.rename(filename, filename_mp4)
            filename = filename_mp4

        return send_file(filename, as_attachment=True, download_name=info['title'] + ".mp4", mimetype='video/mp4')

    except yt_dlp.DownloadError:
        return "Failed to download video or audio. Invalid format or URL.", 400

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
