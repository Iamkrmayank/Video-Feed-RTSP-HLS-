from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.utils import convert_rtsp_to_hls
from pathlib import Path

app = FastAPI(
    title="Drone Video Feed API",
    description="A FastAPI backend to convert RTSP to HLS for browser compatibility.",
    version="1.0.0"
)

# Static files directory for HLS streaming
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.post("/convert", summary="Convert RTSP to HLS")
async def convert_stream(rtsp_url: str, background_tasks: BackgroundTasks):
    """
    Accept an RTSP URL and start the conversion to HLS.
    """
    if not rtsp_url.startswith("rtsp://"):
        raise HTTPException(status_code=400, detail="Invalid RTSP URL format.")

    output_dir = "app/static/hls"
    process, hls_path = convert_rtsp_to_hls(rtsp_url, output_dir)
    
    # Run FFmpeg in the background
    background_tasks.add_task(process.wait)

    return {"hls_url": f"/static/hls/stream.m3u8"}

@app.get("/stream", summary="Get HLS Stream")
async def get_stream():
    """
    Provide the HLS stream file.
    """
    hls_path = Path("app/static/hls/stream.m3u8")
    if not hls_path.exists():
        raise HTTPException(status_code=404, detail="HLS stream not found.")

    return FileResponse(hls_path)
