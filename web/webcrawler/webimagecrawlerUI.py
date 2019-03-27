#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2019-01-02

@author: Byng Zeng
"""

import os
import re
import sys
import subprocess
import threading

from collections import OrderedDict

from web.weburl import \
    get_url_base_and_num, set_url_base_and_num, reclaim_url_address
from web.webcrawler.webimagecrawler import XBaseClass

if sys.version_info[0] == 2:
    import ttk
    from Queue import Queue
    from tkFileDialog import askopenfilename, askdirectory
    from tkMessageBox import \
        showinfo, showerror, showwarning, askyesno
    from Tkinter import \
        Tk, Frame, StringVar, IntVar, \
        Menu, Label, Entry, Button, Listbox, Checkbutton, Scrollbar, \
        X, Y, TOP, LEFT, RIGHT, NORMAL, DISABLED, HORIZONTAL, BOTH
else:
    # from tkinter.simpledialog import askstring
    from queue import Queue
    from tkinter.filedialog import askopenfilename, askdirectory
    from tkinter.messagebox import \
        showinfo, showerror, showwarning, askyesno
    from tkinter import \
        Tk, ttk, Frame, StringVar, IntVar, \
        Menu, Label, Entry, Button, Listbox, Checkbutton, Scrollbar, \
        X, Y, TOP, LEFT, RIGHT, NORMAL, DISABLED, HORIZONTAL, BOTH


############################################################################
#               Const Vars
############################################################################

VERSION = '1.4.0'
AUTHOR = 'Byng.Zeng'

STAT_WAITTING = 'Waitting'
STAT_DOWNLOADING = 'Downloading'
STAT_DONE = 'Done'
STAT_FAIL = 'Failed'
STAT_NOT_SUPPORT = 'Not Support'

LANG_MAP = (
    {'About': 'About',
     'AboutVersion':
         'Web Image Crawler %s\n\nAuther@%s\n\nCopyright(c)%s\n' % (VERSION,
                                                                    AUTHOR,
                                                                    AUTHOR),
     'Config': 'Config', 'Cancel': 'Cancel', 'Copy': 'Copy', 'Clear': 'Clear',
     'Debug': 'Debug', 'Delete': 'Delete',
     'End': 'End', 'Error': 'Error', 'Exit': 'Exit', 'File': 'File',
     'Help': 'Help', 'InvalidType': 'Type/Start is invalid',
     'InvalidURL': 'URL is invalid', 'Lang': 'Language', 'Notice': 'Notice',
     'NoOutput': '\nNo Output', 'Open': 'Open', 'Output': 'Output',
     'Paste': 'Paste',
     'Run': 'Run', 'Start': 'Start', 'State': 'State',
     'Title': 'WebImageCrawler', 'Type': 'Type',
     'TypeList': ('meitulu', 'meizitu', 'mzitu', 'xgmn', 'swmn', 'wgmn',
                  'zpmn', 'mnxz', 'rtys', 'jpmn', 'gzmn', 'nrtys',),
     'OK': 'OK', 'URL': 'URL',  'Warnning': 'Warnning', },
    {'About': '关于',
     'AboutVersion':
         '网页图片爬虫 %s\n\n作者@%s\n\n版权所有(c)%s\n' % (
                                                 VERSION, AUTHOR, AUTHOR),
     'Config': '配置', 'Cancel': '取消', 'Copy': '复制', 'Clear': '清除',
     'Debug': '调试', 'Delete': '删除', 'End': '结束', 'Exit': '退出',
     'Error': '错误', 'File': '文件', 'Help': '帮助',
     'InvalidType': '分类/开始值无效',
     'InvalidURL': '地址值无效', 'Lang': '语言', 'Notice': '提示',
     'NoOutput': '\n没有输出文件', 'Open': '打开', 'Output': '输出',
     'Paste': '粘贴',
     'Run': '运行', 'Start': '开始', 'State': '状态', 'Title': '网页图片爬虫',
     'Type': '分类',
     'TypeList': ('美图录', '妺子图', '妺子图Mz', '性感美女', '丝袜美女',
                  '外国美女', '自拍美女', '美女写真', '人体艺术', '街拍美女',
                  '古装美女', '人体艺术n',),
     'OK': '确定', 'URL': '地址', 'Warnning': '警告', },
)


############################################################################
#               WindowUI Class
############################################################################

class WindowUI(object):

    __slots__ = ('_wm', '_lang', '_view', '_debug', '_output', '_lang_set',
                 '_debug_v_set', '_debug_d_set', '_debug_D_set', '_path_var',
                 '_type_chk', '_type_var', '_type_start', '_type_end',
                 '_lbfs_var')

    def __init__(self):
        self._wm = dict()
        self._lang = 1
        self._view = 0
        self._debug = 0
        self._output = ''
        # create UI
        top = Tk()
        self._wm['top'] = top
        top.title('%s' % LANG_MAP[self._lang]['Title'])
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
        pass

    def menu_file_clear(self):
        pass

    def menu_file_exit(self):
        self._wm['top'].quit()

    def menu_config_lang(self):
        self._lang = self._lang_set.get()
        # update title and menu.
        self._wm['top'].title('%s' % LANG_MAP[self._lang]['Title'])
        self.create_menu(self._wm['top'])
        # update lang of widgets.
        self._wm['lbPath']['text'] = '%s:' % LANG_MAP[self._lang]['URL']
        self._wm['bnPath']['text'] = LANG_MAP[self._lang]['Run']
        self._wm['lbType']['text'] = '%s:' % LANG_MAP[self._lang]['Type']
        self._wm['lbStart']['text'] = '%s:' % LANG_MAP[self._lang]['Start']
        self._wm['lbEnd']['text'] = '%s:' % LANG_MAP[self._lang]['End']
        self._wm['bnType']['text'] = LANG_MAP[self._lang]['OK']
        self._wm['lbURL']['text'] = LANG_MAP[self._lang]['URL']
        self._wm['lbState']['text'] = LANG_MAP[self._lang]['State']
        self._wm['lbOutput']['text'] = LANG_MAP[self._lang]['Output']
        # update type list.
        self._wm['cmbType']['value'] = LANG_MAP[self._lang]['TypeList']

    def menu_config_output(self):
        output = askdirectory()
        if output:
            self._output = output
        else:
            res = askyesno('%s' % LANG_MAP[self._lang]['Delete'],
                           '%s' % self._output if self._output else 'None')
            if res:
                self._output = ''
        self.create_menu(self._wm['top'])

    def menu_config_debug(self):
        self._view = self._debug_v_set.get()
        dm = self._debug_D_set.get()
        dv = self._debug_d_set.get()
        if dv != self._debug:
            if not dm:
                self._debug_D_set.set(1)
            self._debug = dv
        else:
            if dm:
                if not self._debug:
                    self._debug_d_set.set(1)
            else:
                self._debug_d_set.set(0)
            self._debug = self._debug_d_set.get()

    def menu_help_about(self):
        pass

    def create_menu(self, root):
        # create menu bar.
        menubar = Menu(root)

        # create file menu and add commands
        menu_file = Menu(menubar, tearoff=0)
        menu_open = menu_file.add_command(
                        command=self.menu_file_open,
                        label='%s' % LANG_MAP[self._lang]['Open'].center(10))
        menu_clear = menu_file.add_command(
                        command=self.menu_file_clear,
                        label='%s' % LANG_MAP[self._lang]['Clear'].center(10))
        menu_file.add_separator()
        menu_exit = menu_file.add_command(
                        command=self.menu_file_exit,
                        label='%s' % LANG_MAP[self._lang]['Exit'].center(10))

        # create config menu and add commands
        menu_config = Menu(menubar, tearoff=0)
        # create language nemu and add cascade
        menu_lang = Menu(menu_config, tearoff=0)
        self._lang_set = IntVar()
        menu_lang.add_radiobutton(
                label='English', command=self.menu_config_lang,
                variable=self._lang_set, value=0)
        menu_lang.add_radiobutton(
                label='中文', command=self.menu_config_lang,
                variable=self._lang_set, value=1)
        self._lang_set.set(self._lang)
        mbar_lang = menu_config.add_cascade(
                            menu=menu_lang,
                            label='%s' % LANG_MAP[self._lang]['Lang'])
        # create output menu
        menu_output = Menu(menu_config, tearoff=0)
        menu_output.add_command(
                command=self.menu_config_output,
                label='%s' % self._output if self._output else 'None')
        mbar_output = menu_config.add_cascade(
                            menu=menu_output,
                            label='%s' % LANG_MAP[self._lang]['Output'])
        # create configuration menu and add cascade
        menu_debug = Menu(menu_config, tearoff=0)
        self._debug_v_set = IntVar()
        self._debug_d_set = IntVar()
        self._debug_D_set = IntVar()
        menu_debug.add_checkbutton(
                        label='-v View', onvalue=1,
                        variable=self._debug_v_set,
                        command=self.menu_config_debug)
        menu_debug.add_checkbutton(
                        label='-d Debug', onvalue=1,
                        variable=self._debug_D_set,
                        command=self.menu_config_debug)
        menu_debug.add_radiobutton(
                        label='d1 Debug Basic', value=0x01,
                        variable=self._debug_d_set,
                        command=self.menu_config_debug)
        menu_debug.add_radiobutton(
                        label='d2 Debug Advance', value=0x02,
                        variable=self._debug_d_set,
                        command=self.menu_config_debug)
        mbar_debug = menu_config.add_cascade(
                                menu=menu_debug,
                                label='%s' % LANG_MAP[self._lang]['Debug'])
        # create help menu
        menu_help = Menu(menubar, tearoff=0)
        menu_about = menu_help.add_command(
                            command=self.menu_help_about,
                            label='%s' % LANG_MAP[self._lang]['About'])

        # add cascade to menu bar.
        mbar_file = menubar.add_cascade(
                                menu=menu_file,
                                label='%s' % LANG_MAP[self._lang]['File'])
        mbar_config = menubar.add_cascade(
                                menu=menu_config,
                                label='%s' % LANG_MAP[self._lang]['Config'])
        mbar_help = menubar.add_cascade(
                                menu=menu_help,
                                label='%s' % LANG_MAP[self._lang]['Help'])

        root['menu'] = menubar
        self._wm['mbar_file'] = mbar_file
        self._wm['mbar_config'] = mbar_config
        self._wm['mbar_help'] = mbar_help
        self._wm['menu_file'] = menu_file
        self._wm['menu_help'] = menu_help
        self._wm['mbar_lang'] = mbar_lang
        self._wm['mbar_output'] = mbar_output
        self._wm['mbar_debug'] = mbar_debug
        self._wm['menu_open'] = menu_open
        self._wm['menu_clear'] = menu_clear
        self._wm['menu_exit'] = menu_exit
        self._wm['menu_output'] = menu_output
        self._wm['menu_about'] = menu_about

    def create_main_window_frames(self, root):
        Args = Frame(root)
        Args.pack(side=TOP, fill=X)
        Args = Listbox(Args, bg='LightGrey')
        Args.pack(side=TOP, expand=1, fill=X, padx=1, pady=1)

        Path = Frame(Args)
        Path.pack(side=TOP, expand=1, fill=X)

        Type = Frame(Args)
        Type.pack(side=TOP, expand=1, fill=X, pady=2)

        FsInfo = Frame(root)
        FsInfo.pack(side=TOP, expand=1, fill=BOTH)
        FsInfo = Listbox(FsInfo, bg='LightGrey')
        FsInfo.pack(side=TOP, expand=1, fill=BOTH, padx=1, pady=1)

        Hdr = Frame(FsInfo)
        Hdr.pack(side=TOP, fill=X)

        Fs = Frame(FsInfo)
        Fs.pack(side=TOP, expand=1, fill=BOTH, padx=4, pady=4)

        FsList = Frame(Fs)
        FsList.pack(side=LEFT, expand=1, fill=BOTH)
        SbY = Frame(Fs)
        SbY.pack(side=RIGHT, fill=Y)

        SbX = Frame(FsInfo)
        SbX.pack(side=TOP, fill=X)

        self._wm['frmPath'] = Path
        self._wm['frmType'] = Type
        self._wm['frmHdr'] = Hdr
        self._wm['frmFs'] = Fs
        self._wm['frmFsList'] = FsList
        self._wm['frmSbX'] = SbX
        self._wm['frmSbY'] = SbY

    def on_popmenu_path_copy(self):
        pass

    def on_popmenu_path_paste(self):
        pass

    def on_popmenu_path_leave(self, event):
        path_popmenu = self._wm['path_popmenu']
        path_popmenu.unpost()

    def create_path_popmenu(self):
        path_popmenu = Menu(self._wm['top'], tearoff=0)
        path_popmenu.add_command(command=self.on_popmenu_path_copy,
                                 label='%s' % LANG_MAP[self._lang]['Copy'])
        path_popmenu.add_command(command=self.on_popmenu_path_paste,
                                 label='%s' % LANG_MAP[self._lang]['Paste'])
        # bind leave event
        path_popmenu.bind("<Leave>", self.on_popmenu_path_leave)

        self._wm['path_popmenu'] = path_popmenu

    def pop_path_menu(self, event):
        path_popmenu = self._wm['path_popmenu']
        path_popmenu.post(event.x_root, event.y_root)

    def on_run_click(self):
        pass

    def create_path_widgets(self):
        frm = self._wm['frmPath']
        lbPath = Label(frm, text='%s:' % LANG_MAP[self._lang]['URL'])
        lbPath.pack(side=LEFT)
        self._path_var = StringVar()
        enPath = Entry(frm, textvariable=self._path_var)
        enPath.pack(side=LEFT, expand=1, fill=X)
        bnPath = Button(frm, text='%s' % LANG_MAP[self._lang]['Run'],
                        command=self.on_run_click)
        bnPath.pack(side=RIGHT, padx=4, pady=2)

        # self.create_path_popmenu()
        # enPath.bind("<Button-3>", self.pop_path_menu)

        self._wm['lbPath'] = lbPath
        self._wm['enPath'] = enPath
        self._wm['bnPath'] = bnPath

    def on_chk_type_click(self):
        pass

    def on_bn_type_click(self):
        pass

    def create_type_widgets(self):
        frm = self._wm['frmType']
        self._type_chk = StringVar()
        chkType = Checkbutton(frm, text='', onvalue=1, offvalue=0,
                              state=NORMAL, variable=self._type_chk,
                              command=self.on_chk_type_click)
        self._type_chk.set(0)
        chkType.pack(side=LEFT, padx=8)
        lbType = Label(frm, text='%s' % LANG_MAP[self._lang]['Type'])
        lbType.pack(side=LEFT)
        self._type_var = StringVar()
        cmbType = ttk.Combobox(frm, width=8, textvariable=self._type_var)
        cmbType.pack(side=LEFT, padx=4)
        cmbType['value'] = LANG_MAP[self._lang]['TypeList']
        lbStart = Label(frm, text='%s:' % LANG_MAP[self._lang]['Start'])
        lbStart.pack(side=LEFT, padx=4)
        self._type_start = StringVar()
        enStart = Entry(frm, width=8, textvariable=self._type_start)
        enStart.pack(side=LEFT)
        lbEnd = Label(frm, text='%s:' % LANG_MAP[self._lang]['End'])
        lbEnd.pack(side=LEFT, padx=4)
        self._type_end = StringVar()
        enEnd = Entry(frm, width=8, textvariable=self._type_end)
        enEnd.pack(side=LEFT)
        bnType = Button(frm, text='%s' % LANG_MAP[self._lang]['OK'],
                        width=4, command=self.on_bn_type_click)
        bnType.pack(side=LEFT, padx=36)

        cmbType['state'] = DISABLED
        enStart['state'] = DISABLED
        enEnd['state'] = DISABLED
        bnType['state'] = DISABLED

        self._wm['chkType'] = chkType
        self._wm['lbType'] = lbType
        self._wm['lbStart'] = lbStart
        self._wm['lbEnd'] = lbEnd
        self._wm['cmbType'] = cmbType
        self._wm['enStart'] = enStart
        self._wm['enEnd'] = enEnd
        self._wm['bnType'] = bnType

    def create_header_widgets(self):
        frm = self._wm['frmHdr']
        lbURL = Label(frm, text='%s' % LANG_MAP[self._lang]['URL'],
                      width=32)
        lbState = Label(frm, text='%s' % LANG_MAP[self._lang]['State'],
                        width=8)
        lbOutput = Label(frm, text='%s' % LANG_MAP[self._lang]['Output'],
                         width=32)
        # self.chkFsSelAll.pack(side=LEFT, expand=1, fill=X)
        lbURL.pack(side=LEFT, expand=1, fill=X)
        lbState.pack(side=LEFT, expand=1, fill=X)
        lbOutput.pack(side=LEFT, expand=1, fill=X)

        self._wm['lbURL'] = lbURL
        self._wm['lbState'] = lbState
        self._wm['lbOutput'] = lbOutput

    def on_popmenu_fs_open(self):
        pass

    def on_popmenu_fs_leave(self, event):
        fs_popmenu = self._wm['fs_popmenu']
        fs_popmenu.unpost()

    def create_file_list_popmenu(self):
        fs_popmenu = Menu(self._wm['top'], tearoff=0)
        fs_popmenu.add_command(command=self.on_popmenu_fs_open,
                               label='%s' % LANG_MAP[self._lang]['Open'])
        # bind leave event
        fs_popmenu.bind("<Leave>", self.on_popmenu_fs_leave)

        self._wm['fs_popmenu'] = fs_popmenu

    def pop_fs_menu(self, event):
        fs_popmenu = self._wm['fs_popmenu']
        fs_popmenu.post(event.x_root, event.y_root)

    def create_file_list_widgets(self):
        frmFsList = self._wm['frmFsList']
        self._lbfs_var = StringVar()
        lbFs = Listbox(frmFsList, listvariable=self._lbfs_var)
        lbFs.pack(side=LEFT, expand=1, fill=BOTH)
        frmSbY = self._wm['frmSbY']
        sbY = Scrollbar(frmSbY)
        sbY.pack(side=TOP, expand=1, fill=Y)
        frmSbX = self._wm['frmSbX']
        sbX = Scrollbar(frmSbX, orient=HORIZONTAL)
        sbX.pack(side=TOP, expand=1, fill=X)

        lbFs['yscrollcommand'] = sbY.set
        sbY['command'] = lbFs.yview
        lbFs['xscrollcommand'] = sbX.set
        sbX['command'] = lbFs.xview

        self.create_file_list_popmenu()
        lbFs.bind("<Button-3>", self.pop_fs_menu)

        self._wm['lbFs'] = lbFs
        self._wm['sbY'] = sbY
        self._wm['sbX'] = sbX

############################################################################
#               WebImageCrawlerUI Class
############################################################################


class WebImageCrawlerUI(WindowUI):

    __slots__ = ('_name', '_fs_list', '_fs_list_lock', '_class',
                 '_search_urls', '_download_thread_max',
                 '_download_thread_queue', '_download_threads')

    def __init__(self, name=None):
        super(WebImageCrawlerUI, self).__init__()
        self._name = name

        self._fs_list = OrderedDict()
        self._fs_list_lock = threading.Lock()

        self._class = None
        self._search_urls = list()
        self._download_thread_max = 5
        self._download_thread_queue = Queue(self._download_thread_max)
        self._download_threads = None

    def menu_file_open(self):
        f = askopenfilename()
        self._path_var.set(f)
        if f:
            self.update_url_list()
            self.update_list_info()

    def menu_file_clear(self):
        self._fs_list = OrderedDict()
        self.update_list_info()
        self._path_var.set('')

    def menu_help_about(self):
        showinfo(LANG_MAP[self._lang]['About'],
                 LANG_MAP[self._lang]['AboutVersion'])

    def menu_config_lang(self):
        super(WebImageCrawlerUI, self).menu_config_lang()
        self._debug_v_set.set(self._view)
        self._debug_D_set.set(self._debug)
        self._debug_d_set.set(self._debug)

    def on_chk_type_click(self):
        self.update_type_widget_state(self._type_chk.get())

    def on_bn_type_click(self):
        t_type = self._type_var.get()
        t_start = self._type_start.get()
        t_end = self._type_end.get()
        if all((t_type, t_start)):
            if t_type in ['meitulu', '美图录']:
                url = 'https://www.meitulu.com/t/%s' % t_start
                args = {'-u': url, '-n': 1}
            else:
                try:
                    url_start = int(t_start)
                    if t_end:
                        url_end = int(t_end)
                        if url_end >= url_start:
                            n = url_end - url_start + 1
                        else:
                            showerror(
                                '%s' % LANG_MAP[self._lang]['Error'],
                                '%s(%d) > %s(%d)!' % (
                                    LANG_MAP[self._lang]['Start'], url_start,
                                    LANG_MAP[self._lang]['End'], url_end))
                            return
                    else:
                        n = 1
                except ValueError as e:
                    showerror('%s' % LANG_MAP[self._lang]['Error'],
                              '\n%s!' % str(e))
                    return
                # config args
                if self._lang:
                    if type(t_type) != str:
                        t_type = t_type.encode('utf-8')
                    index = LANG_MAP[self._lang]['TypeList'].index(t_type)
                    t_type = LANG_MAP[0]['TypeList'][index]
                args = {'-x': t_type, '-u': t_start, '-n': n}

            # uppdate fs info.
            self._path_var.set(args)
            self.update_url_list()
            self.update_list_info()
        else:
            showerror('%s' % LANG_MAP[self._lang]['Error'],
                      '\n%s!' % LANG_MAP[self._lang]['InvalidType'])

    def on_run_click(self):
        fpath = self._wm['enPath'].get()
        if fpath:
            if not re.compile('{.*}').match(fpath):
                args = {'-u': fpath}
                if self._output:
                    args['-p'] = self._output
            else:
                args = eval(fpath)
            #    if self._output:
            #        args['-p'] = self._output
            #    elif '-p' in args:
            #        del args['-p']
            self._path_var.set(args)
            # # update file list and info
            self.update_url_list()
            self.update_list_info()
            self.update_widget_state(0)

            self.download_url_list()
        else:
            showwarning('%s' % LANG_MAP[self._lang]['Error'],
                        '\n%s!' % LANG_MAP[self._lang]['InvalidURL'])

    def on_popmenu_fs_open(self):
        output = None
        fs = self._wm['lbFs']
        index = fs.curselection()
        if not index:
            return
        data = fs.get(index)
        data = re.compile('http.+Done\s+(.+)').findall(data)
        if data:
            output = data[0].strip()
        if output:
            for k, w in {' ': '\ ', ':': '\:'}.items():
                output = re.sub(k, w, output)
            cmd = 'nautilus %s' % output
            subprocess.check_output(cmd, shell=True)
        else:
            showinfo(LANG_MAP[self._lang]['Notice'],
                     LANG_MAP[self._lang]['NoOutput'])

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
        menu_file = self._wm['menu_file']
        if int(state):
            menu_file.entryconfigure(
                '%s' % LANG_MAP[self._lang]['Open'].center(10), state=NORMAL)
            menu_file.entryconfigure(
                '%s' % LANG_MAP[self._lang]['Clear'].center(10), state=NORMAL)
        else:
            menu_file.entryconfigure(
              '%s' % LANG_MAP[self._lang]['Open'].center(10), state=DISABLED)
            menu_file.entryconfigure(
              '%s' % LANG_MAP[self._lang]['Clear'].center(10), state=DISABLED)

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

    def add_url_info_to_list(self, url, state=None, output=None):
        if not state:
            state = STAT_WAITTING
        if not output:
            output = ''
        self._fs_list[url] = [state, output]

    def update_list_info(self, url=None, state=None, output=None):
        # update fs list
        if url in self._fs_list.keys():
            if state:
                self._fs_list[url][0] = state
            if output:
                self._fs_list[url][1] = output
        # update fs to show.
        with self._fs_list_lock:
            fs = list()
            for key, info in self._fs_list.items():
                fs.append('%s%s%s' % (
                    key.ljust(64), info[0].ljust(16), info[1]))
            # update fs list
            # fs.sort(key=lambda f: f)  # it will match crawler_download_url().
            self._lbfs_var.set(tuple(fs))

    def update_url_list(self, urls=None):
        # clear file list
        self._fs_list = OrderedDict()
        # get file
        if not urls:
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
                    url = XBaseClass.get_num_url_from_xval(
                                        url_type, str(url_start + index))
                    if url:
                        urls.append(url)
            elif '-u' in f:
                args = eval(f)
                if os.path.isfile(args['-u']):
                    with open(args['-u'], 'r') as fd:
                        urls = fd.readlines()
                else:
                    if '-n' in args:
                        n = args['-n']
                        if type(n) is not int:
                            n = int(n)
                    else:
                        n = 1
                    urls = list()
                    for index in range(n):
                        base, num = get_url_base_and_num(args['-u'])
                        if all((base, num)):
                            try:
                                num = int(num)
                            except ValueError:
                                url = args['-u']
                            else:
                                url = set_url_base_and_num(base, num + index)
                        else:
                            url = args['-u']
                        if url:
                            urls.append(url)
            else:
                urls = [f]
        # add file info to list.
        for url in sorted(set(urls)):
            url = reclaim_url_address(url)
            if url:
                self.add_url_info_to_list(url)

    def download_url(self, args=None):
        url = args['-u']
        base, num = get_url_base_and_num(url)
        if base:
            self._class = XBaseClass.get_class_from_base(base)
        else:
            self._class = XBaseClass.get_class_from_url(url)
        hdr = XBaseClass.get_class_instance(self._class)
        if hdr:
            self.update_list_info(url, STAT_DOWNLOADING)
            output = hdr.main(args)
            if output:
                try:
                    if 'search_urls' in output[url]:
                        self._search_urls += output[url]['search_urls']
                        output[url] = ''
                except TypeError:
                    pass
            # update state to DONE.
            if output:
                self.update_list_info(url, STAT_DONE, output[url])
            else:
                self.update_list_info(url, STAT_FAIL)
        else:
            self._pr.pr_err('Error, no found handler!')
            self.update_list_info(url, STAT_FAIL)

        # release thread.
        self._download_thread_queue.get()

    def crawler_download_url(self):
        if len(self._fs_list):
            self._download_threads = list()
            # create thread to download url.
            for url in self._fs_list.keys():  # sorted(self._fs_list.keys()):
                self._class = None
                # set url and start thread to download url.
                args = {'-u': url}
                if self._view:
                    args['-v'] = True
                if self._debug:
                    args['-d'] = self._debug
                if self._output:
                    args['-p'] = self._output
                # create thread and put to queue.
                t = threading.Thread(target=self.download_url, args=(args,))
                self._download_thread_queue.put(args)
                self._download_threads.append(t)
                t.start()
            # waitting for thread.
            for t in self._download_threads:
                t.join()
            self.update_widget_state(1)
            # process search urls.
            if self._search_urls:
                self.update_url_list(self._search_urls)
                self.update_list_info()
                self.update_widget_state(0)
                self.download_url_list()
                self._search_urls = list()
            # print('All of url are done!')

    def download_url_list(self):
        threading.Thread(target=self.crawler_download_url).start()

    def main(self, args=None):
        self.run()


############################################################################
#               main entrance
############################################################################

if __name__ == '__main__':
    ui = WebImageCrawlerUI()
    ui.main()
