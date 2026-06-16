import pytest
from backend.video_processor import VideoProcessor
import os

@pytest.mark.asyncio
async def test_transcribe_non_existent_file():
    processor = VideoProcessor()
    with pytest.raises(Exception):
        await processor.transcribe("non_existent_video.mp4")

@pytest.mark.asyncio
async def test_clip_video_ffmpeg_error():
    processor = VideoProcessor()
    # Providing a file that is not a video should trigger ffmpeg error if it tries to read it
    with open("dummy.txt", "w") as f:
        f.write("not a video")

    with pytest.raises(Exception):
        await processor.clip_video("dummy.txt", 0, 10)

    if os.path.exists("dummy.txt"):
        os.remove("dummy.txt")
