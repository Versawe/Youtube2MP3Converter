import os
from pathlib import Path
from moviepy.editor import *
import wx
import urllib as url
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import pafy
import youtube_dl
from playsound import playsound # for playing audio
import multiprocessing # for stopping audio
import time # for pausing audio
 
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Program')
 
        #Declare Vars
        self.fileCount = 0
        self.eleNum = 1
        self.audioPathList = []
        self.valid_tags = ['iframe', 'video', 'source'] # maybe not need
 
        #Find or Create Program Files
        self.hubPath = Path().home().joinpath("Documents\ADP")
        self.audioPath = Path().home().joinpath("Documents\ADP\AudioArchive")
        self.videoPath = Path().home().joinpath("Documents\ADP\VideoTempStorage")
 
        if(not os.path.isdir(self.hubPath)):
            print("path does not exist")
            os.mkdir(self.hubPath)
            os.mkdir(self.audioPath)
            os.mkdir(self.videoPath)
 
        #intialize panel & Sizer
        #self.panel = wx.Panel(self)
        self.panel = wx.ScrolledWindow(self, -1)
        self.panel.SetScrollbars(1, 1, 600, 400)
        self.panel.SetScrollRate(10,10)
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetBackgroundColour(wx.RED)
 
        self.backButton = wx.Button(self.panel, label="Back")
        self.backButton.Bind(wx.EVT_BUTTON, self.BackTrigger)
        self.backButton.Show(False)
        self.MainSizer.Add(self.backButton, 0, wx.ALL, 5)
 
        # wx element intializations
        self.readText = wx.StaticText(self.panel, label="Program Title")
        self.MainSizer.Add(self.readText, 0, wx.ALL, 5)
 
        self.text_ctrl = wx.TextCtrl(self.panel)
        self.MainSizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)
       
        self.urlGrabButton = wx.Button(self.panel, label="Download")
        self.urlGrabButton.Bind(wx.EVT_BUTTON, self.ScanURL)
        self.MainSizer.Add(self.urlGrabButton, 0, wx.ALL, 5)
 
        self.list = wx.ListBox(self.panel, -1, (0,100), wx.Size(200,100), self.audioPathList, style=1)
        self.list.Bind(wx.EVT_LISTBOX, self.get_selected_clip, self.list)
        self.list.Show(False)
        self.MainSizer.Add(self.list, 1, wx.ALL | wx.ALIGN_LEFT, 5)
 
        self.libraryButton = wx.Button(self.panel, label="Show Library")
        self.libraryButton.Bind(wx.EVT_BUTTON, self.SwitchUIElements)
        self.MainSizer.Add(self.libraryButton, 0, wx.ALL, 5)
 
        self.contain = wx.BoxSizer(wx.HORIZONTAL)
        self.MainSizer.Add(self.contain)
        self.contain2 = wx.BoxSizer(wx.HORIZONTAL)
        self.MainSizer.Add(self.contain2)
 
        # play hud wx elements
        self.playButton = wx.Button(self.panel, name = 'play', label='Play', size=(55,20))
        self.contain.Add(self.playButton, 0, wx.ALL | wx.CENTER, 5)
        self.playButton.Bind(wx.EVT_BUTTON, self.ButtonName)
        self.pauseButton = wx.Button(self.panel, name = 'pause', label='Pause', size=(55,20))
        self.contain.Add(self.pauseButton, 0, wx.ALL | wx.CENTER, 5)
        self.pauseButton.Bind(wx.EVT_BUTTON, self.ButtonName)
        self.stopButton = wx.Button(self.panel, name = 'stop', label='Stop', size=(55,20))
        self.contain.Add(self.stopButton, 0, wx.ALL | wx.CENTER, 5)
        self.stopButton.Bind(wx.EVT_BUTTON, self.ButtonName)
        self.autoPlayButton = wx.Button(self.panel, name = 'autoplay', label='AutoPlay', size=(55,20))
        self.contain2.Add(self.autoPlayButton, 0, wx.ALL | wx.CENTER, 5)
        self.autoPlayButton.Bind(wx.EVT_BUTTON, self.ButtonName)
        self.shuffleButton = wx.Button(self.panel, name = 'shuffle', label='Shuffle', size=(55,20))
        self.contain2.Add(self.shuffleButton, 0, wx.ALL | wx.CENTER, 5)
        self.shuffleButton.Bind(wx.EVT_BUTTON, self.ButtonName)
        self.playButton.Show(False)
        self.pauseButton.Show(False)
        self.stopButton.Show(False)
        self.shuffleButton.Show(False)
        self.autoPlayButton.Show(False)
       
        #Final Setup
        self.panel.SetSizer(self.MainSizer)
        self.RefreshElements()
 
    #Class Functions
    def BackTrigger(self, event):
        self.readText.Show()
        self.text_ctrl.Show()
        self.urlGrabButton.Show()
        self.libraryButton.Show()
 
        self.backButton.Show(False)
        self.list.Show(False)
        self.playButton.Show(False)
        self.pauseButton.Show(False)
        self.stopButton.Show(False)
        self.autoPlayButton.Show(False)
        self.shuffleButton.Show(False)
        self.RefreshElements()
 
    def SwitchUIElements(self, event):
        self.readText.Show(False)
        self.text_ctrl.Show(False)
        self.urlGrabButton.Show(False)
        self.libraryButton.Show(False)
 
        self.backButton.Show()
        self.list.Show()
        self.playButton.Show()
        self.pauseButton.Show()
        self.stopButton.Show()
        self.autoPlayButton.Show()
        self.shuffleButton.Show()
        self.RefreshElements()
 
    def get_selected_clip(self):
        selectedClip = self.list.GetSelection()
        print(selectedClip)
 
    #Read clip files in program folder
    def ReadClips(self):
        for e in os.listdir(self.audioPath):
            self.audioPathList.append(e)
 
    def ButtonName(self, event): # example test
        print(event.GetEventObject().GetName())
 
    def ScanURL(self, event):
        formData = self.text_ctrl.GetValue()
        validate = URLValidator()
        try:
            validate(formData)
            #print("Valid URL")
        except ValidationError as e:
            #print("Not a URL")
            self.text_ctrl.Clear()
 
    def RefreshElements(self):
        self.MainSizer.Fit(self)
        self.SetSize(500,400)
        self.MainSizer.Layout()
        self.Show()
 
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()