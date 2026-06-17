# NEXUS VIDEO AGENT 🚀

NEXUS VIDEO AGENT is a web-based AI video clipping service designed for mobile and desktop browsers. It automatically detects "viral" moments in videos and clips them into downloadable MP4 files using Alibaba's FunASR Paraformer model and FFmpeg.

## 🌟 Features

- **Video Upload**: Upload MP4 files directly from your device.
- **URL Download**: Support for YouTube, TikTok, and other platforms via `yt-dlp`.
- **AI-Powered Clipping**: Uses FunASR to transcribe and identify key segments.
- **Mobile-Friendly**: Gradio-based UI optimized for mobile browsers.
- **FastAPI Backend**: Asynchronous and production-ready API.
- **Dockerized**: Easy deployment with Docker and Docker Compose.

## 🛠 Technology Stack

- **Backend**: Python 3.9+, FastAPI, FFmpeg
- **AI**: FunASR (Paraformer model)
- **Downloader**: yt-dlp
- **Frontend**: Gradio
- **Deployment**: Docker, Docker Compose

## 🚀 Quick Start (Docker Compose)

The easiest way to run NEXUS VIDEO AGENT is using Docker Compose.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/nexus-video-agent.git
   cd nexus-video-agent
   ```

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - **Gradio UI**: [http://localhost:7860](http://localhost:7860)
   - **FastAPI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📱 Mobile Access

To access the service from your mobile phone:

1. Ensure your phone and computer are on the same Wi-Fi network.
2. Find your computer's local IP address (e.g., `192.168.1.5`).
3. Open the mobile browser and go to `http://192.168.1.5:7860`.
4. Alternatively, use the Gradio public link generated in the terminal (`share=True`).

## 🔧 Manual Installation

If you prefer to run it locally without Docker:

1. **Install FFmpeg**:
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend**:
   ```bash
   python backend/main.py
   ```

4. **Run the Frontend**:
   ```bash
   python frontend/app.py
   ```

## 🧪 Running Tests

```bash
pytest
```

## 📂 Project Structure

```text
nexus-video-agent/
├── backend/            # FastAPI Backend
├── frontend/           # Gradio Frontend
├── tests/              # Unit & Integration Tests
├── outputs/            # Clipped video segments
├── temp_videos/        # Temporary downloads
├── docker-compose.yml  # Docker setup
└── requirements.txt    # Python dependencies
```

## 📝 License

MIT
