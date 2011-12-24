#!/usr/bin/env python 

import wx
import signal, psutil
import os, sys, webbrowser
import shlex, subprocess
import django, time


os.chdir('MyProject')

class Editor(wx.Frame):
    
    def __init__(self, parent, id, title, file, **kwargs):
        wx.Frame.__init__(self, parent, id, title, **kwargs)
        panel = wx.Panel(self, size=(600,400))
        panel.SetBackgroundColour('White')
        self.textarea = wx.TextCtrl(self, -1,style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_RICH2)
        frameSizer = wx.GridSizer(rows=1, cols=1)
        frameSizer.Add(panel,1,wx.EXPAND)
        self.SetSizer(frameSizer) 
        self.Fit()
        self.CreateStatusBar()
        self.SetStatusText("Edit this file")

        self.file = file
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self.textarea,1,wx.EXPAND)
        panel.SetSizer(panelSizer)
        panel.Fit()

        self.toolbar = self.CreateToolBar(wx.TB_TEXT)
        self.tool_save = self.toolbar.AddLabelTool(wx.NewId(), 'Save', wx.Image('../icons/save.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.toolbar.EnableTool(self.tool_save.GetId(), False)
        self.toolbar.Realize()
        self.toolbar.SetToolBitmapSize(size=(32,32))
        self.Bind(wx.EVT_TOOL, self.OnSave, self.tool_save)

        file_content = open(file,'r')
        for line in file_content.readlines():
            self.textarea.write(line)

        self.Bind(wx.EVT_TEXT, self.OnModify)

        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        self.save = menu1.Append(wx.NewId(), '&Save\tCtrl-S', 'Save')
        menuBar.Append(menu1, '&File')        
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnSave, self.save)

    def OnModify(self, event):
        self.toolbar.EnableTool(self.tool_save.GetId(), True)
        self.SetStatusText('File modified')

    def SaveFile(self):
        out = open(self.file,'w')
        out.write(self.textarea.GetValue())
        out.close()
        self.SetStatusText("File saved")
            
    def OnSave(self, event):
        self.SaveFile()
        self.toolbar.EnableTool(self.tool_save.GetId(), False)


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
        
        self.toolbar = self.CreateToolBar(wx.TB_TEXT)
        self.tool_run = self.toolbar.AddLabelTool(wx.NewId(), 'Run', wx.Image('../icons/run.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.tool_stop = self.toolbar.AddLabelTool(wx.NewId(), 'Stop', wx.Image('../icons/stop.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.tool_browse = self.toolbar.AddLabelTool(wx.NewId(), 'Browse', wx.Image('../icons/open_browser.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.tool_create = self.toolbar.AddLabelTool(wx.NewId(), 'Create App', wx.Image('../icons/create_app.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.tool_sync = self.toolbar.AddLabelTool(wx.NewId(), 'Sync DB', wx.Image('../icons/sync_db.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.tool_edit = self.toolbar.AddLabelTool(wx.NewId(), 'Edit', wx.Image('../icons/edit_files.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.toolbar.Realize()
        self.toolbar.SetToolBitmapSize(size=(32,32))
        
        self.toolbar.EnableTool(self.tool_stop.GetId(), False)
        self.toolbar.EnableTool(self.tool_browse.GetId(), False)

        self.Bind(wx.EVT_TOOL, self.OnRun, self.tool_run)
        self.Bind(wx.EVT_TOOL, self.OnStop, self.tool_stop)
        self.Bind(wx.EVT_TOOL, self.OnBrowse, self.tool_browse)
        self.Bind(wx.EVT_TOOL, self.OnCreate, self.tool_create)
        self.Bind(wx.EVT_TOOL, self.OnSync, self.tool_sync)
        self.Bind(wx.EVT_TOOL, self.OnEdit, self.tool_edit)

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
       
        self.textarea.write('''\nThe Browse button will take you to the admin login page.\nUsername: admin, password: admin\n''')

        self.toolbar.EnableTool(self.tool_stop.GetId(), True)
        self.toolbar.EnableTool(self.tool_browse.GetId(), True)


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
        self.toolbar.EnableTool(self.tool_stop.GetId(), False)
        self.toolbar.EnableTool(self.tool_browse.GetId(), False)

    def OnBrowse(self, event):
        time.sleep(1)
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

    def OnEdit(self, event):
        file_types = "Python files (*.py)|*.py|HTML template files (*.html)|*.html|CSS files (*.css)|*.css" 
        dialog = wx.FileDialog(None, message='Choose a file to edit', defaultDir=os.getcwd(), wildcard=file_types)
        if dialog.ShowModal() == wx.ID_OK:
            file = dialog.GetPath()
            editor = Editor(None, -1, 'DjangoApp - Editor', file, size=(600,400))
            editor.Show()

                                        
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
