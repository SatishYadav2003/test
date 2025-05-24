from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import traceback
from yt_dlp import YoutubeDL

app = FastAPI()

# === INPUT SCHEMA ===
class JobRequest(BaseModel):
    video_url: str
    video_format_id: str
    audio_format_id: str

# === PROCESS FUNCTION (Drive upload removed) ===
def process_job(video_url, video_format_id, audio_format_id):
    try:
        # Format string: audio+video (correct order for merging in yt-dlp)
        format_string = f"{audio_format_id}+{video_format_id}"

        ydl_opts = {
            'outtmpl': '/tmp/%(title).100s.%(ext)s',  # limit length, safe filename
            'format': format_string,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'cookiefile': 'cookies.txt',
            'restrictfilenames': True,  # Restrict filenames to ASCII + safe chars
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # List files after download to find the merged video file
        files = os.listdir('/tmp')
        print("Files in /tmp after download:", files)

        # Look for mp4 file (merged output)
        merged_file = next((f for f in files if f.endswith('.mp4')), None)
        if not merged_file:
            raise Exception("Merged file not found in /tmp")

        local_path = f'/tmp/{merged_file}'

        # Simulated success message instead of Drive upload
        simulated_link = f"Successfully generated: {merged_file}"

        # Cleanup the downloaded file after success
        if os.path.exists(local_path):
            os.remove(local_path)

        return simulated_link

    except Exception as e:
        traceback.print_exc()
        raise

# === FASTAPI ENDPOINT ===
@app.post("/process")
def handle_request(req: JobRequest):
    try:
        result = process_job(req.video_url, req.video_format_id, req.audio_format_id)
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
