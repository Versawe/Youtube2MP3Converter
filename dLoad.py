import youtube_dl
from pathlib import Path
import findFFMPEG

class Example():
    def __init__(self) -> None:
        self.outPutPath = Path.home()
        self.ffmpegPath = str(findFFMPEG.Find_ffmpeg_Path())
        self.outPutPath = self.outPutPath.joinpath(self.outPutPath, "Extractions")
        self.outPutPath1 = self.outPutPath.joinpath(self.outPutPath, "Videos")
        self.outPutPath2 = self.outPutPath.joinpath(self.outPutPath, "Audio")


        if not Path.exists(self.outPutPath):
            self.outPutPath.mkdir(parents=True, exist_ok=True)
            self.outPutPath1.mkdir(parents=True, exist_ok=True)
            self.outPutPath2.mkdir(parents=True, exist_ok=True)

        user_input = input("-a for audio\n-v for video\nFollowed by URL\n")
        self.Check_Input(user_input)

    def Check_Input(self, input):
        print(input[:2])
        if(input[:2] == "-a"):
            print(input[3:len(input)])
            try:
                self.Download_Audio(input[3:len(input)])
            except Exception as e:
                print(str(e))
                pass
        elif(input[:2] == "-v"):
            print(input[3:len(input)])
            try:
                self.Download_Video(input[3:len(input)])
            except Exception as e:
                print(str(e))
                pass

    def Download_Audio(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'outtmpl': str(self.outPutPath2) + "\\%(title)s.%(ext)s",
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'ffmpeg_location': self.ffmpegPath
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])

    def Download_Video(self, url):
        ydl_opts = {
            'format': 'bestvideo/best',
            'outtmpl': str(self.outPutPath1) + "\\%(title)s.%(ext)s",
            'noplaylist': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])

if __name__ == "__main__":
    Example()