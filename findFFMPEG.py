import re
from pathlib import Path

def Find_ffmpeg_Path():
    ffmpegPath = ""

    for path in Path.home().rglob('*ffmpeg.exe'):
        if(re.search(r'bin\\ffmpeg.exe', str(path))):
            ffmpegPath = path

    print(ffmpegPath)
    return ffmpegPath