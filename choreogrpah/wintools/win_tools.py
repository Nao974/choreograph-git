from tkinter import *
import common.constants as g

class win_tools(Toplevel):
    def __init__(self, interface, **kwargs):
        Toplevel.__init__(self, **kwargs)

        self.lang = interface.lang

        self.title(self.lang['Tools'])
        self.lf_write_robot = LabelFrame(self, text=self.lang['Write -> Robot'])
        self.lf_read_robot = LabelFrame(self, text=self.lang['Read <- Robot'])
        self.lf_interactive_to = LabelFrame(self, text=self.lang['Interactive -> ...'])
        self.lf_setting = LabelFrame(self, text=self.lang['Settings'])
        self.state = {}

        g.write_realtime = IntVar()
        g.write_realtime.set(1)  # 1 pour cochée // 0 décochée

        self.state['write_robot'] = 0
        Button(self.lf_write_robot, text=self.lang['Show / Hide'], command= lambda x='write_robot': self.show_hide(x)).pack(anchor="w")
        self.cv_write_robot = Canvas(self.lf_write_robot)
        Checkbutton(self.cv_write_robot, text=self.lang['Real-Time Interface Writing'], variable=g.write_realtime, command= self.check_realtime).pack(anchor="w")
        self.cv_torobot_bt = Button(self.cv_write_robot, text=self.lang['Interface -> Robot'], state=DISABLED, command=interface.tab_interactive.change_all)
        self.cv_torobot_bt.pack(anchor="w")

        self.state['read_robot'] = 0
        Button(self.lf_read_robot, text=self.lang['Show / Hide'], command= lambda x='read_robot': self.show_hide(x)).pack(anchor="w")
        self.cv_read_robot = Canvas(self.lf_read_robot)
        Button(self.cv_read_robot, text=self.lang['Interface <- Robot']).pack(anchor="w")

        self.state['interactive_to'] = 0
        Button(self.lf_interactive_to, text=self.lang['Show / Hide'], command= lambda x='interactive_to': self.show_hide(x)).pack(anchor="w")
        self.cv_interactive_to = Canvas(self.lf_interactive_to)
        Button(self.cv_interactive_to, text=self.lang['SnapShot Position'], command=interface.tab_interactive.snapshot).pack(pady=2, anchor="w")

        self.state['setting'] = 0
        Button(self.lf_setting, text=self.lang['Show / Hide'], command= lambda x='setting': self.show_hide(x)).pack(anchor="w")
        self.cv_setting = Canvas(self.lf_setting)
        Checkbutton(self.cv_setting, text=self.lang["Connect Controller"], variable=g.connect_controller, command=self.check_controller).pack(anchor="w")
        Checkbutton(self.cv_setting, text=self.lang["Check Motor"], variable=g.check_motor, command=self.check_motor).pack(anchor="w")
        Checkbutton(self.cv_setting, text=self.lang["Update Engine at Loading"], variable=g.update_engine, command=self.check_engine).pack(anchor="w")
        Checkbutton(self.cv_setting, text=self.lang['catch exceptions'], variable=g.catch_exception).pack(anchor="w")

        self.lf_write_robot.pack(anchor="nw", expand=True, fill=X)
        self.lf_read_robot.pack(anchor="nw", expand=True, fill=X)
        self.lf_interactive_to.pack(anchor="nw", expand=True, fill=X)
        self.lf_setting.pack(anchor="nw", expand=True, fill=X)
        self.show_hide('all')

    def show_hide(self, x):
        if x == 'write_robot' or x == 'all':
            if self.state['write_robot']:
                self.cv_write_robot.pack_forget()
                self.state['write_robot'] = 0
            else:
                self.cv_write_robot.pack(expand=True, fill=X, pady=5, padx=10, anchor="w")
                self.state['write_robot'] = 1

        if x == 'read_robot' or x == 'all':
            if self.state['read_robot']:
                self.cv_read_robot.pack_forget()
                self.state['read_robot'] = 0
            else:
                self.cv_read_robot.pack(expand=True, fill=X, pady=5, padx=10, anchor="w")
                self.state['read_robot'] = 1

        if x == 'interactive_to' or x == 'all':
            if self.state['interactive_to']:
                self.cv_interactive_to.pack_forget()
                self.state['interactive_to'] = 0
            else:
                self.cv_interactive_to.pack(expand=True, fill=X, pady=5, padx=10, anchor="w")
                self.state['interactive_to'] = 1

        if x == 'setting' or x == 'all':
            if self.state['setting']:
                self.cv_setting.pack_forget()
                self.state['setting'] = 0
            else:
                self.cv_setting.pack(expand=True, fill=X, pady=5, padx=10, anchor="w")
                self.state['setting'] = 1

    def check_realtime(self):
        if g.write_realtime.get() == 1:
            self.cv_torobot_bt.config(state=DISABLED)
        else:
            self.cv_torobot_bt.config(state=NORMAL)

    def check_controller(self):
        if g.connect_controller.get() == 0:
            g.check_motor.set(0)
            g.update_engine.set(0)

    def check_motor(self):
        if g.check_motor.get() == 1:
            g.connect_controller.set(1)
        else:
            g.update_engine.set(0)

    def check_engine(self):
        if g.update_engine.get() == 1:
            g.check_motor.set(1)
            g.connect_controller.set(1)

