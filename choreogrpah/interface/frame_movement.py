from tkinter import *
from tkinter.filedialog import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk  # pip install pillow
from datetime import datetime
import json
from collections import OrderedDict
import os
from tkinter.messagebox import askyesno
import time

import constants as g

class Frame_Movement(Canvas):

    def __init__(self, interface, **kwargs):
        Canvas.__init__(self, interface.windows, **kwargs)

        self.lang = interface.lang

        self.interface = interface
        self.filepath_movement = ''
        self.position_detail = 0
        self.movement_detail = 0
        self.mov_name = StringVar()
        self.mov_time = IntVar()
        self.mov_time.set(250)
        self.mov_function = {}

        self.fct_win = 0

        # Positions Bank
        position_cv = Canvas(self)
        Label(position_cv, text=self.lang['Positions Bank']).grid(column=0, row=0, pady=2, padx=5,sticky=EW)
        g.position_tree = ttk.Treeview(position_cv)
        g.position_tree['columns'] = ('nb_motor', 'description')
        g.position_tree.heading("#0", text=self.lang['Position'])
        # g.position_tree.column('#0', width=200)
        g.position_tree.heading('nb_motor', text=self.lang['Nbr Motor(s)'])
        g.position_tree.column('nb_motor', width=85)
        g.position_tree.heading('description', text=self.lang['Description'])
        g.position_tree.column('description', width=200)
        g.position_tree.bind("<<TreeviewSelect>>", self.position_selected)

        self.position_sb = Scrollbar(position_cv, orient='vertical', command=g.position_tree.yview)
        g.position_tree.configure(yscrollcommand=self.position_sb.set)
        g.position_tree.grid(column=0, row=1, padx=2, pady=5, sticky=W)
        self.position_sb.grid(column=1, row=1, sticky='nse')
        self.position_sb.configure(command=g.position_tree.yview)
        position_cv.grid(column=0, row=0, padx=2, pady=5, sticky=W)

        # Position Buttons
        position_bt = Canvas(self)
        Button(position_bt, text='-> Robot', command=self.position_robot).grid(column=0, row=0, pady=2, padx=5)
        Button(position_bt, text='{}'.format(self.lang['Remove']), command=self.position_remove).grid(column=1, row=0, pady=2, padx=5)
        Button(position_bt, text='{}'.format(self.lang['Delete file']), command=self.position_delete).grid(column=2, row=0, pady=2, padx=5)
        Button(position_bt, text='{} <-'.format(self.lang['Interactive']), command=self.position_to_interface).grid(column=3, row=0, pady=2, padx=5)
        position_bt.grid(column=0, row=1, padx=2, pady=5)

        # Position Detail
        self.position_detail= LabelFrame(self, text=self.lang['nothing selected'])
        self.position_detail.grid(column=0, row=2, padx=2, pady=5)

        # functions Buttons
        function_cv = Canvas(self)
        Label(function_cv, text="F(x)").grid(column=0, row=0, pady=0, padx=5,sticky=EW)
        Button(function_cv, text='Direct(x)', command=self.direct_insert).grid(column=0, row=1, pady=2, padx=5,sticky=EW)
        Button(function_cv, text='Linear(x)', command=self.linear_win).grid(column=0, row=2, pady=2, padx=5,sticky=EW)
        Button(function_cv, text='Log(x)', state=DISABLED).grid(column=0, row=3, pady=2, padx=5,sticky=EW)
        Button(function_cv, text='Exp(x)', state=DISABLED).grid(column=0, row=4, pady=2, padx=5,sticky=EW)
        Button(function_cv, text='Oscillator(A,O,T,Ph)', command=self.oscillator_win).grid(column=0, row=5, pady=2, padx=5,sticky=EW)
        Button(function_cv, text='none(x)', state=DISABLED).grid(column=0, row=6, pady=2, padx=5,sticky=EW)
        function_cv.grid(column=1, row=2, padx=2, pady=5, sticky=NS)

        # Movements Bank
        movement_cv = Canvas(self)
        Label(movement_cv, text=self.lang["Movements Bank"]).grid(column=0, row=0, pady=2, padx=5,sticky=EW)
        g.movement_tree = ttk.Treeview(movement_cv)
        g.movement_tree['columns'] = ('nb_position', 'time_base')
        g.movement_tree.heading("#0", text='{}s'.format(self.lang['Movement']))
        # g.movement_tree.column('#0', width=200)
        g.movement_tree.heading('nb_position', text='{}'.format(self.lang['Nbr Posit°(s)']))
        g.movement_tree.column('nb_position', width=85)
        g.movement_tree.heading('time_base', text='{}'.format(self.lang['time_base']))
        g.movement_tree.column('time_base', width=85)
        g.movement_tree.bind("<<TreeviewSelect>>", self.movement_selected)

        self.movement_sb = Scrollbar(movement_cv, orient='vertical', command=g.movement_tree.yview)
        g.movement_tree.configure(yscrollcommand=self.movement_sb.set)
        g.movement_tree.grid(column=0, row=1, padx=2, pady=5, sticky=W)
        self.movement_sb.grid(column=1, row=1, sticky='nse')
        self.movement_sb.configure(command=g.movement_tree.yview)
        movement_cv.grid(column=2, row=0, padx=2, pady=5, sticky=W)

        # Movement Buttons
        movement_bt = Canvas(self)
        Button(movement_bt, text=self.lang['New'], command=self.movement_selected).grid(column=0, row=0, pady=2, padx=5)
        Button(movement_bt, text=self.lang['Remove'], command=self.movement_remove).grid(column=1, row=0, pady=2, padx=5)
        Button(movement_bt, text=self.lang['Delete file'], command=self.movement_delete).grid(column=2, row=0, pady=2, padx=5)
        movement_bt.grid(column=2, row=1, padx=2, pady=5)

        # Movement Detail
        self.movement_detail = LabelFrame(self, text=self.lang['nothing selected'])
        self.movement_detail.grid(column=2, row=2, padx=2, pady=5)

    def position_update(self, filepath_position):
        self.filepath_position = filepath_position

        for position_file in g.position_list:
            with open(filepath_position + '/' + position_file, 'rb') as file:
                position = json.load(file, object_pairs_hook=OrderedDict)
            position['file'] = filepath_position + '/' + position_file
            category = position['category']
            name = '{}_{}'.format(position['category'], position['name'])
            description = position['description']
            n_motor = len(position['motors'])
            state = 0
            for cle, value in position['motors'].items():
                if cle in g.motors_memory:
                    state = 1
                else:
                    print('{}: {} {}: {}'.format(name, self.lang['Motor'], cle, self.lang['not in skeleton']))
                    state = 0

            if state == 1:
                g.position_memory[name] = position
                if not g.position_tree.exists(category):
                    g.position_tree.insert('', 'end', category, text=category)
                g.position_tree.insert(category, 'end', text=name, values=(n_motor, description[0:35]))

    def position_selected(self, event):
        try:
            for item in g.position_tree.selection():
                name = g.position_tree.item(item, "text")
                if name in g.position_memory:
                    self.position_detail.destroy()
                    self.position_detail= LabelFrame(self, text=name)
                    Label(self.position_detail, text="{}: ...{}".format(self.lang['File'], g.position_memory[name]['file'][-80:])).grid(column=0, row=0, padx=2, sticky=W)
                    Label(self.position_detail, text="{}: {}".format(self.lang['Category'], g.position_memory[name]['category'])).grid(column=0, row=1, padx=2, sticky=W)
                    Label(self.position_detail, text="{}: {}".format(self.lang['Description'], g.position_memory[name]['description'])).grid(column=0, row=2, padx=2, sticky=W)

                    Label(self.position_detail, text="{}s: ".format(self.lang['Motor'])).grid(column=0, row=3, padx=2, sticky=W)
                    frame_row = 4
                    for motor in g.position_memory[name]['motors'].items():
                        Label(self.position_detail, text='{} : {}'.format(motor[0], motor[1])).grid(column=0, row=frame_row, padx=10, sticky=W)
                        frame_row += 1

                self.position_detail.grid(column=0, row=2, padx=2, pady=5, sticky='EW')
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def position_remove(self):
        try:
            for item in g.position_tree.selection():
                name = g.position_tree.item(item, "text")
                if name in g.position_memory:
                    del g.position_memory[name]
                g.position_tree.delete(item)
            self.position_detail.destroy()
            self.position_detail = LabelFrame(self)
            self.position_detail.grid(column=0, row=2, padx=2, pady=5, sticky='EW')
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def position_delete(self):
        try:
            for item in g.position_tree.selection():
                name = g.position_tree.item(item, "text")
                file = g.position_memory[name]['file']
                if askyesno(self.lang['Delete File'], '{}: ...{} ?'.format(self.lang['Are you sure you want to delete file'], file[-20:])):
                    if os.path.exists(file):
                        os.remove(file)
                        print('{} {}: {}'.format(self.lang['File'], self.lang['deleted'], file))
                    if name in g.position_memory:
                        del g.position_memory[name]
                    g.position_tree.delete(item)
                    self.position_detail.destroy()
                    self.position_detail = LabelFrame(self)
                    self.position_detail.grid(column=0, row=2, padx=2, pady=5, sticky='EW')
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def position_to_interface(self):
        try:
            for item in g.position_tree.selection():
                name_selection = g.position_tree.item(item, "text")
                if name_selection in g.position_memory:
                    g.interface_category = g.position_memory[name_selection]['category']
                    g.interface_name = g.position_memory[name_selection]['name']
                    g.interface_description = g.position_memory[name_selection]['description']
                    for motor in g.motors_memory.items():
                        motor[1]['selected'].set(0)
                    for motor in g.position_memory[name_selection]['motors'].items():
                        name_motor = motor[0]
                        position = int(motor[1])
                        g.motors_memory[name_motor]['position_it'].set(position)
                        g.motors_memory[name_motor]['selected'].set(1)
                    self.interface.tab_master.select(self.interface.tab_interactive)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def position_robot(self):
        name_motor = ''
        for item in g.position_tree.selection():
            name_selection = g.position_tree.item(item, "text")
            if name_selection in g.position_memory:
                 for motor in g.position_memory[name_selection]['motors'].items():
                    name_motor = motor[0]
                    position = int(motor[1])
                    g.motors_memory[name_motor]['position_it'].set(position)

        if name_motor != '':
            self.interface.tab_interactive.change_all()

    def movement_update(self, filepath_movement):
        for movement_file in g.movement_list:
            with open(filepath_movement + '/' + movement_file, 'rb') as file:
                movement = json.load(file) #, object_pairs_hook=OrderedDict)
            movement['file'] = filepath_movement + '/' + movement_file
            name = movement['name']
            duration = movement['duration']
            n_function= len(movement['functions'])
            state = 1
            for cle, value in movement['functions'].items():
                if value['position'] not in g.position_memory:
                    print('{} {}: {} {} {}'.format(self.lang['In Movement'], name, self.lang['Position'], value['position'], self.lang['unknown']))
                    state = 0
            if state == 1:
                g.movement_memory[name] = movement
                insert_id = g.movement_tree.insert('', 'end', text=name, values=(n_function, duration))
                g.movement_memory[name]['id'] = insert_id

    def movement_selected(self, event=''):
        try:
            self.mov_function = {}

            if event != '':
                item = g.movement_tree.selection()
                name = g.movement_tree.item(item[0], "text")
                movement = g.movement_memory[name]
                self.movement_detail.destroy()
                self.movement_detail = LabelFrame(self, text='...{}'.format(movement['file'][-50:]))
                self.mov_name.set(name)
                self.mov_time.set(movement['duration'])
            else:
                movement = {}
                self.movement_detail.destroy()
                self.movement_detail = LabelFrame(self, text='New')
                self.mov_name.set('')
                self.mov_time.set(250)

            Label(self.movement_detail, text="{} :".format(self.lang['Name'])).grid(column=0, row=0, padx=2, pady=5, sticky=W)
            Entry(self.movement_detail, textvariable=self.mov_name, width=20).grid(column=1, row=0, padx=2, pady=5, sticky=W)
            Label(self.movement_detail, text="{} (ms):".format(self.lang['Time Base'])).grid(column=0, row=1, padx=2, pady=5, sticky=W)
            Entry(self.movement_detail, textvariable=self.mov_time, width=5).grid(column=1, row=1, padx=2, pady=5, sticky=W)

            mov_cv = Canvas(self.movement_detail)
            g.mov_detail_tree = ttk.Treeview(mov_cv)
            g.mov_detail_tree['columns'] = ('position', 'duration', 'nb_step')
            g.mov_detail_tree.heading("#0", text=self.lang['function'])
            g.mov_detail_tree.column('#0', width=100)
            g.mov_detail_tree.heading('position', text=self.lang['Position'])
            g.mov_detail_tree.column('position', width=100)
            g.mov_detail_tree.heading('duration', text=self.lang['Duration (ms)'])
            g.mov_detail_tree.column('duration', width=85)
            g.mov_detail_tree.heading('nb_step', text=self.lang['Nbr Step(s)'])
            g.mov_detail_tree.column('nb_step', width=85)

            if event !='':
                for cle, value in movement['functions'].items():
                    insert_id = g.mov_detail_tree.insert('', 'end', text=value['function'], values=(value['position'], value['duration'], value['nb_step']))

                    self.mov_function[insert_id] = {}
                    self.mov_function[insert_id]['function'] = value['function']
                    self.mov_function[insert_id]['position'] = value['position']
                    self.mov_function[insert_id]['duration'] = value['duration']
                    self.mov_function[insert_id]['nb_step'] = value['nb_step']
                    if 'data' in value:
                        self.mov_function[insert_id]['data'] = value['data']

            g.mov_detail_tree.bind("<Double-1>", self.movDouble_click)
            g.mov_detail_tree.grid(column=0, row=0, padx=2, pady=5, sticky=W)

            mov_play = LabelFrame(mov_cv)
            button_delete = Button(mov_play, text=self.lang['Delete Line'], command=self.movDetail_deleteLine)
            button_delete.grid(column=0, row=0, pady=2, padx=5, sticky=W)
            button_play = Button(mov_play, text=self.lang['Play One'], command=self.movement_play_one)
            button_play.grid(column=1, row=0, pady=2, padx=5, sticky=W)
            button_up = Button(mov_play, text=self.lang['Up'], command=self.movDetail_up)
            button_up.grid(column=2, row=0, pady=2, padx=5, sticky=W)
            button_down = Button(mov_play, text=self.lang['Down'], command=self.movDetail_down)
            button_down.grid(column=3, row=0, pady=2, padx=5, sticky=W)
            mov_play.grid(column=0, row=1, padx=2, pady=5)

            mov_bt = LabelFrame(mov_cv)
            Button(mov_bt, text=self.lang['Play All'], command=self.movement_play_all).grid(column=0, row=3, pady=2, padx=5)
            Button(mov_bt, text=self.lang['Save As'], command=self.movement_save).grid(column=1, row=3, padx=3, pady=3)
            Button(mov_bt, text=self.lang['Export to C'], command=self.export_to_c).grid(column=2, row=3, padx=3, pady=3)
            mov_bt.grid(column=0, row=2, padx=2, pady=5)

            mov_cv.grid(column=0, row=2, columnspan=2, padx=2, pady=5)

            self.movement_detail.grid(column=2, row=2, padx=2, pady=5)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def movement_save(self):
        try:
            dict2json = {}
            name = self.mov_name.get()
            dict2json['name'] = name
            dict2json['duration'] = self.mov_time.get()
            dict2json['functions'] = {}
            if dict2json['name'] != '' and dict2json['duration'] != '':
                print('{}={}'.format(self.lang['function'], self.mov_function))
                dict2json['functions'] = self.mov_function
                print('fjson={}'.format(dict2json['functions']))

                if name in g.movement_memory:
                    g.movement_tree.delete(g.movement_memory[dict2json['name']]['id'])
                g.movement_memory[name] = dict2json
                insert_id = g.movement_tree.insert('', 'end', text=dict2json['name'], values=(len(dict2json['functions']), dict2json['duration']))
                g.movement_tree.selection_set(insert_id)
                g.movement_memory[name]['id']= insert_id
                if 'file' not in dict2json:
                    file = '{}.mov'.format(dict2json['name'])
                    dict2json['file'] = 'Not saved'
                else:
                    file = dict2json['file']
                f = asksaveasfilename(title="Save a Movement", initialfile=file, defaultextension='.mov', filetypes=[('Movement files', '.mov'), ('All files', '.*')])
                if f is None or f == '':
                    pass
                else:
                    with open(f, 'w') as fp:
                        dict2json['file'] = f
                        json.dump(dict2json, fp, indent=2)
                    g.movement_memory[dict2json['name']]['file'] = f
                self.movement_selected('')
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def movement_remove(self):
        try:
            for item in g.movement_tree.selection():
                name = g.movement_tree.item(item, "text")
                if name in g.movement_memory:
                    del g.movement_memory[name]
                g.movement_tree.delete(item)
            self.movement_detail.destroy()
            self.movement_detail = LabelFrame(self, text='nothing selected')
            self.movement_detail.grid(column=2, row=2, padx=2, pady=5)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def movement_delete(self):
        try:
            for item in g.movement_tree.selection():
                name = g.movement_tree.item(item, "text")
                file = g.movement_memory[name]['file']
                if askyesno('{}'.format(self.lang['Delete File']), '{}: ...{} ?'.format(self.lang['Are you sure you want to delete file'], file[-20:])):
                    if os.path.exists(file):
                        os.remove(file)
                        print('{} {}: {}'.format(self.lang['File'], file, self.lang['deleted']))
                    if name in g.movement_memory:
                        del g.movement_memory[name]
                    g.movement_tree.delete(item)
                    self.movement_detail.destroy()
                    self.movement_detail = LabelFrame(self, text='nothing selected')
                    self.movement_detail.grid(column=2, row=2, padx=2, pady=5)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def linear_win(self, item=''):
        try:
            if item == '':
                item_position = g.position_tree.selection()[0]
                name_position = g.position_tree.item(item_position, "text")
                duration = IntVar()
                duration.set(self.mov_time.get())
            else:
                name_position = self.mov_function[item]['position']
                duration = IntVar()
                duration.set(self.mov_function[item]['duration'])

            if name_position in g.position_memory:
                self.fct_win = Toplevel()
                self.fct_win.title('{}: Linear'.format(self.lang['function']))
                Label(self.fct_win, text="{}: {}".format(self.lang['Position Selected'], name_position)).grid(columnspan=2, column=0, row=0, padx=2, sticky=W)
                Label(self.fct_win, text="{}: {} ms".format(self.lang['Time Base'], self.mov_time.get())).grid(columnspan=2, column=0, row=1, padx=2, sticky=W)

                Label(self.fct_win, text='{}:'.format(self.lang['Duration (ms)'])).grid(column=0, row=2, padx=2, pady=10, sticky=W)
                Entry(self.fct_win, textvariable=duration, width=5).grid(column=1, row=2, pady=2, sticky=W)
                if item == '':
                    Button(self.fct_win, text='{}'.format(self.lang['Insert']), command=lambda x=(name_position, duration): self.linear_insert(x)).grid(columnspan=2, column=0, row=3, padx=3, pady=3)
                else:
                    Button(self.fct_win, text='{}'.format(self.lang['Update']), command=lambda x=(item, duration): self.linear_update(x)).grid(columnspan=2, column=0, row=3, padx=3, pady=3)

            else:
                print('{}'.format(self.lang['For create a movement, select a position before']))
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def linear_insert(self, x):
        try:
            step = int(int(x[1].get()) / int(self.mov_time.get()))
            insert_id = g.mov_detail_tree.insert('', 'end', text='Linear', values="{} {} {}".format(x[0], x[1].get(), step))
            self.mov_function[insert_id] = {}
            self.mov_function[insert_id]['function'] = 'Linear'
            self.mov_function[insert_id]['position'] = x[0]
            self.mov_function[insert_id]['duration'] = x[1].get()
            self.mov_function[insert_id]['nb_step'] = step

            g.mov_detail_tree.see(insert_id)
            self.fct_win.destroy()
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def linear_update(self, x):
        try:
            item = x[0]
            step = int(int(x[1].get()) / int(self.mov_time.get()))
            g.mov_detail_tree.set(item, '#2', x[1].get())
            g.mov_detail_tree.set(item, '#3', step)

            self.mov_function[item]['duration'] = x[1].get()
            self.mov_function[item]['nb_step'] = step

            g.mov_detail_tree.see(item)
            self.fct_win.destroy()
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def oscillator_win(self, item=''):
        try:
            if item == '':
                item_position = g.position_tree.selection()[0]
                name_position = g.position_tree.item(item_position, "text")
                self.duration = IntVar()
                self.duration.set(self.mov_time.get())
                self.cycle = IntVar()
                self.cycle.set(1)

            else:
                name_position = self.mov_function[item]['position']
                self.duration = IntVar()
                self.duration.set(self.mov_function[item]['duration'])
                self.cycle = IntVar()
                self.cycle.set(self.mov_function[item]['data']['cycle'])

            if name_position in g.position_memory:
                self.fct_win = Toplevel()
                self.fct_win.title('{}: Oscillator'.format(self.lang['function']))
                Label(self.fct_win, text='{}:'.format(self.lang['Position Selected'])).grid(column=0, row=0, padx=2, sticky=W)
                Label(self.fct_win, text="{}".format(name_position)).grid(column=1, row=0, padx=2, sticky=W)
                Label(self.fct_win, text='{}:'.format(self.lang['Duration (ms)'])).grid(column=0, row=2, padx=2, pady=10, sticky=W)
                Entry(self.fct_win, textvariable=self.duration, width=5).grid(column=1, row=2, pady=2, sticky=W)
                Label(self.fct_win, text='{}:'.format(self.lang['Cycle'])).grid(column=0, row=3, padx=2, pady=10, sticky=W)
                Entry(self.fct_win, textvariable=self.cycle, width=5).grid(column=1, row=3, pady=2, sticky=W)

                i = 0
                self.ll_pin = {}
                self.ll_A = {}
                self.ll_O= {}
                self.ll_Ph = {}
                motors_lf = LabelFrame(self.fct_win)
                for motor in g.position_memory[name_position]['motors'].items():
                    self.ll_pin[str(i)] = IntVar()
                    self.ll_pin[str(i)].set(g.motors_memory[motor[0]]['id'])
                    self.ll_A[str(i)] = IntVar()
                    self.ll_O[str(i)] = IntVar()
                    self.ll_Ph[str(i)] = IntVar()
                    if item != '':
                        self.ll_pin[str(i)].set(self.mov_function[item]['data']['pin'][str(i)])
                        self.ll_A[str(i)].set(self.mov_function[item]['data']['A'][str(i)])
                        self.ll_O[str(i)].set(self.mov_function[item]['data']['O'][str(i)])
                        self.ll_Ph [str(i)].set(self.mov_function[item]['data']['Ph'][str(i)])

                    Label(motors_lf, text='{}: pin='.format(motor[0])).grid(column=0, row=i, padx=1, pady=2, sticky=E)
                    Entry(motors_lf, textvariable=self.ll_pin[str(i)], width=5, state=DISABLED).grid(column=1, row=i, padx=1, pady=2, sticky=W)
                    Label(motors_lf, text='{}: A='.format(motor[0])).grid(column=2, row=i, padx=1, pady=2, sticky=E)
                    Entry(motors_lf, textvariable=self.ll_A[str(i)], width=5).grid(column=3, row=i, padx=1, pady=2, sticky=W)
                    Label(motors_lf, text='O=').grid(column=4, row=i, padx=1, pady=2, sticky=E)
                    Entry(motors_lf, textvariable=self.ll_O[str(i)],width=5).grid(column=5, row=i, padx=1, pady=2, sticky=W)
                    Label(motors_lf, text='Phase Diff=').grid(column=6, row=i, padx=1, pady=2, sticky=E)
                    Entry(motors_lf, textvariable=self.ll_Ph[str(i)],width=5).grid(column=7, row=i, padx=1, pady=2, sticky=W)
                    i += 1

                motors_lf.grid(column=0, columnspan=2, row=4, padx=10, sticky=W)
                if item == '':
                    Button(self.fct_win, text='{}'.format(self.lang['Insert']), command=lambda x=(name_position, i): self.oscillator_insert(x)).grid(columnspan=2, column=0, row=5, padx=3, pady=3)
                else:
                    Button(self.fct_win, text='{}'.format(self.lang['Update']), command=lambda x=(item, i): self.oscillator_update(x)).grid(columnspan=2, column=0, row=5, padx=3, pady=3)
            else:
                print('{}'.format(self.lang['For create a movement, select a position before']))
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def oscillator_insert(self, x):
        try:
            Nb = int(x[1])
            T = int(self.duration.get())
            cycle = int(self.cycle.get())
            pin = {}
            A = {}
            O = {}
            Ph= {}
            j = 0
            for i in range(0, Nb):
                if self.ll_A[str(i)].get() != 0:
                    pin[str(i)] = self.ll_pin[str(i)].get()
                    A[str(i)] = self.ll_A[str(i)].get()
                    O[str(i)] = self.ll_O[str(i)].get()
                    Ph[str(i)] = self.ll_Ph[str(i)].get()
                    j += 1
            Nb = j
            step = int( T / int(self.mov_time.get()))
            insert_id = g.mov_detail_tree.insert('', 'end', text='Oscillator', values="{} {} {}".format(x[0], T, step))
            self.mov_function[insert_id] = {}
            self.mov_function[insert_id]['function'] = 'Oscillator'
            self.mov_function[insert_id]['position'] = x[0]
            self.mov_function[insert_id]['duration'] = T
            self.mov_function[insert_id]['nb_step'] = step

            self.mov_function[insert_id]['data'] = {}
            self.mov_function[insert_id]['data']['cycle'] = cycle
            self.mov_function[insert_id]['data']['T'] = T
            self.mov_function[insert_id]['data']['Nb'] = Nb
            self.mov_function[insert_id]['data']['pin'] = pin
            self.mov_function[insert_id]['data']['A'] = A
            self.mov_function[insert_id]['data']['O'] = O
            self.mov_function[insert_id]['data']['Ph'] = Ph

            g.mov_detail_tree.see(insert_id)
            self.fct_win.destroy()
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def oscillator_update(self, x):
        try:
            item = x[0]
            Nb = int(x[1])
            T = int(self.duration.get())
            cycle = int(self.cycle.get())
            pin = {}
            A = {}
            O = {}
            Ph= {}
            j = 0
            for i in range(0, Nb):
                if self.ll_A[str(i)].get() != 0:
                    pin[str(i)] = self.ll_pin[str(i)].get()
                    A[str(i)] = self.ll_A[str(i)].get()
                    O[str(i)] = self.ll_O[str(i)].get()
                    Ph[str(i)] = self.ll_Ph[str(i)].get()
                    j += 1
            Nb = j
            step = int( T / int(self.mov_time.get()))

            g.mov_detail_tree.set(item, '#2', T)
            g.mov_detail_tree.set(item, '#3', step)
            self.mov_function[item]['duration'] = T
            self.mov_function[item]['nb_step'] = step

            self.mov_function[item]['data']['cycle'] = cycle
            self.mov_function[item]['data']['T'] = T
            self.mov_function[item]['data']['Nb'] = Nb
            self.mov_function[item]['data']['pin'] = pin
            self.mov_function[item]['data']['A'] = A
            self.mov_function[item]['data']['O'] = O
            self.mov_function[item]['data']['Ph'] = Ph

            g.mov_detail_tree.see(item)
            self.fct_win.destroy()
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def direct_insert(self):
        try:
            item_position = g.position_tree.selection()[0]
            name_position = g.position_tree.item(item_position, "text")

            if name_position in g.position_memory:
                insert_id = g.mov_detail_tree.insert('', 'end', text='Direct', values="{} {} {}".format(name_position, int(self.mov_time.get()), 1))
                self.mov_function[insert_id] = {}
                self.mov_function[insert_id]['function'] = 'Direct'
                self.mov_function[insert_id]['position'] = name_position
                self.mov_function[insert_id]['duration'] = int(self.mov_time.get())
                self.mov_function[insert_id]['nb_step'] = 1

                g.mov_detail_tree.see(insert_id)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def movDouble_click(self, event):
        try:
            item = g.mov_detail_tree.selection()
            function= self.mov_function[item[0]]['function']
            if function == 'Linear':
                self.linear_win(item[0])
            if function == 'Oscillator':
                self.oscillator_win(item[0])
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def movDetail_deleteLine(self):
        try:
            item = g.mov_detail_tree.selection()[0]
            g.mov_detail_tree.delete(item)
            if item in self.mov_function:
                del self.mov_function[item]
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def movDetail_up(self):
        try:
            item = g.mov_detail_tree.selection()[0]
            parent = g.mov_detail_tree.parent(item)
            last = g.mov_detail_tree.prev(item)
            last_index= g.mov_detail_tree.index(last)
            g.mov_detail_tree.move(item, parent, last_index)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def movDetail_down(self):
        try:
            item = g.mov_detail_tree.selection()[0]
            parent = g.mov_detail_tree.parent(item)
            next = g.mov_detail_tree.next(item)
            next_index= g.mov_detail_tree.index(next)
            g.mov_detail_tree.move(item, parent, next_index)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(
                    self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def movement_play_one(self):
        try:
            for item in g.mov_detail_tree.selection():
                function_selected = self.mov_function[item]['function']
                position_selected = self.mov_function[item]['position']
                duration_selected = int(self.mov_function[item]['duration'])

                self.movement_play(item, function_selected, position_selected, duration_selected)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(
                    self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def movement_play_all(self):
        try:
            self.play_win = Toplevel()
            now = datetime.now()
            self.play_win.title('{}: {} {}'.format(self.mov_name.get(), self.lang['play all at'], now.strftime('%H:%M:%S')))
            tt_play = Text(self.play_win)
            tt_play.grid(column=0, row=0, sticky=N)
            for item, mov in self.mov_function.items():
                function_selected = mov['function']
                position_selected = mov['position']
                duration_selected = int(mov['duration'])
                tt_play.insert(END, '\n{}: {} {} {} ms\n'.format(function_selected, position_selected, self.lang['in'], duration_selected))
                tt_play.insert(END, '---------------------------------------------\n')

                if function_selected == 'Oscillator':
                    tt_play.insert(END, '   {}(s):  {}\n'.format(self.lang['Cycle'], self.mov_function[item]['data']['cycle']))
                    tt_play.insert(END, '   Servo(s): {}\n'.format(self.mov_function[item]['data']['Nb']))
                    tt_play.insert(END, '   T:             {}\n'.format(self.mov_function[item]['data']['T']))
                    tt_play.insert(END, '   pin:           {}\n'.format(self.mov_function[item]['data']['pin']))
                    tt_play.insert(END, '   A:             {}\n'.format(self.mov_function[item]['data']['A']))
                    tt_play.insert(END, '   O:             {}\n'.format(self.mov_function[item]['data']['O']))
                    tt_play.insert(END, '   Ph             {}\n'.format(self.mov_function[item]['data']['Ph']))
                else:
                    for cle, value in g.position_memory[position_selected]['motors'].items():
                        tt_play.insert(END, '   {} (pin{}): {} => {}\n'.format(cle, g.motors_memory[cle]['id'], self.lang['Position'], value))

                tt_play.see(END)
                self.play_win.update()
                self.movement_play(item, function_selected, position_selected, duration_selected)
                self.play_win.after(duration_selected)
            tt_play.insert(END, '\n------------- {} ---------------------------\n'.format(self.lang['END']))
            tt_play.see(END)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(
                    self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def movement_play(self, item, function_selected, position_selected, duration_selected):
        try:
            i = 0
            motors = {}
            positions = {}
            pin = {}
            orientations = {}

            for cle, value in g.position_memory[position_selected]['motors'].items():
                motors[i] = cle
                positions[i] = int(value)
                pin[i] = g.motors_memory[cle]['id']
                orientations[i] = g.motors_memory[cle]['orientation']
                g.motors_memory[cle]['position_it'].set(value)
                i += 1

            if i > 0:
                if function_selected == 'Direct':
                    g.motors_memory[motors[0]]['engine'].fct_moveServos(duration_selected, i, pin, positions, orientations)
                if function_selected == 'Linear':
                    g.motors_memory[motors[0]]['engine'].fct_moveServos(duration_selected, i, pin, positions, orientations)
                if function_selected == 'Oscillator':
                    cycle = self.mov_function[item]['data']['cycle']
                    T = self.mov_function[item]['data']['T']
                    Nb = self.mov_function[item]['data']['Nb']
                    pin = self.mov_function[item]['data']['pin']
                    A = self.mov_function[item]['data']['A']
                    O = self.mov_function[item]['data']['O']
                    Ph = self.mov_function[item]['data']['Ph']
                    g.motors_memory[motors[0]]['engine'].fct_oscillateServos(cycle, T, Nb, pin, A, O, Ph)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(
                    self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def export_to_c(self):
        try:
            toc_win = Toplevel()
            toc_win.title('{} C'.format(self.lang['Export to']))
            toc_text = Text(toc_win, height=50, width=150)
            toc_text.grid(column=0, row=0, sticky=N)

            toc_text.insert(END, '// {}={}\n'.format(self.lang['List of positions: position'], '{pin, position}'))
            positions = {}
            for item, mov in self.mov_function.items():
                position_selected = mov['position']
                pin = []
                position = []
                for cle, value in g.position_memory[position_selected]['motors'].items():
                    pin.append(str(g.motors_memory[cle]['id']))
                    position.append(value)
                if position_selected not in positions:
                    positions[position_selected] = {}
                    positions[position_selected]['pin'] = pin
                    positions[position_selected]['pos'] = position

            for pos, value in positions.items():
                toc_text.insert(END, 'int pos_{}[2][{}]={}'.format(pos.replace('-', '_').replace(' ', '_'), len(value['pin']), '{ {'))
                toc_text.insert(END, '{}{}'.format(",".join(value['pin']), '}, {'))
                toc_text.insert(END, '{}{}\n'.format(",".join(value['pos']), '} };'))



            toc_text.insert(END, '\n// {}\n'.format(self.lang['Optional data for some functions']))
            for item, mov in self.mov_function.items():
                function_selected = mov['function']
                if 'data' in mov and function_selected == 'Oscillator':
                    A = []
                    O = []
                    Ph = []
                    toc_text.insert(END, 'int {}[3][{}]= {}'.format(item, len(mov['data']['A']), '{ {'))
                    for a_value in mov['data']['A'].values():
                        A.append(str(a_value))
                    toc_text.insert(END, '{}{}'.format(",".join(A), '}, {'))
                    for O_value in mov['data']['O'].values():
                        O.append(str(O_value))
                    toc_text.insert(END, '{}{}'.format(",".join(O), '}, {'))
                    for Ph_value in mov['data']['Ph'].values():
                        Ph.append(str(Ph_value))
                    toc_text.insert(END, '{}{}\n'.format(",".join(Ph), '} };'))


            toc_text.insert(END, '\n// {}\n'.format(self.lang['Movement = {function, pointer to basic position, duration, number of cycles, pointer to optional data}']))
            toc_text.insert(END, 'movement mov_{}[{}]={}'.format(self.mov_name.get().lower().replace('-', '_').replace(' ', '_'), len(self.mov_function), '{'))
            for item, mov in self.mov_function.items():
                function_selected = mov['function']
                position_selected = mov['position'].replace('-', '_').replace(' ', '_')
                duration_selected = int(mov['duration'])
                toc_text.insert(END, '\n{ ')
                toc_text.insert(END, '{}, (int*) &pos_{}, {}'.format(function_selected.upper(), position_selected, duration_selected))

                if 'data' in mov:
                    toc_text.insert(END, ', {}, (int*) &{}'.format(mov['data']['cycle'], item))
                else:
                    toc_text.insert(END, ', 1,')

                toc_text.insert(END, '}, ')

            toc_text.delete('end - 3 chars', END)
            toc_text.insert(END, '\n};\n')
        except:
            print('\033[31m {} \033[0m'.format(self.lang['Error while translating the skeleton']))

