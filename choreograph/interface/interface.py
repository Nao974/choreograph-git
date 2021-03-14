from interface.frame_skeleton import *
from interface.frame_interactive import *
from interface.frame_movement import *
# from interface.frame_tracker import *
from interface.frame_controller import *
from wintools.win_tools import *
from common.lang_EN import *
from common.lang_FR import *
from servomboxe.mboxe_dummy import *
import common.constants as g

from os import path
import json
from collections import OrderedDict
from tkinter import *
from PIL import Image, ImageTk  # pip install pillow

class Interface:
    def __init__(self, version, lang):
        self.version = version
        self.frame_set = 0
        self.lang = lang
        self.bye = 'N'

        self.filepath_view = ''
        self.filepath_skeleton = ''
        self.filepath_position = ''
        self.filepath_movement = ''
        self.filepath_controller = ''

        self.windows = Tk()
        #self.windows.geometry("450x450")
        self.windows.title('DIRP- Choregraph v%s' % self.version)
        # self.windows.iconbitmap(...)
        #self.windows.resizable(0, 0)

        g.check_motor = IntVar()
        g.update_engine = IntVar()
        g.connect_controller = IntVar()
        g.bind_key = IntVar()
        g.catch_exception = IntVar()
        g.check_motor.set(1)  # 1 pour cochée // 0 pour décochée
        g.update_engine.set(1)
        g.connect_controller.set(1)
        g.bind_key.set(0)
        g.catch_exception.set(0)

        g.current_path = os.getcwd()

        self.tab_interactive = Frame_Interactive(self)
        # self.windows.bind('<Key>', self.keyPressed)

        self.toolwindow = win_tools(self)

        self.add_frames()
        self.add_toolbar()

        print("\n---------------------------")
        print("Choregraph    v%s" % self.version)
        print("---------------------------")
        print("Mboxe %s v%s" % (self.lang['library'], Mboxe(-1).return_vlib()))
        print("---------------------------")
        print("%s: %s-%s" % (self.lang['System'], g.system[0], g.system[1]) )
        print("---------------------------")
        print("%s\n" % g.current_path)


    def add_frames(self):
        if self.frame_set == 0:
            self.tab_master = ttk.Notebook(self.windows)

            self.tab_skeleton = Frame_Skeleton(self)
            self.tab_master.add(self.tab_skeleton, text=self.lang['Skeleton'])
            self.tab_interactive = Frame_Interactive(self)
            self.tab_master.add(self.tab_interactive, text=self.lang['Interactive'])
            self.tab_movement = Frame_Movement(self)
            self.tab_master.add(self.tab_movement, text=self.lang['Movement'])
            # self.tab_tracker = Frame_Tracker(self)
            # self.tab_master.add(self.tab_tracker, text=self.lang['Tracker'])
            self.tab_controller = Frame_Controller(self)
            self.tab_master.add(self.tab_controller, text=self.lang['Controller'])

            self.tab_master.pack(expand=1, fill='both')
            self.frame_set = 1

    def add_toolbar(self):
        self.toolbar = Menu(self.windows)
        self.add_toolbar_filemenu()
        self.add_toolbar_skeleton()
        self.add_toolbar_movement()
        # self.add_toolbar_tracker()
        self.add_toolbar_controller()
        # self.add_toolbar_mboxemenu()
        self.add_toolbar_helpmenu()
        self.windows.config(menu=self.toolbar)

    def add_toolbar_filemenu(self):
        menu_file = Menu(self.toolbar, tearoff=0)
        menu_file.add_command(label=self.lang['Open Project'], command=self.load_project)
        menu_file.add_separator()

        menu_file.add_command(label=self.lang['English'], command=self.select_EN)
        menu_file.add_command(label=self.lang['French'], command=self.select_FR)
        menu_file.add_separator()
        menu_file.add_command(label=self.lang['Exit'], command=self.quit)
        self.toolbar.add_cascade(label=self.lang['File'], menu=menu_file)

    def add_toolbar_skeleton(self):
        menu_skeleton = Menu(self.toolbar, tearoff=0)
        menu_skeleton.add_command(label=self.lang['Open File'], command=self.load_skeleton)
        menu_skeleton.add_command(label=self.lang['Update'], command=self.update_skeleton)
        menu_skeleton.add_separator()
        menu_skeleton.add_command(label=self.lang["Export to Arduino Sketch"], command=self.tab_skeleton.export_arduino)
        menu_skeleton.add_command(label=self.lang["Recalculate TRIMs"], command=self.tab_skeleton.recalculate_trim)
        menu_skeleton.add_separator()

