import pytest
from backend.video_downloader import download_video
import os

@pytest.mark.asyncio
async def test_download_invalid_url():
    with pytest.raises(Exception):
        await download_video("https://invalid-url-nexus.com")

# Mocking or using a small public video for actual test if needed
