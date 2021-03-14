from tkinter.messagebox import *
from tkinter import *

# from _mboxe.interface import *
# from servoserial.interface import *
import common.constants as g

from servomboxe.mboxe_dummy import *
from servopwm.servo_pwm import *
from servoserial.servo_serial_dummy import *

from PIL import Image, ImageTk  # pip install pillow

class Frame_Skeleton(Canvas):
    def __init__(self, interface, **kwargs):
        Canvas.__init__(self, interface.windows, **kwargs)

        self.interface = interface
        self.frame_row = 0
        self.frame_column = 0
        self.lang = interface.lang

        Label(self, text=self.lang['No file loaded, Menu Skeleton->Open File']).grid(column=0, row=0, pady=2, padx=5, sticky=W)

    def skeleton_update(self, name_file):
        for obj in self.winfo_children():
            obj.destroy()

        frame_skeleton = Canvas(self)

        if not g.skeleton_memory == {}:
            Label(frame_skeleton, text="{}: {}".format(self.lang['File'], name_file)).grid(column=self.frame_column, row=self.frame_row, pady=2, padx=5, sticky=W)
            self.frame_row += 1
            imh = {}
            imh['pi'] = ImageTk.PhotoImage(Image.open('choreograph/images/pi.png'))
            imh['pi_b'] = ImageTk.PhotoImage(Image.open('choreograph/images/pi_b.png'))
            imh['pi_3'] = ImageTk.PhotoImage(Image.open('choreograph/images/pi_3.png'))
            imh['pi_4'] = ImageTk.PhotoImage(Image.open('choreograph/images/pi_4.png'))
            imh['arduino'] = ImageTk.PhotoImage(Image.open('choreograph/images/arduino.png'))
            imh['arduino_nano'] = ImageTk.PhotoImage(Image.open('choreograph/images/arduino_nano.png'))
            imh['arduino_uno'] = ImageTk.PhotoImage(Image.open('choreograph/images/arduino_uno.png'))
            imh['arduino_mega'] = ImageTk.PhotoImage(Image.open('choreograph/images/arduino_mega.png'))
            imh['servo_pwm'] = ImageTk.PhotoImage(Image.open('choreograph/images/servo_pwm.png'))
            imh['servo_serial'] = ImageTk.PhotoImage(Image.open('choreograph/images/servo_serial.png'))
            imh['mboxe_a'] = ImageTk.PhotoImage(Image.open('choreograph/images/mboxe.png'))
            imh['mboxe_b'] = ImageTk.PhotoImage(Image.open('choreograph/images/mboxe.png'))
            imh['servo_pwm'] = ImageTk.PhotoImage(Image.open('choreograph/images/servo_pwm.png'))

            g.controllers_memory = g.skeleton_memory.get('controller')
            motorgroups = g.skeleton_memory.get('motorgroups')
            g.motors_memory = g.skeleton_memory.get('motors')
            nbre_mg = 0
            nbre_ctr = 0
            frame_mg = {}
            frame_ctr = {}

            for name, controller in g.controllers_memory.items():
                frame_ctr[nbre_ctr] = LabelFrame(frame_skeleton, text="{}".format(name))
                ctr_row = 0
                ctr_column = 0
                text_mcard = "{}\n".format(name)
                for cle, value in controller.items():
                    text_mcard += "{}: {}\n".format(cle, value)
                imh_mcard = imh[controller['type']]
                if 'mg_alignment' not in controller:
                    controller['mg_alignment'] = 'v'
                g.controllers_memory[name]['state']= ''

                if g.connect_controller.get() == 1:
                    if controller['connection'] == 'serial':
                        if g.serial_port != '':
                            g.serial_port.close()
                        try:
                            g.serial_port = serial.Serial(controller['address'][0], baudrate=controller['address'][1])
                            c_recu = g.serial_port.read(1)
                            while ord(c_recu) != 0:
                                c_recu = g.serial_port.read(1)
                            c_recu = g.serial_port.read(1)
                            while ord(c_recu) != 255:
                                c_recu = g.serial_port.read(1)
                            c_recu = g.serial_port.read(1)
                            while ord(c_recu) != 0:
                                c_recu = g.serial_port.read(1)
                            g.controllers_memory[name]['state'] = 1
                        except:
                            g.controllers_memory[name]['state'] = 0
                            g.serial_port = ''
                        print("{} {}: {}= {}".format(self.lang['Connect Controller to'], controller['connection'], self.lang['state'], g.controllers_memory[name]['state']))

                bt_mcard = Button(frame_ctr[nbre_ctr], text=text_mcard, command= lambda x=name: self.win_controller(x),
                                  fg=g.state_colors[g.controllers_memory[name]['state']][0],
                                  background=g.state_colors[g.controllers_memory[name]['state']][1],
                                  image=imh_mcard, compound=LEFT, anchor=W, justify=LEFT, padx=5)
                bt_mcard.grid(column=ctr_column, row=ctr_row, padx=2, pady=5)
                bt_mcard.image = imh_mcard
                ctr_row += 1

                ctr_motorgroups = controller.get('attached_motorgroups')
                for ctr_mg in ctr_motorgroups:
                    mg_row = 0
                    mg_column = 0
                    frame_mg[nbre_mg] = LabelFrame(frame_ctr[nbre_ctr], text="MG_{}".format(ctr_mg))
                    frame_mg[nbre_mg].grid(column=ctr_column, columnspan=2, row=ctr_row, padx=2, pady=5, sticky=E)
                    if controller['mg_alignment'] == 'h':
                        ctr_column += 2
                    else:
                        ctr_row += 1
                    for motor in motorgroups.get(ctr_mg):
                        text_motor = "{}\n".format(motor)
                        for cle, value in g.motors_memory[motor].items():
                            text_motor += "{}: {}\n".format(cle, value)
                        id = g.motors_memory[motor].get('id')
                        imh_mboxe= imh[g.motors_memory[motor].get('type')]

                        if 'mboxe' in g.motors_memory[motor].get('type'):
                            g.motors_memory[motor]['engine'] = Mboxe(id)
                        elif 'serial' in g.motors_memory[motor].get('type'):
                            g.motors_memory[motor]['engine'] = Sserial(id)
                        else:
                            g.motors_memory[motor]['engine'] = Spwm(id, g.motors_memory[motor].get('orientation'))

                        g.motors_memory[motor]['state'] = ''
                        if g.check_motor.get() == 1 and g.motors_memory[motor]['type'] != 'servo_pwm':
                            g.motors_memory[motor]['engine'].get(id)
                            g.motors_memory[motor]['state'] = g.motors_memory[motor]['engine'].return_state()
                            print("{} {}, id={}: {}={}".format(self.lang['Search Engine'], motor, g.motors_memory[motor]['engine'].return_id(), self.lang['state'], g.motors_memory[motor]['state']))

                        if g.update_engine.get() == 1:
                            print("{} {}:".format(self.lang['For Engine'], motor))
                            if g.motors_memory[motor]['offset'] != g.motors_memory[motor]['engine'].return_offset():
                                g.motors_memory[motor]['engine'].set_offset(g.motors_memory[motor]['offset'])
                                print("  -> {} offset= {}".format(self.lang['Update'], g.motors_memory[motor]['engine'].return_offset()))
                            if g.motors_memory[motor]['angle_limit'][0] != g.motors_memory[motor]['engine'].return_limitBW():
                                g.motors_memory[motor]['engine'].set_limitBW(g.motors_memory[motor]['angle_limit'][0])
                                print("  -> {} limitBW= {}".format(self.lang['Update'],g.motors_memory[motor]['engine'].return_limitBW()))
                            if g.motors_memory[motor]['angle_limit'][1] != g.motors_memory[motor]['engine'].return_limitFW():
                                g.motors_memory[motor]['engine'].set_limitFW(g.motors_memory[motor]['angle_limit'][1])
                                print("  -> {} limitFW= {}".format(self.lang['Update'],g.motors_memory[motor]['engine'].return_limitFW()))
                            if "{}".format(g.motors_memory[motor]['skeleton_position']) != g.motors_memory[motor]['engine'].return_skeletonPosition():
                                g.motors_memory[motor]['engine'].set_skeletonPosition("{}".format(g.motors_memory[motor]['skeleton_position']))
                                print("  -> {} SkeletonPosition= {}".format(self.lang['Update'], g.motors_memory[motor]['engine'].return_skeletonPosition()))
                            print("  -> {}= {}".format(self.lang['Set to default Position'], g.motors_memory[motor]['default_position']))
                            g.motors_memory[motor]['engine'].set_positionCurrent(g.motors_memory[motor]['default_position'])
                        g.motors_memory[motor]['button'] = Button(frame_mg[nbre_mg], text=text_motor,
                                                                  fg=g.state_colors[g.motors_memory[motor]['state']][0],
                                                                  background=g.state_colors[g.motors_memory[motor]['state']][1],
                                                                  command=lambda x=g.motors_memory[motor]: self.win_mboxe(x),
                                                                  image=imh_mboxe, anchor=W, justify=LEFT)

                        g.motors_memory[motor]['button'].image = imh_mboxe
                        g.motors_memory[motor]['button']['compound'] = LEFT
                        g.motors_memory[motor]['button'].grid(column=mg_column, row=mg_row, padx=2, pady=5, sticky=W)
                        mg_row += 1
                    nbre_mg += 1
                frame_ctr[nbre_ctr].grid(column=self.frame_column, row=self.frame_row, padx=2, pady=5, sticky=NW)
                nbre_ctr += 1

                self.frame_column += 1

        else:
            Label(self, text=self.lang['No file loaded, Menu Skeleton->Open File']).grid(column=0, row=0, pady=2, padx=5, sticky=W)

      
        defilY = Scrollbar(self, orient='vertical')
        defilY.grid(column=0, row=0, sticky='ns')   
        frame_skeleton.grid(column=1, row=0, padx=2, pady=5)
        frame_skeleton.configure(yscrollcommand =defilY.set)
        defilY.configure(command=frame_skeleton.yview)
        frame_skeleton.configure(scrollregion=frame_skeleton.bbox(ALL))

    def win_controller(self, controller):
        wincontroller= Toplevel()
        wincontroller.geometry("450x45")
        wincontroller.title("{}: {}".format(self.lang['Controller'], controller))
        Button(wincontroller, text="blablabla", ).grid(column=0, row=0, padx=2, pady=5, sticky=NW)

    def win_mboxe(self, motor):
        if 'mboxe' in motor['type']:
            if g.check_motor.get() == 1 and motor['engine'].return_state() == 0:
                showerror('{}'.format(self.lang['Error']), '{}'.format(self.lang['State Engine is down']))
            else:
                winmboxe = Toplevel()
                winmboxe.title("Mboxe: {}".format(motor['id']))
                mboxe_manager(winmboxe, motor['engine'], self.interface.lang)
        elif 'serial' in motor['type']:
            if g.check_motor.get() == 1 and motor['engine'].return_state() == 0:
                showerror('{}'.format(self.lang['Error']), '{}'.format(self.lang['State Engine is down']))
            else:
                winmboxe = Toplevel()
                winmboxe.title("Serial Servo: {}".format(motor['id']))
                serial_manager(winmboxe, motor['engine'], self.interface.lang)
        else:
            showerror('servo_pwm', 'no option for this engine')

    def export_arduino(self):
        try:
            pin = []
            offset = []
            min = []
            max = []
            home = []
            orientation = []

            arduino_win = Toplevel()
            arduino_win.title('{} Arduino'.format(self.lang['Export to']))
            ea_text = Text(arduino_win, height=60)
            ea_text.grid(column=0, row=0, sticky=N)
            ea_text.insert(END, '#include<Servo.h>\n#include <Oscillator.h>\n#include<choregraph.h>\n\n')

            i=0
            for motor in g.skeleton_memory.get("motors"):
                ea_text.insert(END, '#define\t{}\t{}\n'.format(motor.upper(), i))
                pin.append(g.motors_memory[motor]['id'])
                offset.append(g.motors_memory[motor]['offset'])
                min.append(g.motors_memory[motor]['angle_limit'][0])
                max.append(g.motors_memory[motor]['angle_limit'][1])
                home.append(g.motors_memory[motor]['default_position'])
                orientation.append(g.motors_memory[motor]['orientation'][0])
                i+=1
            ea_text.insert(END, '\n#define\tNBRE_SERVO\t{}\n'.format(i))
            ea_text.insert(END, '#define\tMAX_POS\t180\n')

            ea_text.insert(END, '\nbyte pin[]={')
            for value in pin:
                ea_text.insert(END, '{}, '.format(value))
            ea_text.delete('end-3c', 'end')
            ea_text.insert(END, '};\n')

            ea_text.insert(END, 'byte offset[]={')
            for value in offset:
                ea_text.insert(END, '{}, '.format(value))
            ea_text.delete('end-3c', 'end')
            ea_text.insert(END, '};\n')

            ea_text.insert(END, 'byte orientation[]={')
            for value in orientation:
                ea_text.insert(END, '\'{}\', '.format(value))
            ea_text.delete('end-3c', 'end')
            ea_text.insert(END, '};\n')

            ea_text.insert(END, 'byte angle_min[]={')
            for value in min:
                ea_text.insert(END, '{}, '.format(value))
            ea_text.delete('end-3c', 'end')
            ea_text.insert(END, '};\n')

            ea_text.insert(END, 'byte angle_max[]={')
            for value in max:
                ea_text.insert(END, '{}, '.format(value))
            ea_text.delete('end-3c', 'end')
            ea_text.insert(END, '};\n')

            ea_text.insert(END, 'byte home[]={')
            for value in home:
                ea_text.insert(END, '{}, '.format(value))
            ea_text.delete('end-3c', 'end')
            ea_text.insert(END, '};\n')

            ea_text.insert(END, '\nchoregraph chore;\n')

            ea_text.insert(END, '\nvoid setup()\n{\n')
            ea_text.insert(END, ' for(int i=0; i<NBRE_SERVO; i++)\n\t{\n')
            ea_text.insert(END, '\t chore.servoInit(pin[i]);\n\t chore.servoOffset(i, offset[i]);\n\t moveSingle_safe(i, home[i]);\n')
            ea_text.insert(END, '\t}\n')
            ea_text.insert(END, '\n // put your setup code here, to run once:\n\n')
            ea_text.insert(END, '}\n')

            ea_text.insert(END, '\nvoid loop()\n{\n')
            ea_text.insert(END, ' // put your main code here, repeatedly:\n\n')
            ea_text.insert(END, '}\n')

            ea_text.insert(END, '\nvoid moveSingle_safe(byte servo_id, byte pos)\n{\n')
            ea_text.insert(END, ' if (orientation[servo_id] == \'i\')\n\tpos= MAX_POS -pos;\n')
            ea_text.insert(END, ' if (pos <= angle_max[servo_id] && pos>= angle_min[servo_id])\n\tchore.moveSingle(servo_id, pos);\n')
            ea_text.insert(END, '}\n')

            ea_text.see(END)
        except:
            print('\033[31m {} \033[0m'.format(self.lang['Error while translating the skeleton']))

    def recalculate_trim(self):
        try:
            self.trim_win= Toplevel(self)
            self.trim_win.title(self.lang['Recalculate TRIMs'])
            frame_row = 0

            check_cv= Canvas(self.trim_win)
            for motor in g.motors_memory:
                trim = int(g.motors_memory[motor]["default_position"]) - int(g.motors_memory[motor]['position_it'].get())
                new_offset = int(g.motors_memory[motor]["offset"]) + trim
                ckb = Checkbutton(check_cv, text=motor)
                if new_offset != g.motors_memory[motor]["offset"]:
                    ckb.toggle()
                ckb.grid(column=0, row=frame_row, sticky=W)
                Label(check_cv,text='Offset: {}'.format(g.motors_memory[motor]["offset"])).grid(column=1, row=frame_row, sticky=W)
                Label(check_cv,text='{}: {}'.format(self.lang['default position - current'], trim)).grid(column=2, row=frame_row, sticky=W)
                Label(check_cv,text='=> {} Offset: {}'.format(self.lang['New'], new_offset)).grid(column=3, row=frame_row, sticky=W)
                frame_row+=1
            check_cv.grid(column=0, row=0, padx=3, pady=3, sticky=W)
            Label(self.trim_win, text='{}'.format(self.lang['The selected engines have been modified, update your json file then menu Skeleton-> Update'])).grid(column=0,row=3, padx=3, pady=3, sticky=NW)
            # Button(self.trim_win,text=self.lang['Update Skeleton in memory'], command=self.update_trim).grid(column=0,row=3, padx=3, pady=3, sticky=NW)

        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))

    def update_trim(self):
        try:
            for motor in g.motors_memory:
                trim = int(g.motors_memory[motor]["default_position"]) - int(g.motors_memory[motor]['position_it'].get())
                new_offset = int(g.motors_memory[motor]["offset"]) + trim

                g.motors_memory[motor]["offset"] = new_offset
                g.motors_memory[motor]['engine'].set_positionCurrent(g.motors_memory[motor]["default_position"])
        except Exception as e:
            if g.catch_exception.get() == 1:
                print('\033[31m {}'.format(type(e)))
                print('{} \033[0m'.format(str(e)))
            else:
                print('\033[31m {} \033[0m'.format(self.lang['Unexpected error, check "File-> Verbose Log" for more information']))
