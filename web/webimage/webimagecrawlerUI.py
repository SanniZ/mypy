#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on: 2019-01-02

@author: Zbyng Zeng
"""
import os

from tkinter import Tk, Frame, StringVar,\
                    Menu, Label, Entry, Button, Listbox, Checkbutton, Scrollbar,\
                    X, Y, TOP, LEFT, RIGHT, NORMAL, DISABLED, HORIZONTAL, BOTH
from tkinter.filedialog import askopenfilename #askdirectory
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, showwarning

import threading
from queue import Queue

from web.webbase import WebBase
from web.webimage.webimagecrawler import URL_BASE
from web.webimage.girlsky import Girlsky
from web.webimage.pstatp import Pstatp
from web.webimage.meizitu import Meizitu
from web.webimage.mzitu import Mzitu
from web.webimage.webimage import WebImage

STAT_WAITTING = 'Waitting'
STAT_DOWNLOADING = 'Downloading'
STAT_DONE = 'Done'
STAT_FAIL = 'Failed'

ABOUT = '''
    WebImage Crawler 1.0

    Auther@Zbyng.Zeng

    Copyright(c)Zbyng.Zeng
'''


############################################################################
#               FileInfo Class
############################################################################

class FileInfo(object):
    def __init__(self):
        self._url = None
        self._state = STAT_WAITTING
        self._output = ''
        self._args = None


############################################################################
#               WindowUI Class
############################################################################

class WindowUI(object):

    def __init__(self):
        self._wm = dict()
        # create UI
        top = Tk()
        self._wm['top'] = top
        top.title('WebImageCrawler')
        top.geometry('800x640')

        top.resizable(0, 0)
        self.create_menu(top)

    def run(self):
        root = self._wm['top']
        # create frames for main window.
        self.create_main_window_frames(root)
        # create path widgets.
        self.create_path_widgets()

        self.create_type_widgets()
        # create header of file list.
        self.create_header_widgets()
        # create file list widghts
        self.create_file_list_widgets()

        root.mainloop()

    def menu_file_open(self):
        print('run menu_file_open')

    def menu_file_exit(self):
        self._wm['top'].quit()

    def menu_help_about(self):
        print('run menu_help_about')

    def create_menu(self, root):
        menubar = Menu(root)

        menu_file = Menu(menubar, tearoff = 0)
        menu_file.add_command(label = 'Open', command=self.menu_file_open)
        #menu_file.add_separator()
        menu_file.add_command(label = 'Exit', command=self.menu_file_exit)

        menu_help = Menu(menubar, tearoff = 0)
        menu_help.add_command(label = 'About', command=self.menu_help_about)

        menubar.add_cascade(label = 'File', menu = menu_file)
        menubar.add_cascade(label = 'Help', menu = menu_help)
        root['menu'] = menubar
        self._wm['menu_file'] = menu_file
        self._wm['menu_help'] = menu_help

    def create_main_window_frames(self, root):
        Args = Frame(root)
        Args.pack(side = TOP, fill = X)
        Args = Listbox(Args, bg = 'LightGrey')
        Args.pack(side = TOP, expand = 1, fill = X, padx = 1, pady = 1)

        Path = Frame(Args)
        Path.pack(side = TOP, expand = 1, fill = X)

        Type = Frame(Args)
        Type.pack(side = TOP, expand = 1, fill = X, pady = 2)

        FsInfo = Frame(root)
        FsInfo.pack(side = TOP, expand = 1, fill = BOTH)
        FsInfo = Listbox(FsInfo, bg = 'LightGrey')
        FsInfo.pack(side = TOP, expand = 1, fill = BOTH, padx = 1, pady = 1)

        Hdr = Frame(FsInfo)
        Hdr.pack(side = TOP, fill = X)

        Fs = Frame(FsInfo)
        Fs.pack(side = TOP, expand = 1, fill = BOTH, padx = 4, pady = 4)

        FsList = Frame(Fs)
        FsList.pack(side = LEFT, expand = 1, fill = BOTH)
        SbY = Frame(Fs)
        SbY.pack(side = RIGHT, fill=Y)

        SbX = Frame(FsInfo)
        SbX.pack(side = TOP, fill = X)

        self._wm['frmPath'] = Path
        self._wm['frmType'] = Type
        self._wm['frmHdr'] = Hdr
        self._wm['frmFs'] = Fs
        self._wm['frmFsList'] = FsList
        self._wm['frmSbX'] = SbX
        self._wm['frmSbY'] = SbY

    def on_run_click(self):
        print('run on_run_click')

    def create_path_widgets(self):
        frm = self._wm['frmPath']
        lbPath = Label(frm, text = 'Path:')
        lbPath.pack(side = LEFT)
        self._path_var = StringVar()
        enPath = Entry(frm, textvariable = self._path_var)
        enPath.pack(side = LEFT, expand=1, fill=X)
        bnPath = Button(frm, text = 'Run', command = self.on_run_click)
        bnPath.pack(side = RIGHT, padx = 4, pady = 2)

        self._wm['lbPath'] = lbPath
        self._wm['enPath'] = enPath
        self._wm['bnPath'] = bnPath

    def on_chk_type_click(self):
        print('run on_bn_type_click')

    def on_bn_type_click(self):
        print('run on_chk_type_click')

    def create_type_widgets(self):
        frm = self._wm['frmType']
        self._type_chk = StringVar()
        chkType = Checkbutton(frm, text = '', onvalue = 1, offvalue = 0, state = NORMAL,
                              variable = self._type_chk, command = self.on_chk_type_click)
        self._type_chk.set(0)
        chkType.pack(side = LEFT, padx = 8)
        lbType = Label(frm, text = 'Type:')
        lbType.pack(side = LEFT)
        self._type_var = StringVar()
        cmbType = ttk.Combobox(frm, width = 8, textvariable = self._type_var)
        cmbType.pack(side = LEFT, padx = 4)
        cmbType['value'] = ('xgmn', 'swmn', 'wgmn', 'zpmn', 'mnxz', 'rtys', 'jpmn', 'gzmn', 'nrtys', 'meizitu', 'mzitu')
        lbStart = Label(frm, text = 'Start:')
        lbStart.pack(side = LEFT, padx = 4)
        self._type_start = StringVar()
        enStart = Entry(frm, width = 8, textvariable = self._type_start)
        enStart.pack(side = LEFT)
        lbEnd = Label(frm, text = 'End:')
        lbEnd.pack(side = LEFT, padx = 4)
        self._type_end = StringVar()
        enEnd = Entry(frm, width = 8, textvariable = self._type_end)
        enEnd.pack(side = LEFT)
        bnType = Button(frm, text = 'OK', width = 4, command = self.on_bn_type_click)
        bnType.pack(side = LEFT, padx = 36)

        cmbType['state'] = DISABLED
        enStart['state'] = DISABLED
        enEnd['state'] = DISABLED
        bnType['state'] = DISABLED

        self._wm['chkType'] = chkType
        self._wm['cmbType'] = cmbType
        self._wm['enStart'] = enStart
        self._wm['enEnd'] = enEnd
        self._wm['bnType'] = bnType

    def create_header_widgets(self):
        frm = self._wm['frmHdr']
        self.lbFsURL = Label(frm, text = 'URL', width = 32)
        self.lbFsState = Label(frm, text = 'State', width = 8)
        self.lbFsOutput = Label(frm, text = 'Output', width = 32)
        #self.chkFsSelAll.pack(side = LEFT, expand =1, fill = X)
        self.lbFsURL.pack(side = LEFT, expand =1, fill=X)
        self.lbFsState.pack(side = LEFT, expand =1, fill=X)
        self.lbFsOutput.pack(side = LEFT, expand =1, fill=X)


    def create_file_list_widgets(self):
        frmFsList = self._wm['frmFsList']
        self._lbfs_var = StringVar()
        lbFs = Listbox(frmFsList, listvariable = self._lbfs_var)
        lbFs.pack(side = LEFT, expand = 1, fill = BOTH)
        frmSbY = self._wm['frmSbY']
        sbY = Scrollbar(frmSbY)
        sbY.pack(side = TOP, expand = 1, fill=Y)
        frmSbX = self._wm['frmSbX']
        sbX = Scrollbar(frmSbX, orient = HORIZONTAL)
        sbX.pack(side = TOP, expand = 1, fill=X)

        lbFs['yscrollcommand'] = sbY.set
        sbY['command'] = lbFs.yview
        lbFs['xscrollcommand'] = sbX.set
        sbX['command'] = lbFs.xview

        self._wm['lbFs'] = lbFs
        self._wm['sbY'] = sbY
        self._wm['sbX'] = sbX


############################################################################
#               WebImageCrawlerUI Class
############################################################################

class WebImageCrawlerUI(WindowUI):

    def __init__(self, name=None):
        super().__init__()
        self._name = name

        self._fs_list = None
        self._fs_list_cnt = 0
        self._fs_list_lock = threading.Lock()

        self._class = None
        self._download_thread_max = 5
        self._download_thread_queue = Queue(self._download_thread_max)
        self._download_threads = None


    def menu_file_open(self):
        f = askopenfilename()
        self._path_var.set(f)
        if f:
            self.update_url_list()
            self.update_list_info()

    def menu_help_about(self):
        showinfo('About', ABOUT)

    def on_chk_type_click(self):
        self.update_type_widget_state(self._type_chk.get())

    def on_bn_type_click(self):
        t_type  = self._type_var.get()
        t_start = self._type_start.get()
        t_end   = self._type_end.get()
        if all((t_type, t_start)):
            url_start = int(t_start)
            if t_end:
                url_end = int(t_end)
                if url_end > url_start:
                    n = url_end - url_start + 1
                else:
                    showerror('Error', 'Start(%d) > End(%d)!' % (url_start, url_end))
                    return
            else:
                n = 1
            # config args
            args = {'-x': t_type, '-u' : t_start, '-n' : n}
            self._path_var.set(args)

            # update file list and info.
            self.update_url_list()
            self.update_list_info()
        else:
            showerror('Error', '\ntype/start is invalid.')

    def on_run_click(self):
        fp = self._wm['enPath'].get()
        if fp:
            # # update file list and info
            self.update_url_list()
            self.update_list_info()
            self.update_widget_state(0)

            self.download_url_list()
        else:
            showwarning('Warning', '\nNot set path!')

    def update_type_widget_state(self, state):
        if int(state):
            self._wm['cmbType']['state'] = NORMAL
            self._wm['enStart']['state'] = NORMAL
            self._wm['enEnd']['state'] = NORMAL
            self._wm['bnType']['state'] = NORMAL
        else:
            self._wm['cmbType']['state'] = DISABLED
            self._wm['enStart']['state'] = DISABLED
            self._wm['enEnd']['state'] = DISABLED
            self._wm['bnType']['state'] = DISABLED

    def update_menu_state(self, state):
        if int(state):
            self._wm['menu_file'].entryconfigure('Open', state = NORMAL)
        else:
            self._wm['menu_file'].entryconfigure('Open', state = DISABLED)

    def update_widget_state(self, state):
        # update state of menu
        self.update_menu_state(state)
        # update state of widgets.
        if int(state):
            self._wm['chkType']['state'] = NORMAL
            self._wm['bnPath']['state'] = NORMAL
            self._wm['enPath']['state'] = NORMAL
            self.update_type_widget_state(self._type_chk.get())
        else:
            self._wm['chkType']['state'] = DISABLED
            self._wm['bnPath']['state'] = DISABLED
            self._wm['enPath']['state'] = DISABLED
            self.update_type_widget_state(0)


    def add_url_info_to_list(self, url, state = None, output = None):
        info = FileInfo()
        info._url = url
        if state:
            info._state = state
        if output:
            info._output = output
        self._fs_list.append(info)
        self._fs_list_cnt += 1

    def update_list_info(self, url = None, state = None, output = None):
        with self._fs_list_lock:
            fs = list()
            for i, info in enumerate(self._fs_list):
                if url == info._url:
                    if state:
                        info._state = state
                    if output:
                        info._output = output
                #print(info._url, info._state, info._output)
                fs.append('%s%s%s' % (info._url.ljust(64), info._state.ljust(16), info._output.ljust(64)))
            self._lbfs_var.set(tuple(fs))

    def update_url_list(self):
        # clear file list
        self._fs_list_cnt = 0
        self._fs_list = list()
        # get file
        f = self._wm['enPath'].get()
        if os.path.isfile(f):
            with open(f, 'r') as fd:
                urls = fd.readlines()
        elif '-x' in f:
            args = eval(f)
            url_start = int(args['-u'])
            n = args['-n']
            url_type = args['-x']
            urls = list()
            for index in range(n):
                if url_type in URL_BASE:
                    url_base = list(URL_BASE[url_type])[0]
                    url = url_base.replace('URLID', str(url_start + index))
                    urls.append(url)
        else:
            urls = [f]
        # add file info to list.
        for url in set(urls):
            url = WebBase.reclaim_url_address(url)
            if url:
                self.add_url_info_to_list(url)
        # sort of file list.
        self._fs_list.sort(key = lambda info: info._url, reverse=False)

    def download_url(self, args=None):
        url = args['-u']
        if self._class:
            if self._class == 'girlsky':
                hdr = Girlsky('Girlsky')
            elif self._class == 'pstatp':
                hdr = Pstatp('Pstatp')
            elif self._class == 'meizitu':
                hdr = Meizitu('Meizitu')
            elif self._class == 'mzitu':
                hdr = Mzitu('Mzitu')
        else:
            hdr = WebImage('WebImage')
        if hdr:
            self.update_list_info(url, STAT_DOWNLOADING)
            output = hdr.main(args)
            # update state to DONE.
            if output:
                self.update_list_info(url, STAT_DONE, output)
            else:
                self.update_list_info(url, STAT_FAIL)
        else:
            self._pr.pr_err('Error, no found handler!')
            self.update_list_info(url, STAT_FAIL)

        # release thread.
        self._download_thread_queue.get()

    def crawler_download_url(self):
        if self._fs_list_cnt:
            index = 0
            self._download_threads = list()
            # create thread to download url.
            while self._fs_list_cnt:
                self._class = None
                info = self._fs_list[index]
                index += 1
                self._fs_list_cnt -= 1
                url = WebBase.reclaim_url_address(info._url)
                base, num = WebBase.get_url_base_and_num(url)
                if base:
                    for dict_url_base in URL_BASE.values():
                        if base == list(dict_url_base)[0]:
                            self._class =  dict_url_base[base]
                            break
                if self._class:
                    url = {'-u' : url}
                    # create thread and put to queue.
                    t = threading.Thread(target = self.download_url, args = (url,))
                    self._download_thread_queue.put(url)
                    self._download_threads.append(t)
                    t.start()
            for t in self._download_threads:
                t.join()
            self.update_widget_state(1)
            #print('All of url are done!')

    def download_url_list(self):
        self.update_url_list()
        self.update_list_info()
        threading.Thread(target = self.crawler_download_url).start()


    def main(self):
        self.run()


############################################################################
#               main entrance
############################################################################

if __name__ == '__main__':
    ui = WebImageCrawlerUI()
    ui.main()