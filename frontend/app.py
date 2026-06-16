import gradio as gr
import requests
import time
import os
from frontend.components import header, footer

# Backend internal URL for container communication
API_URL = "http://backend:8000/api"

def upload_and_process(file):
    if file is None:
        return "No file uploaded", None

    files = {"file": open(file.name, "rb")}
    resp = requests.post(f"{API_URL}/upload", files=files)
    if resp.status_code != 200:
        return f"Upload failed: {resp.text}", None

    video_path = resp.json()["video_path"]
    return video_path, f"Uploaded: {os.path.basename(video_path)}"

def download_and_process(url):
    if not url:
        return "No URL provided", None

    resp = requests.post(f"{API_URL}/download", json={"url": url})
    if resp.status_code != 200:
        return f"Download failed: {resp.text}", None

    video_path = resp.json()["video_path"]
    return video_path, f"Downloaded: {os.path.basename(video_path)}"

def run_ai_clip(video_path, language):
    if not video_path:
        return "Please upload or download a video first.", []

    resp = requests.post(f"{API_URL}/ai-clip", json={"video_path": video_path, "language": language})
    if resp.status_code != 200:
        return f"AI Clip failed: {resp.text}", []

    task_id = resp.json()["task_id"]

    while True:
        status_resp = requests.get(f"{API_URL}/status/{task_id}")
        status_data = status_resp.json()
        if status_data["status"] == "completed":
            clips = status_data["result"]
            break
        elif status_data["status"] == "failed":
            return f"AI processing failed: {status_data.get('error')}", []
        time.sleep(2)

    if not clips:
        return "No viral clips detected.", []

    result_text = "Detected Clips:\n"
    gallery_items = []
    for clip in clips:
        result_text += f"- {clip['text']} ({clip['start']:.2f}s - {clip['end']:.2f}s)\n"
        # We pass the local path to Gradio Gallery.
        # Since 'outputs' is mounted in both containers, Gradio can access the file.
        # Gradio will handle serving the file to the mobile browser.
        local_path = os.path.join("outputs", clip['filename'])
        gallery_items.append((local_path, f"{clip['text']} ({clip['start']:.2f}s)"))

    return result_text, gallery_items

with gr.Blocks(title="NEXUS VIDEO AGENT", theme=gr.themes.Soft()) as demo:
    header()

    video_state = gr.State()

    with gr.Tab("Upload & Clip"):
        with gr.Row():
            with gr.Column():
                video_input = gr.File(label="Upload Video", file_types=["video"])
                upload_btn = gr.Button("Upload", variant="primary")
            with gr.Column():
                url_input = gr.Textbox(label="Video URL (YouTube, TikTok, etc.)")
                download_btn = gr.Button("Download", variant="primary")

        status_output = gr.Textbox(label="Status", interactive=False)

        with gr.Row():
            lang_radio = gr.Radio(["en", "zh"], label="Language", value="en")
            ai_clip_btn = gr.Button("🚀 Auto-Detect Viral Clips", variant="secondary")

        with gr.Row():
            transcription_output = gr.Textbox(label="AI Detection Results", lines=10)
            video_gallery = gr.Gallery(label="Generated Clips", show_label=True, columns=2)

    upload_btn.click(upload_and_process, inputs=[video_input], outputs=[video_state, status_output])
    download_btn.click(download_and_process, inputs=[url_input], outputs=[video_state, status_output])
    ai_clip_btn.click(run_ai_clip, inputs=[video_state, lang_radio], outputs=[transcription_output, video_gallery])

    footer()

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
