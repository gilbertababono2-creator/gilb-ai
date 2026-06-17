import os
import ffmpeg
import asyncio
import uuid
from typing import List, Dict

# Models for different languages
MODELS = {
    "zh": {
        "model": "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
        "model_revision": "v2.0.4",
        "vad_model": "iic/speech_fsmn-vad_ts-16k-common-pytorch",
        "vad_model_revision": "v1.2.0",
        "punc_model": "iic/punc_ct-punc-zh-cn-common-vocab272727-pytorch",
        "punc_model_revision": "v1.0.1",
    },
    "en": {
        "model": "iic/speech_paraformer-large-vad-punc_asr_nat-en-16k-common-vocab10020-pytorch",
        "model_revision": "v2.0.4",
        "vad_model": "iic/speech_fsmn-vad_ts-16k-common-pytorch",
        "vad_model_revision": "v1.2.0",
        "punc_model": "iic/punc_ct-punc-en-mini-common-vocab10020-pytorch",
        "punc_model_revision": "v1.0.1",
    }
}

# Mock model for testing
class MockModel:
    def generate(self, input, **kwargs):
        if not os.path.exists(input):
            raise FileNotFoundError(f"File {input} not found")
        return [{
            'text': 'This is a mock transcription.',
            'sentence_info': [
                {'start': 0, 'end': 2000, 'text': 'First viral moment.'},
                {'start': 3000, 'end': 5000, 'text': 'Second viral moment.'}
            ]
        }]

class VideoProcessor:
    def __init__(self):
        self.models = {}
        if os.getenv("TESTING") == "True":
            self.models["en"] = MockModel()
            self.models["zh"] = MockModel()
        else:
            from funasr import AutoModel
            print("Pre-loading English model...")
            self.models["en"] = AutoModel(**MODELS["en"])
            print("Models loaded.")

    async def get_model(self, language: str):
        if language not in self.models:
            if os.getenv("TESTING") == "True":
                self.models[language] = MockModel()
            else:
                from funasr import AutoModel
                print(f"Loading {language} model...")
                self.models[language] = AutoModel(**MODELS.get(language, MODELS["en"]))
        return self.models[language]

    async def transcribe(self, video_path: str, language: str = 'en'):
        model = await self.get_model(language)
        loop = asyncio.get_event_loop()
        def _inference():
            return model.generate(input=video_path, batch_size_s=300)
        res = await loop.run_in_executor(None, _inference)
        return res

    async def clip_video(self, video_path: str, start_time: float, end_time: float, output_name: str = None):
        if not output_name:
            output_name = f"clip_{uuid.uuid4()}.mp4"
        output_path = os.path.join(os.getenv("OUTPUT_DIR", "outputs"), output_name)
        try:
            stream = ffmpeg.input(video_path, ss=start_time, t=end_time - start_time)
            stream = ffmpeg.output(stream, output_path, c='copy')
            await loop_run_ffmpeg(stream)
            return output_path
        except Exception as e:
            print(f"FFmpeg error: {e}")
            raise e

    async def auto_ai_clip(self, video_path: str, language: str = 'en'):
        transcription = await self.transcribe(video_path, language)
        clips = []
        if transcription and len(transcription) > 0:
            data = transcription[0]
            if 'sentence_info' in data:
                for i, segment in enumerate(data['sentence_info'][:5]):
                    start = segment['start'] / 1000.0
                    end = segment['end'] / 1000.0
                    text = segment['text']
                    output_name = f"ai_clip_{i}_{uuid.uuid4()}.mp4"
                    clip_path = await self.clip_video(video_path, start, end, output_name)
                    clips.append({
                        "id": i, "start": start, "end": end, "text": text,
                        "path": clip_path, "filename": output_name
                    })
        return clips

async def loop_run_ffmpeg(stream):
    loop = asyncio.get_event_loop()
    def _run():
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
    await loop.run_in_executor(None, _run)

video_processor = VideoProcessor()
