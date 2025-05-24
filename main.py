from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import traceback
import gspread
from yt_dlp import YoutubeDL
from oauth2client.service_account import ServiceAccountCredentials




app = FastAPI()



# === INPUT SCHEMA ===
class JobRequest(BaseModel):
    video_url: str
    video_format_id: str
    audio_format_id: str

# === PROCESS FUNCTION (Drive upload removed) ===
def process_job(video_url, video_format_id, audio_format_id):
    try:
        format_string = f"{audio_format_id}+{video_format_id}"
        ydl_opts = {
            'outtmpl': '/tmp/%(title)s.%(ext)s',
            'format': format_string,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'cookiefile': 'cookies.txt'
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        files = os.listdir('/tmp')
        merged_file = next((f for f in files if f.endswith(('.mp4', '.webm', '.mkv'))), None)
        if not merged_file:
            raise Exception("Merged file not found")

        local_path = f'/tmp/{merged_file}'

        # Simulated success message instead of Drive upload
        simulated_link = f"Successfully generated: {merged_file}"

     

        os.remove(local_path)
        return simulated_link

    except Exception as e:
        traceback.print_exc()

        raise

# === FASTAPI ENDPOINT ===
@app.post("/process")
def handle_request(req: JobRequest):
    try:
        link = process_job(req.video_url, req.video_format_id, req.audio_format_id)
        return {"status": "success", "message": link}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
