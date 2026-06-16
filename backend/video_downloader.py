import yt_dlp
import os
import uuid
import asyncio
from backend.config import TEMP_DIR

async def download_video(url: str) -> str:
    """
    Downloads a video from a given URL using yt-dlp.
    Returns the path to the downloaded file.
    """
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    file_id = str(uuid.uuid4())
    outtmpl = os.path.join(TEMP_DIR, f"{file_id}.%(ext)s")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': outtmpl,
        'quiet': True,
        'no_warnings': True,
    }

    def _download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)

    loop = asyncio.get_event_loop()
    try:
        file_path = await loop.run_in_executor(None, _download)
        return file_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        raise e
