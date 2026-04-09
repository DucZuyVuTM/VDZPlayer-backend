import yt_dlp


def get_video_info(url: str):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "source": info.get('extractor_key'),
                "videoUrl": info.get('url'),
                "thumbnail": info.get('thumbnail'),
                "title": info.get('title'),
            }
        except Exception as e:
            print(f"Error: {e}")
            return None