#        menu_skeleton.add_checkbutton(label=self.lang["Connect Controller"], variable=g.connect_controller, command=self.check_controller)
#        menu_skeleton.add_checkbutton(label=self.lang["Check Motor"], variable=g.check_motor, command=self.check_motor)
#        menu_skeleton.add_checkbutton(label=self.lang["Update Engine at Loading"], variable=g.update_engine, command=self.check_engine)
        self.toolbar.add_cascade(label=self.lang['Skeleton'], menu=menu_skeleton)

    def add_toolbar_movement(self):
        menu_movement = Menu(self.toolbar, tearoff=0)
        menu_movement.add_command(label=self.lang['Load Positions'], command=self.load_position)
        menu_movement.add_command(label=self.lang['Load Movements'], command=self.load_movement)
        self.toolbar.add_cascade(label=self.lang['Movement'], menu=menu_movement)

    def add_toolbar_tracker(self):
        menu_tracker = Menu(self.toolbar, tearoff=0)
        menu_tracker.add_command(label=self.lang['Select Folder'], command=self.load_tracker)
        self.toolbar.add_cascade(label=self.lang['Tracker'], menu=menu_tracker)

    def add_toolbar_controller(self):
        menu_controller = Menu(self.toolbar, tearoff=0)
        menu_controller.add_command(label=self.lang['Open File'], command=self.load_controller)
        menu_controller.add_command(label=self.lang['Update'], command=self.update_controller)
        self.toolbar.add_cascade(label=self.lang['Controller'], menu=menu_controller)

    def add_toolbar_mboxemenu(self):
        self.menu_mboxe = Menu(self.toolbar, tearoff=0)
        self.menu_mboxe.add_command(label=self.lang['To Scan'])
        self.menu_mboxe.add_separator()
        self.toolbar.add_cascade(label=self.lang['Mboxe'], menu=self.menu_mboxe)

    def add_toolbar_helpmenu(self):
        menu_help = Menu(self.toolbar, tearoff=0)
        menu_help.add_command(label=self.lang['About'], command=self.show_about)
        self.toolbar.add_cascade(label=self.lang['Help'], menu=menu_help)

    def load_skeleton(self):
        self.filepath_skeleton = ''
        self.update_skeleton()


    def update_skeleton(self):
        print(self.lang["---Load_Skeleton---"])
        name_file = ''
        if self.filepath_skeleton == '':
            self.filepath_skeleton = askopenfilename(title=self.lang['Select a Skeleton file'],
                                                     filetypes=[('Skeleton files', '.skt'), ('JSON files', '.json'), ('All files', '.*')])
        try:
            with open(self.filepath_skeleton, 'rb') as file:
                g.skeleton_memory = json.load(file, object_pairs_hook=OrderedDict)
            print("%s: %s" % (self.lang['Loading file'], self.filepath_skeleton))
            name_file = path.basename(self.filepath_skeleton)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {}:{} \033[0m'.format(self.lang['Cancel or Error in file management'],self.filepath_skeleton))

        if name_file != '':
            try:
                self.tab_skeleton.skeleton_update(name_file)
                self.tab_interactive.interactive_update(name_file)
            except Exception as e:
                if g.catch_exception.get() == 1:
                    print('\033[31m {}'.format(type(e)))
                    print('{} \033[0m'.format(str(e)))
                else:
                    print('\033[31m {} \033[0m'.format(self.lang['Skeleton processing error']))


    def load_controller(self):
        self.filepath_controller = ''
        self.update_controller()

    def update_controller(self):
        print(self.lang['---Load_Controller---'])
        if self.filepath_controller == '':
            self.filepath_controller = askopenfilename(title=self.lang['Select a Controller file'],
                                                     filetypes=[('Controller files', '.ctl'), ('JSON files', '.json'), ('All files', '.*')])
        try:
            with open(self.filepath_controller, 'rb') as file:
                g.controller_memory = json.load(file)
            print("%s: %s" % (self.lang['Loading file'], self.filepath_controller))
            name_file = path.basename(self.filepath_controller)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Cancel or Error in file management']))

        if self.filepath_controller != '':
            try: self.tab_controller.controller_update(self.filepath_controller)
            except Exception as e:
                if g.catch_exception.get() == 1:
                    print('\033[31m {}'.format(type(e)))
                    print('{} \033[0m'.format(str(e)))
                else:
                    print('\033[31m {} \033[0m'.format(self.lang['Controller processing error']))

    def load_position(self):
        print(self.lang['---Load_Position---'])
        if g.motors_memory == {}:
            showinfo(self.lang['Becarefule'], self.lang['Please load Skeleton before'])
            print(self.lang['Please load Skeleton before'])
        else:
            if self.filepath_position == '':
                try:
                    self.filepath_position = askdirectory(title=self.lang['Select Folder'])
                except Exception as e:
                    if g.catch_exception.get() == 1:
                        print('\033[31m {}'.format(type(e)))
                        print('{} \033[0m'.format(str(e)))
                    else:
                        print('\033[31m {} \033[0m'.format(self.lang['Cancel or Error in file management']))
            try:
                g.position_list = os.listdir(self.filepath_position)
                print("{}: {}".format(self.lang['Folder selected'], self.filepath_position))
                print("{}: {}".format(self.lang['Files list'], g.position_list))
                self.tab_movement.position_update(self.filepath_position)
            except Exception as e:
                if g.catch_exception.get() == 1:
                    print('\033[31m {}'.format(type(e)))
                    print('{} \033[0m'.format(str(e)))
                else:
                    print('\033[31m {} \033[0m'.format(self.lang['Position(s) processing error']))

    def load_movement(self):
        print(self.lang['---Load_movement---'])
        if g.motors_memory == {}:
            showinfo(self.lang['Becarefule'], self.lang['Please load Skeleton before'])
            print(self.lang['Please load Skeleton before'])
        else :
            if self.filepath_movement == '':
                try:
                    self.filepath_movement = askdirectory(title=self.lang['Select Folder'])
                except Exception as e:
                    if g.catch_exception.get() == 1:
                        print('\033[31m {}'.format(type(e)))
                        print('{} \033[0m'.format(str(e)))
                    else:
                        print('\033[31m {} \033[0m'.format(self.lang['Cancel or Error in file management']))
            try:
                g.movement_list = os.listdir(self.filepath_movement)
                print("{}: {}".format(self.lang['Folder selected'], self.filepath_movement))
                print("{}: {}".format(self.lang['Files list'], g.movement_list))
                self.tab_movement.movement_update(self.filepath_movement)
            except Exception as e:
                if g.catch_exception.get() == 1:
                    print('\033[31m {}'.format(type(e)))
                    print('{} \033[0m'.format(str(e)))
                else:
                    print('\033[31m {} \033[0m'.format(self.lang['Movement(s) processing error']))

    def load_project(self):
        print(self.lang['---Load_projet---'])
        self.filepath_project = askopenfilename(title=self.lang['Select a Project file'],
                                                 filetypes=[('Project files', '.pjt'), ('JSON files', '.json'),
                                                            ('All files', '.*')])
        try:
            with open(self.filepath_project, 'r') as file:
                self.project_memory = json.load(file) #, object_pairs_hook=OrderedDict)
            print("%s: %s" % (self.lang['Loading file'], self.filepath_project))
            filepath= self.project_memory['detail']['filepath']

            self.filepath_skeleton = filepath+self.project_memory['detail']['skeleton']
            self.update_skeleton()

            if 'view' in self.project_memory['detail']:
                self.filepath_view = filepath+self.project_memory['detail']['view']
                self.load_view()

            self.filepath_position = filepath+self.project_memory['detail']['position']
            self.load_position()

            self.filepath_movement = filepath+self.project_memory['detail']['movement']
            self.load_movement()

            self.filepath_controller = filepath+self.project_memory['detail']['controller']
            self.update_controller()
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Cancel or Error in file management']))

    def load_view(self):
        try:
            if 'view' in self.project_memory['detail']:
                self.view_win = Toplevel()
                view_img = ImageTk.PhotoImage(Image.open(self.filepath_view))
                view_bt = Button(self.view_win, image=view_img)
                view_bt.pack()
                view_bt.image = view_img
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Cancel or Error in file management']))

    def load_tracker(self):
        try:
            print(self.lang['---Load_tracker---'])
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Cancel or Error in file management']))

    def quit(self):
        if askyesno(self.lang['Quit'], '%s' % self.lang['Are you sure you want to quit ?']):
            self.bye = 'Q'
            self.windows.destroy()

    def select_EN(self):
        self.lang = lang_EN
        self.bye = 'EN'
        self.windows.destroy()

    def select_FR(self):
        self.lang = lang_FR
        self.bye = 'FR'
        self.windows.destroy()

    def show_about(self):
        showinfo(self.lang['About'], '%s %s' % (self.lang['About Text'], self.version))

    def get_lang(self):
        return self.lang

    def get_bye(self):
        return self.bye
