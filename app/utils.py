import subprocess
from pathlib import Path

def convert_rtsp_to_hls(rtsp_url: str, output_dir: str):
    """
    Convert RTSP stream to HLS using FFmpeg.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    hls_path = Path(output_dir) / "stream.m3u8"
    command = [
        "ffmpeg", "-i", rtsp_url,
        "-c:v", "libx264", "-preset", "ultrafast",
        "-f", "hls", "-hls_time", "2", "-hls_list_size", "3",
        "-hls_flags", "delete_segments",
        str(hls_path)
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process, hls_path
