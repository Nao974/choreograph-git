from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk  # pip install pillow

import constants as g

class Frame_Tracker(LabelFrame):
    def __init__(self, interface, **kwargs):
        Canvas.__init__(self, interface.windows, **kwargs)
        self. n_row = 16
        #self.action = 1
        self.frame_row = 0
        self.frame_column = 0
        self.mboxe_list = {}
        self.motor_af = {}
        self.motor_bf = {}
        self.motor_val = {}

        Label(self, text="No file loaded, Menu Skeleton->Open File").grid(column=0, row=0, pady=2, padx=5, sticky=W)

    def tracker_update(self):
        for obj in self.winfo_children():
            obj.destroy()

        frame_tracker = Canvas(self)
        if not g.skeleton_memory == {}:
            frame_rows= LabelFrame(frame_tracker, text="Time")
            frame_row= LabelFrame(frame_rows, text="Row")
            self.col_number_af = tk.Text(frame_row, height=self.n_row, width=3)
            self.val_number = tk.Text(frame_row, height=1, width=3, bg='orange')
            self.val_number.insert(END, '000')
            self.col_number_bf = tk.Text(frame_row, height=self.n_row, width=3)
            i = 1
            while i <= self.n_row:
                self.col_number_bf.insert(tk.END, '{:03d}\n'.format(i))
                self.col_number_af.insert(tk.END, "\n")
                i += 1
            self.col_number_af.grid(column=0, row=3, sticky=N)
            self.val_number.grid(column=0, row=4, sticky=N)
            self.col_number_bf.grid(column=0, row=5, sticky=N)
            frame_row.grid(column=0, row=0, padx=2, pady=5, sticky=NW)
            frame_rows.grid(column=self.frame_column, row=self.frame_row, padx=2, pady=5, sticky=NW)
            self.frame_column += 1

            controllers = g.skeleton_memory.get('controller')
            motorgroups = g.skeleton_memory.get('motorgroups')
            motors = g.skeleton_memory.get('motors')
            nbre_mg = 0
            nbre_ctr = 0
            nbre_motor = 0
            frame_mg = {}
            frame_ctr = {}
            motor = {}

            for name, controller in controllers.items():
                frame_ctr[nbre_ctr] = LabelFrame(frame_tracker, text="{}".format(name))
                text_mcard = "{}\n".format(name)
                for cle, value in controller.items():
                    text_mcard += "{}: {}\n".format(cle, value)

                ctr_motorgroups = controller.get('attached_motorgroups')
                frame_col = 0
                for ctr_mg in ctr_motorgroups:
                    frame_mg[nbre_mg] = LabelFrame(frame_ctr[nbre_ctr], text="MG_{}".format(ctr_mg))
                    frame_mg[nbre_mg].grid(column=frame_col, row=0, padx=2, pady=5, sticky=E)
                    frame_col += 1
                    mg_col = 0
                    for mboxe in motorgroups.get(ctr_mg):
                        text_motor = "{}\n".format(mboxe)
                        id = motors[mboxe].get('id')
                        motor[id] = Label(frame_mg[nbre_mg], text=text_motor)#  .grid(column=1, row=2, sticky=W)
                        self.motor_bf[id] = tk.Text(frame_mg[nbre_mg], height=self.n_row, width=4)
                        self.motor_af[id] = tk.Text(frame_mg[nbre_mg], height=self.n_row, width=4)
                        self.motor_val[id]= tk.Text(frame_mg[nbre_mg], height=1, width=4, bg='orange')
                        self.motor_val[id].insert(END, '----')

                        i = 1
                        while i <= self.n_row:
                            self.motor_bf[id].insert(tk.END, '----\n')
                            self.motor_af[id].insert(tk.END, "\n")

                            i += 1
                        self.motor_af[id].grid(column=mg_col, row=3, sticky=N)
                        self.motor_val[id].grid(column=mg_col, row=4, sticky=N)
                        self.motor_bf[id].grid(column=mg_col, row=5, sticky=N)
                        mg_col += 1
                        nbre_motor += 1
                    nbre_mg += 1
                frame_ctr[nbre_ctr].grid(column=self.frame_column, row=self.frame_row, padx=2, pady=5, sticky=NW)
                nbre_ctr += 1
                self.frame_column += 1
        else:
            Label(self, text="No file loaded, Menu Skeleton->Open File").grid(column=0, row=0, pady=2, padx=5, sticky=W)
        frame_tracker.grid(column=0, row=0, padx=2, pady=5, sticky=W)

        frame_play = LabelFrame(self)
        im_play = Image.open('images/b_play.png').resize((32, 32), Image.ANTIALIAS)
        imh_play = ImageTk.PhotoImage(im_play)
        im_pause = Image.open('images/b_pause.png').resize((32, 32), Image.ANTIALIAS)
        imh_pause = ImageTk.PhotoImage(im_pause)
        im_forward = Image.open('images/b_forward.png').resize((32, 32), Image.ANTIALIAS)
        imh_forward = ImageTk.PhotoImage(im_forward)
        im_tostart = Image.open('images/b_tostart.png').resize((32, 32), Image.ANTIALIAS)
        imh_tostart = ImageTk.PhotoImage(im_tostart)
        im_toend = Image.open('images/b_toend.png').resize((32, 32), Image.ANTIALIAS)
        imh_toend = ImageTk.PhotoImage(im_toend)
        im_delete = Image.open('images/b_delete.png').resize((32, 32), Image.ANTIALIAS)
        imh_delete = ImageTk.PhotoImage(im_delete)
        im_read = Image.open('images/b_read.png').resize((32, 32), Image.ANTIALIAS)
        imh_read = ImageTk.PhotoImage(im_read)
        im_loop = Image.open('images/b_loop.png').resize((32, 32), Image.ANTIALIAS)
        imh_loop = ImageTk.PhotoImage(im_loop)

        button_pause = Button(frame_play, text="Pause", image=imh_pause,command=self.play)
        button_pause.grid(column=1, row=0, pady=2, padx=5, sticky=W)
        button_pause.image = imh_pause

        button_play = Button(frame_play, text="Play", image=imh_play,command=self.play)
        button_play.grid(column=2, row=0, pady=2, padx=5, sticky=W)
        button_play.image = imh_play

        button_forward = Button(frame_play, text="Forward", image=imh_forward,command=self.play)
        button_forward.grid(column=3, row=0, pady=2, padx=5, sticky=W)
        button_forward.image = imh_forward

        button_tostart = Button(frame_play, text="To Start", image=imh_tostart,command=self.tostart)
        button_tostart.grid(column=0, row=0, pady=2, padx=5, sticky=W)
        button_tostart.image = imh_tostart

        button_toend = Button(frame_play, text="To End", image=imh_toend,command=self.play)
        button_toend.grid(column=4, row=0, pady=2, padx=5, sticky=W)
        button_toend.image = imh_toend

        button_delete = Button(frame_play, text="Delete", image=imh_delete, command=self.play)
        button_delete.grid(column=1, row=1, pady=2, padx=5, sticky=W)
        button_delete.image = imh_delete

        button_read = Button(frame_play, text="Read", image=imh_read, command=self.play)
        button_read.grid(column=2, row=1, pady=2, padx=5, sticky=W)
        button_read.image = imh_read

        button_loop = Button(frame_play, text="Loop", image=imh_loop, command=self.play)
        button_loop.grid(column=3, row=1, pady=2, padx=5, sticky=W)
        button_loop.image = imh_loop

        frame_play.grid(column=0, row=1, pady=2, padx=5, sticky=W)

    def play(self):
        motors = g.g.skeleton_memory.get('motors')

        row_val_number = self.val_number.get("1.0", "1.end")
        row_col_number = self.col_number_bf.get("1.0", "1.end")
        if row_val_number != '':
            self.col_number_af.delete("1.0", "1.end")
            self.col_number_af.insert(END, row_val_number)
            self.col_number_af.see(END)
            self.val_number.delete("1.0", "2.0")
            self.val_number.insert(END, row_col_number)
            self.col_number_bf.delete("1.0", "2.0")

            for motor in motors.items():
                id = motor[1].get('id')

                row_val_motor = self.motor_val[id].get("1.0", "1.end")
                row_col_motor = self.motor_bf[id].get("1.0", "1.end")

                self.motor_af[id].delete("1.0", "1.end")
                self.motor_af[id].insert(END, row_val_motor)
                self.motor_af[id].see(END)
                self.motor_val[id].delete("1.0", "2.0")
                self.motor_val[id].insert(END, row_col_motor)
                self.motor_bf[id].delete("1.0", "2.0")

            self.after(1000, self.play)

    def tostart(self):
        self.tracker_update()
