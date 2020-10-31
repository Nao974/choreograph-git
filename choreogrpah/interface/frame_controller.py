from tkinter.filedialog import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk  # pip install pillow
import os
import time
import constants as g

class Frame_Controller(Canvas):
    def __init__(self, interface, **kwargs):
        Canvas.__init__(self, interface.windows, **kwargs)

        self.lang = interface.lang

        self.frame_row = 0
        self.frame_column = 0
        self.command = {}
        self.syek = {}

        Label(self, text=self.lang['No file loaded, Menu Controller->Open File']).grid(column=0, row=0, pady=2, padx=5, sticky=W)
        interface.windows.bind('<Key>', self.keyPressed)
        
    def controller_update(self, name_file):
        for obj in self.winfo_children():
            obj.destroy()

        if not g.controller_memory == {}:
            pathname= os.path.dirname(name_file)
            filename= os.path.basename(name_file)
            controller = g.controller_memory.get('controller')

            image = Image.open(pathname+'/'+controller["picture"])
            photo = ImageTk.PhotoImage(image)
            x, y = image.size
            frame_controller = Canvas(self, width=x, height= y)
            frame_controller.create_image(0,0, image=photo, anchor="nw")
            frame_controller.image= photo
            frame_controller.grid(column=0, row=0, pady=2, padx=5, sticky=W)
            Label(self, text=filename).grid(column=0, row=0, pady=2, padx=5,sticky=NW)

            frame_keys = LabelFrame(self, text=self.lang['Keys'])

            for i in range(2):
                frame_keys.columnconfigure(i, minsize=int(x/2))
            Checkbutton(frame_keys, text=self.lang['Bind Keys'], variable=g.bind_key).grid(column=0, row=0, pady=2, padx=2, sticky=W)

            keys = g.controller_memory["keys"]
            for k in keys:
                val = keys[k]
                self.syek[val]= k
            keys_button={}
            tab_l = LabelFrame(frame_keys)
            key = 'L1'
            keys_button[key]= Button(tab_l, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=0, row=0, pady=2, padx=5, sticky="w")
            key = 'L2'
            keys_button[key]= Button(tab_l, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=0, row=1, pady=2, padx=5, sticky="w")
            tab_l.grid(column=0, row=1, pady=2, padx=5)#  , sticky="nesw")
            tab_r= LabelFrame(frame_keys)

            tab_r = LabelFrame(frame_keys)
            key = 'R1'
            keys_button[key]= Button(tab_r, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=0, row=0, pady=2, padx=5, sticky="w")
            key = 'R2'
            keys_button[key]= Button(tab_r, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=0, row=1, pady=2, padx=5, sticky="w")
            tab_r.grid(column=1, row=1, pady=2, padx=5)#  , sticky="nesw")

            tab_c= LabelFrame(frame_keys)
            key = 'UP'
            keys_button[key]= Button(tab_c, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=1, row=0, pady=2, padx=5, sticky="ew")
            key = 'LF'
            keys_button[key]= Button(tab_c, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=0, row=1, pady=2, padx=5, sticky="e")
            key = 'RG'
            keys_button[key]= Button(tab_c, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=2, row=1, pady=2, padx=5, sticky="w")
            key = 'DW'
            keys_button[key]= Button(tab_c, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=1, row=2, pady=2, padx=5, sticky="ew")
            tab_c.grid(column=0, row=2, pady=2, padx=5)#  , sticky="nesw")

            tab_b = LabelFrame(frame_keys)
            key = 'T'
            keys_button[key]= Button(tab_b, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=1, row=0, pady=2, padx=5, sticky="ew")
            key = 'S'
            keys_button[key]= Button(tab_b, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=0, row=1, pady=2, padx=5, sticky="e")
            key = 'O'
            keys_button[key]= Button(tab_b, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=2, row=1, pady=2, padx=5, sticky="w")
            key = 'X'
            keys_button[key]= Button(tab_b, text=key+"="+keys[key], command=lambda x=key: self.action4button(x), repeatdelay=50, repeatinterval=1).grid(column=1, row=2, pady=2, padx=5, sticky="ew")
            tab_b.grid(column=1, row=2, pady=2, padx=5)#  , sticky="nesw")

            frame_keys.grid(column=0, row=1, pady=2, padx=5, sticky="nesw")

            tree = ttk.Treeview(self,style="mystyle.Treeview")
            tree['columns'] = ('movement')
            tree.column('#0', width=50)
            tree.column('movement', width=100)
            tree.heading("#0", text=self.lang['Key'])
            tree.heading('movement', text=self.lang['Movement'])

            for cle, value in g.controller_memory["movements"].items():
                tree.insert('', 'end', text=cle, values=value)

            tree.grid(column=1, row=0, padx=2, pady=5, sticky="nesw")

        else:
            Label(self, text=self.lang['No file loaded, Menu Controller->Open File']).grid(column=0, row=0, pady=2, padx=5,sticky=W)

    def action4button(self, button):
        try:
            mov_name = g.controller_memory["movements"][button]
            if mov_name in g.movement_memory:
                mov_functions = g.movement_memory[mov_name]['functions']
                print("Button={} => Mov={}".format(button, mov_name))
                for cle, value in mov_functions.items():
                    i = 0
                    motors = {}
                    positions = {}
                    pin = {}
                    orientation = {}
                    duration_selected = int(value['duration'])
                    function_selected = value['function']
                    position_selected = value['position']
                    for cle_m, value_m in g.position_memory[position_selected]['motors'].items():
                        motors[i] = cle_m
                        positions[i] = int(value_m)
                        pin[i] = g.motors_memory[cle_m]['id']
                        orientation[i] = g.motors_memory[cle_m]['orientation']
                        g.motors_memory[cle_m]['position_it'].set(value_m)
                        i += 1

                    if i > 0:
                        if function_selected == 'Direct':
                            g.motors_memory[motors[0]]['engine'].fct_moveServos(duration_selected, i, pin, positions, orientation)
                        if function_selected == 'Linear':
                            g.motors_memory[motors[0]]['engine'].fct_moveServos(duration_selected, i, pin, positions, orientation)
                        if function_selected == 'Oscillator':
                            cycle = value['data']['cycle']
                            T = value['data']['T']
                            Nb = value['data']['Nb']
                            pin = value['data']['pin']
                            A = value['data']['A']
                            O = value['data']['O']
                            Ph = value['data']['Ph']
                            g.motors_memory[motors[0]]['engine'].fct_oscillateServos(cycle, T, Nb, pin, A, O, Ph)
                    time.sleep(duration_selected/1000)
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Management error between key and movement']))
    def keyPressed(self,event):
        try:
            if g.bind_key.get() == 1:
                key = event.char
                print('{}={}'.format(self.lang['Key pressed'], key))
                self.action4button(self.syek[key])
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Management error between key and movement']))
