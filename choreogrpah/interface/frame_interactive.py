from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import Image, ImageTk  # pip install pillow
from _mboxe.mboxe_dummy import *
import constants as g
import json

class Frame_Interactive(Canvas):

    def __init__(self, interface, **kwargs):
        Canvas.__init__(self, interface.windows, **kwargs)

        self.lang = interface.lang

        self.snap_win = 0
        self.category = StringVar()
        self.name = StringVar()
        self.description = StringVar()
        self.desc_text = 0

        self.frame_row = 0
        self.frame_column = 0

        Label(self, text=self.lang['No file loaded, Menu Skeleton->Open File']).grid(column=0, row=0, pady=2, padx=5, sticky=W)

    def tw_click(self):
        if self.tw_state:
            self.tw_inter_lf_cv.pack_forget()
            self.tw_state = 0
        else:
            self.tw_inter_lf_cv.pack(expand=True, fill=X, pady=5, padx=10, anchor="w")
            self.tw_state = 1

    def interactive_update(self, name_file):
        for obj in self.winfo_children():
            obj.destroy()

        frame_interactive = Canvas(self)
        if not g.skeleton_memory == {}:
            controllers = g.skeleton_memory.get('controller')
            motorgroups = g.skeleton_memory.get('motorgroups')
            nbre_mg = 0
            nbre_ctr = 0
            frame_mg = {}
            frame_ctr = {}
            bg_colors= ('#D3F8E2', '#E4C1F9', '#EDE7B1', '#A9DEF9', '#F694C1', '#ADDDCE', '#E6B655', '#CA7E8D', '#70AE98', '#F0A35E')

            for name, controller in controllers.items():
                ctr_motorgroups = controller.get('attached_motorgroups')
                for ctr_mg in ctr_motorgroups:
                    for motor in motorgroups.get(ctr_mg):
                        text_motor = "{}\n".format(motor)
                        id = g.motors_memory[motor].get('id')

                        frame_column= g.motors_memory[motor]["skeleton_position"][0]
                        frame_row = g.motors_memory[motor]["skeleton_position"][1]
                        frame_sticky = g.motors_memory[motor]["skeleton_position"][2]
                        if frame_sticky==-1: frame_sticky='W'
                        elif frame_sticky==0: frame_sticky='N'
                        elif frame_sticky==1: frame_sticky='E'
                        else: frame_sticky='N'

                        frame_text= "Offset: {}\n".format(g.motors_memory[motor]["offset"])
                        frame_text +="{}: {}\n".format(self.lang['Angle_limit'], g.motors_memory[motor]["angle_limit"])
                        frame_text +="{}: {}".format(self.lang['Default_position'], g.motors_memory[motor]["default_position"])

                        g.motors_memory[motor]['position_it'] = StringVar()
                        g.motors_memory[motor]['position_it'].set(g.motors_memory[motor]["default_position"])
                        g.motors_memory[motor]['selected'] = IntVar()
                        g.motors_memory[motor]['selected'].set(1)

                        motor_lf = LabelFrame(frame_interactive, text=text_motor, background=bg_colors[nbre_ctr])
                        Label(motor_lf, text=frame_text).grid(column=0,row=0, pady=2, padx=2, sticky=EW)
                        self.motor_sb = Spinbox(motor_lf, from_=g.motors_memory[motor]["angle_limit"][0], to=g.motors_memory[motor]["angle_limit"][1], textvariable=g.motors_memory[motor]['position_it'], command=lambda x=motor: self.position_changed(x))
                        self.motor_sb.bind("<FocusOut>",lambda event, x=motor: self.focus_changed(event,x))
                        self.motor_sb.grid(column=0,row=1, pady=2, padx=2, sticky=W)
                        motor_lf.grid(column=frame_column, row=frame_row, padx=2, pady=2, sticky=frame_sticky)
                        frame_row += 1
                    nbre_mg += 1
                nbre_ctr += 1
        else:
            Label(self, text=self.lang['No file loaded, Menu Skeleton->Open File']).grid(column=0, row=0, pady=2, padx=5,sticky=W)
        for r in range(frame_interactive.grid_size()[0]):
            frame_interactive.columnconfigure(r, minsize=50)
        frame_interactive.grid(column=0, row=0, padx=5, pady=5)

    def position_changed(self, motor):
        if g.write_realtime.get() == 1:
            value= int(g.motors_memory[motor]['position_it'].get())
            try:
                g.motors_memory[motor]['engine'].set_positionCurrent(value)
            except Exception as e:
                if g.catch_exception.get() == 1:
                    print('\033[31m {}'.format(type(e)))
                    print('{} \033[0m'.format(str(e)))
                else:
                    print('\033[31m {} \033[0m'.format(self.lang['Problem when sending the order']))

    def focus_changed(self,event,motor):
        self.position_changed( motor)

    def change_all(self):
        print("Interface -> Robot: {}".format(self.lang['update all motors']))
        for motor in g.motors_memory:
            value= int(g.motors_memory[motor]['position_it'].get())
            try:
                g.motors_memory[motor]['engine'].set_positionCurrent(value)
            except Exception as e:
                if g.catch_exception.get() == 1:
                    print('\033[31m {}'.format(type(e)))
                    print('{} \033[0m'.format(str(e)))
                else:
                    print('\033[31m {}: {} \033[0m'.format(motor, self.lang['Problem when sending the order']))

    def test(self, category):
        self.category.set(category)

    def snapshot(self):
        try:
            self.snap_win= Toplevel(self)
            self.snap_win.title(self.lang['SnapShot Position'])
            frame_row = 0

            check_cv= Canvas(self.snap_win)
            for motor in g.motors_memory:
                Checkbutton(check_cv, text=motor, variable= g.motors_memory[motor]['selected']).grid(column=0, row=frame_row, sticky=W)
                Label(check_cv,text=g.motors_memory[motor]['position_it'].get()).grid(column=1, row=frame_row, sticky=W)
                frame_row+=1
            check_cv.grid(column=0, row=0, padx=3, pady=3, sticky=W)

            cat_cv= Canvas(self.snap_win)
            self.category.set(g.interface_category)
            self.name.set(g.interface_name)
            Label(cat_cv, text='{} :'.format(self.lang['Category'])).grid(column=0, row=0, sticky=E)
            Entry(cat_cv, textvariable= self.category, width= 20).grid(column=1, row=0, sticky=W)
            Label(cat_cv, text='{} :'.format(self.lang['Name'])).grid(column=0, row=1, sticky=E)
            Entry(cat_cv, textvariable= self.name, width= 20).grid(column=1, row=1, sticky=W)
            cat_cv.grid(column=0,row=1, padx=3, pady=3, sticky=W)

            description_cv= Canvas(self.snap_win)
            Label(description_cv, text=self.lang['Description']).grid(column=0, row=0, sticky=EW)
            self.desc_text= Text(description_cv, wrap='word', width=39, height=5)
            self.desc_text.insert(END, g.interface_description)
            self.desc_text.grid(column=0, row=1, sticky=E)
            description_cv.grid(column=0,row=2, padx=3, pady=3, sticky=W)

            Button(self.snap_win,text=self.lang['Save'],command=self.snapshot_save).grid(column=0,row=3, padx=3, pady=3, sticky=NW)

        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Error while generating the Snapshot window']))

    def snapshot_save(self):
        try:
            dict2json = {}
            dict2json['category']= self.category.get()
            g.interface_category = dict2json['category']
            dict2json['name']= self.name.get()
            g.interface_name = dict2json['name']
            dict2json['description']= "{}".format(self.desc_text.get('1.0', END))
            g.interface_description = dict2json['description']
            self.description.set(self.desc_text.get('1.0', END))

            if dict2json['category']!='' and dict2json['name']!='':
                dict2json['motors']={}
                for motor in g.motors_memory:
                    if g.motors_memory[motor]['selected'].get() == 1:
                        dict2json['motors'][motor]= g.motors_memory[motor]['position_it'].get()

                f = asksaveasfilename(title=self.lang['Save position'], initialfile="{}_{}.pos".format(dict2json['category'], dict2json['name']), defaultextension='.pos', filetypes=[('Position files', '.pos'), ('All files', '.*')])
                if f is None or f=='':
                    pass
                else:
                    with open(f, 'w') as fp:
                        json.dump(dict2json, fp, indent=2)

                category = dict2json['category']
                name = '{}_{}'.format(dict2json['category'],dict2json['name'])
                description = dict2json['description']
                n_motor = len(dict2json['motors'])
                g.position_memory[name] = dict2json
                g.position_memory[name]['file'] = f

                if not g.position_tree.exists(category):
                    g.position_tree.insert('', 'end', category, text=category)
                insert_id= g.position_tree.insert(category, 'end', text=name, values="{} {}".format(n_motor, description[0:30]))
                g.position_tree.see(insert_id)
            else:
                showerror(self.lang['Error'], self.lang['Category and Name must not be empty'])
            self.snap_win.destroy()

        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Cancel or Error in file management']))
