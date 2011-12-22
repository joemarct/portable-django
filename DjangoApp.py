#!/usr/bin/env python 

import wx
import signal, psutil
import os, sys, webbrowser
import shlex, subprocess
import django

os.chdir('MyProject')

class Frame(wx.Frame):

    def __init__(self, parent, id, title, **kwargs):
        wx.Frame.__init__(self, parent, id, title, **kwargs)
        panel = wx.Panel(self)
        panel.SetBackgroundColour('White')
        self.textarea = wx.TextCtrl(self, -1,style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2, size=(460,200))
 

        toolbar = self.CreateToolBar()
        tool_run = toolbar.AddSimpleTool(wx.NewId(), wx.Image('../gui_images/run.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Run Server', 'Run Server')
        tool_stop = toolbar.AddSimpleTool(wx.NewId(), wx.Image('../gui_images/stop.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Stop Server', 'Stop Server')
        tool_browse = toolbar.AddSimpleTool(wx.NewId(), wx.Image('../gui_images/open_browser.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Open in Browser', 'Open in Browser')
        toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.OnRun, tool_run)
        self.Bind(wx.EVT_TOOL, self.OnStop, tool_stop)
        self.Bind(wx.EVT_TOOL, self.OnBrowse, tool_browse)


        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        run = menu1.Append(wx.NewId(), '&Run', 'Run server')
        stop = menu1.Append(wx.NewId(), '&Stop', 'Stop server')
        menu1.AppendSeparator()
        close = menu1.Append(wx.ID_EXIT, 'E&xit', 'Close program')
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, close) 
        self.Bind(wx.EVT_MENU, self.OnRun, run)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        menuBar.Append(menu1, '&Server')        
        self.SetMenuBar(menuBar)

        self.ServerStatus('Down')
    
    def ServerStatus(self, status):
        self.server_status = status

    def RecordPid(self, pid):
        self.server_pid = pid

    def OnRun(self, event):
        if self.server_status == 'Down':
            command = '%s manage.py runserver' % sys.executable
            args = shlex.split(command)
            server = subprocess.Popen(args)
            self.RecordPid(server.pid)
            self.textarea.write('The development server is running at http://127.0.0.1:8000/\n')
            self.ServerStatus('Up')
        elif self.server_status == 'Up':
            self.textarea.write('The development server is already running\n')

    def ShutdownServer(self):
        if self.server_status == 'Up':
            parent = psutil.Process(self.server_pid)
            for child in parent.get_children():
                child.kill()
            parent.kill()
            self.textarea.write('The development server has been stopped.\n\n')
            self.ServerStatus('Down')
        else:
            pass
                  
    def OnStop(self, event):
        self.ShutdownServer()

    def OnBrowse(self, event):
        webbrowser.open('http://localhost:8000/', new=1)
                                        

    def OnCloseWindow(self,event):
        self.ShutdownServer()
        self.Destroy()


class App(wx.App):
    
    def OnInit(self):
        frame = Frame(None, -1, 'DjangoApp', size=(450,200))
        frame.Show()
        frame.Center()
        self.SetTopWindow(frame)
        return True


if __name__ == '__main__':
    app = App(False)
    app.MainLoop()
