from fileinput import filename
from pytube import exceptions, YouTube
import os
from pathlib import Path
import wx
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import ConvertShorts

#may fix PyInstaller error
try:
    import pkg_resources.py2_warn
except ImportError:
    pass
 
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Program')
 
        #Find or Create Program Files
        self.hubPath = Path().home().joinpath("Documents\ADP")
        self.audioPath = Path().home().joinpath("Documents\ADP\AudioArchive")
        self.videoPath = Path().home().joinpath("Documents\ADP\VideoArchive")
 
        if(not os.path.exists(self.hubPath)):
            print("main path does not exist")
            os.mkdir(self.hubPath)
        if(not os.path.exists(self.audioPath)):
            print("audio path does not exist")
            os.mkdir(self.audioPath)
        if(not os.path.exists(self.videoPath)):
            print("video path does not exist")
            os.mkdir(self.videoPath)
 
        #intialize panel & Sizer
        self.panel = wx.ScrolledWindow(self, -1)
        self.panel.SetScrollbars(1, 1, 600, 400)
        self.panel.SetScrollRate(10,10)
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetBackgroundColour(wx.RED)
 
        # wx element intializations
        self.readText = wx.StaticText(self.panel, label="Program Title")
        self.MainSizer.Add(self.readText, 0, wx.ALL, 5)

        self.backButton = wx.Button(self.panel, label="Back")
        self.backButton.Bind(wx.EVT_BUTTON, self.BackTrigger)
        self.backButton.Show(False)
        self.MainSizer.Add(self.backButton, 0, wx.ALL, 5)
 
        self.text_ctrl = wx.TextCtrl(self.panel)
        self.MainSizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)
 
        self.audioButton = wx.Button(self.panel, label="Download Audio")
        self.audioButton.Bind(wx.EVT_BUTTON, self.DownLoadAudio)
        self.MainSizer.Add(self.audioButton, 0, wx.ALL, 5)

        self.videoButton = wx.Button(self.panel, label="Download Video")
        self.videoButton.Bind(wx.EVT_BUTTON, self.DownLoadVideo)
        self.MainSizer.Add(self.videoButton, 0, wx.ALL, 5)

        resList = ["360p", "720p"]
        self.resOptions = wx.ComboBox(self.panel, choices=resList, style=0, value="360p")
        self.resOptions.Show(False)
        self.MainSizer.Add(self.resOptions, 0, wx.ALL, 5)

        self.qualityButton = wx.Button(self.panel, label="Confirm Quality")
        self.qualityButton.Bind(wx.EVT_BUTTON, self.SelectQuality)
        self.MainSizer.Add(self.qualityButton, 0, wx.ALL, 5)
        self.qualityButton.Show(False)
 
        self.contain = wx.BoxSizer(wx.HORIZONTAL)
        self.MainSizer.Add(self.contain)
        self.contain2 = wx.BoxSizer(wx.HORIZONTAL)
        self.MainSizer.Add(self.contain2)
       
        #Final Setup
        self.panel.SetSizer(self.MainSizer)
        self.RefreshElements()
 
    #Class Functions
    #Refreshes GUI when Back button is clicked back to main screen
    def BackTrigger(self, *args):
        self.readText.Show()
        self.readText.SetLabel("Program Title")
        self.text_ctrl.Show()
        self.audioButton.Show()
        self.videoButton.Show()

        self.resOptions.Show(False)
        self.backButton.Show(False)
        self.qualityButton.Show(False)
        self.text_ctrl.Clear()
        self.RefreshElements()
 
    #Controlling GUI Elements when download audio is clicked
    def DownLoadAudio(self, event):
        self.readText.Show()
        self.readText.SetLabel("Attempting to Download mp3")
        self.text_ctrl.Show(False)
        self.audioButton.Show(False)
        self.videoButton.Show(False)
 
        self.backButton.Show()
        self.ScanURL("audio")
        self.RefreshElements()

    #Controlling GUI Elements when download video is clicked
    def DownLoadVideo(self, event):
        self.readText.Show()
        self.readText.SetLabel("Select Video Quality")
        self.resOptions.Show()
        self.audioButton.Show(False)
        self.videoButton.Show(False)
 
        self.qualityButton.Show()
        self.backButton.Show()
        self.RefreshElements()
    
        #Controlling GUI Elements when download video is clicked
    def SelectQuality(self, event):
        self.readText.Show()
        self.readText.SetLabel("Attempting to Download mp4")
        self.text_ctrl.Show(False)
        self.audioButton.Show(False)
        self.videoButton.Show(False)
        self.qualityButton.Show(False)
        self.resOptions.Show(False)
 
        self.backButton.Show()
        self.ScanURL("video")
        self.RefreshElements()

    #Function to scan the url and decide what to do with the url
    def ScanURL(self, whichButton):
        formData = ConvertShorts.convert_shorts(self.text_ctrl.GetValue())
        #see if the url is valid
        validate = URLValidator()
        try:
            validate(formData)
            print("Valid URL")
            #see if youtube url will work or not
            try:
                yt = YouTube(formData)
                print(yt.title)
                self.readText.SetLabel("Video Found")
                #if user clicks the audio button
                if(whichButton == "audio"):
                    print("audio file")
                    self.readText.SetLabel("Sucessfully Downloaded Audio File")
                    #streams the audio video
                    file = yt.streams.filter(only_audio = True)
                    stream = yt.streams.get_by_itag(140)
                    #changes file type from mp4 to mp3
                    out_file = stream.download(output_path=str(self.audioPath))
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                #if user clicks the video button
                elif(whichButton == "video"):
                    print("video file")
                    qualityData = self.resOptions.GetValue()
                    self.readText.SetLabel("Sucessfully Downloaded Video File")
                    #downloads the video file
                    file = yt.streams.filter(file_extension='mp4')
                    if(qualityData == "360p"):
                        stream = yt.streams.get_by_itag(18)
                    elif(qualityData == "720p"):
                        stream = yt.streams.get_by_itag(22)
                    else:
                        stream = yt.streams.get_by_itag(18)
                    stream.download(output_path=str(self.videoPath), filename_prefix = qualityData +"_")
            #exception handler for pytube
            except exceptions.PytubeError:
                print("Not a valid Youtube link")
                
                self.BackTrigger()
                self.readText.SetLabel("Submission is not valid Youtube Video")
                self.text_ctrl.Clear()
        #exception handler for invalid url entry
        except ValidationError as e:
            print("Not a URL")
            self.readText.SetLabel("Submission is not valid URL")
            self.text_ctrl.Clear()
 
    #Refreshes GUI Elements
    def RefreshElements(self):
        self.MainSizer.Fit(self)
        self.SetSize(500,400)
        self.MainSizer.Layout()
        #self.text_ctrl.Clear()
        self.Show()

#Runs Script
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()