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
        panel = wx.Panel(self, size=(450,200))
        panel.SetBackgroundColour('White')
        self.textarea = wx.TextCtrl(self, -1,style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2)
        frameSizer = wx.GridSizer(rows=1, cols=1)
        frameSizer.Add(panel,1,wx.EXPAND)
        self.SetSizer(frameSizer) 
        self.Fit()
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self.textarea,1,wx.EXPAND)
        panel.SetSizer(panelSizer)
        panel.Fit()

        self.textarea.write('''You are now ready to play with Django.\nClick the Run button to start the server.\n''')
        self.textarea.write('''\nThe Browse button will take you to the admin login page.\nUsername: admin, password: admin\n''')

        toolbar = self.CreateToolBar()
        tool_run = toolbar.AddSimpleTool(wx.NewId(), wx.Image('../gui_images/run.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Run', 'Run')
        tool_stop = toolbar.AddSimpleTool(wx.NewId(), wx.Image('../gui_images/stop.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Stop', 'Stop')
        tool_browse = toolbar.AddSimpleTool(wx.NewId(), wx.Image('../gui_images/open_browser.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Browse', 'Browse')
        tool_create = toolbar.AddSimpleTool(wx.NewId(), wx.Image('../gui_images/create_app.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Create an App', 'Create an App')
        tool_sync = toolbar.AddSimpleTool(wx.NewId(), wx.Image('../gui_images/sync_db.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Sync DB', 'Sync DB')
        toolbar.Realize()
        toolbar.SetToolBitmapSize(size=(32,32))
        self.Bind(wx.EVT_TOOL, self.OnRun, tool_run)
        self.Bind(wx.EVT_TOOL, self.OnStop, tool_stop)
        self.Bind(wx.EVT_TOOL, self.OnBrowse, tool_browse)
        self.Bind(wx.EVT_TOOL, self.OnCreate, tool_create)
        self.Bind(wx.EVT_TOOL, self.OnSync, tool_sync)

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
            self.textarea.write('\nThe development server is running at http://127.0.0.1:8000/')
            self.ServerStatus('Up')
        elif self.server_status == 'Up':
            self.textarea.write('\nThe development server is already running')

    def ShutdownServer(self):
        if self.server_status == 'Up':
            parent = psutil.Process(self.server_pid)
            for child in parent.get_children():
                child.kill()
            parent.kill()
            self.textarea.write('\nThe development server has been stopped.')
            self.ServerStatus('Down')
        else:
            pass
                  
    def OnStop(self, event):
        self.ShutdownServer()

    def OnBrowse(self, event):
        webbrowser.open('http://localhost:8000/admin/', new=1)

    def OnCreate(self, event):
        dialog = wx.TextEntryDialog(None,'Name of app:','Create an App','')
        if dialog.ShowModal() == wx.ID_OK:
            response = dialog.GetValue()

        command = '%s manage.py startapp %s' % (sys.executable, str(response))
        args = shlex.split(command)
        create_app = subprocess.Popen(args, stderr=subprocess.PIPE)
        error = create_app.stderr.read().split('\n')[0].split(';1m')[-1]
        if error:
            self.textarea.write('\n'+error)
        else:
            self.textarea.write('\nThe app named %s has been created' % response)
        
    def OnSync(self, event):
        command = '%s manage.py syncdb' % sys.executable
        args = shlex.split(command)
        syncdb = subprocess.Popen(args, stdout=subprocess.PIPE)
        self.textarea.write('\n'+syncdb.stdout.read())
                                        
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
