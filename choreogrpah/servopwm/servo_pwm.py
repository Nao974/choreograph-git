# -*- coding: utf-8 -*-
import struct
import time

import serial  # install: pip install pyserial
import constants as g


class Spwm():
    """Classe définissant le paramétrage et commande d'un servo moteur PWM"""

    version = '1.0_2019-11'
    debug = True
    reg_list = {}
    baud = 500000

    MIN_POS = 0
    MAX_POS = 180
    SERVO_INITSINGLE = 10
    SERVO_INITOFFSET = 11
    SERVO_INITSKELETON = 15
    SERVO_MOVESINGLE = 20
    SERVO_MOVETIME = 21
    SERVO_MOVESERVOS = 30
    SERVO_OSCILLATESERVOS = 31

    INPUT = 0
    OUTPUT = 1
    LOW = 0
    HIGH = 1

    def __init__(self, pin, orientation):
        self.serial = g.serial_port
        self.servoInit(pin)

        self.id_ref = {"type": int(), "size": 2, "min": 1, "max": 255}
        self.id = pin
        self.orientation = orientation
        self.versionCode_ref = {"read": 0x2B, "write": 0x3B, "type": float(), "size": 4}
        self.versionCode = 0
        self.infoConfig_ref = {"read": 0x2C, "write": 0x3C, "type": bytearray(), "size": 15}
        self.infoConfig = "A Saisir"
        self.skeletonPosition_ref = {"read": 0x2D, "write": 0x3D, "type": bytearray(), "size": 10}
        self.skeletonPosition = "???"

        self.state_ref = {"read": 0x2F, "type": bytes(), "size": 1}
        self.state_list = {0x00: "Initialisation"}
        self.state_list[0x01] = "Prêt"
        self.state_list[0x10] = "Erreur suite blocage arbre"
        self.state_list[0x11] = "Erreur > seuil Courant"
        self.state_list[0x12] = "Erreur > seuil Température"
        self.state_list[0x20] = "Errreur carte MC"
        self.state_list[0x30] = "Arrêt suite contact FW"
        self.state_list[0x35] = "Arrêt suite contact BW"
        self.state = 0x00
        self.state = ''

        self.mode_ref = {"read": 0x2E, "write": 0x3E, "type": bytes(), "size": 1, "min": 0, "max": 3}
        self.mode_list = {0: "Mode Interactif"}
        self.mode_list[1] = "Mode roue libre"
        self.mode_list[2] = "Mode PID Position"
        self.mode_list[3] = "Mode PID Vitesse"
        self.mode = 2

        self.limitBW_ref = {"read": 0x20, "write": 0x30, "type": int(), "size": 2, "min": self.MIN_POS, "max": self.MAX_POS}
        self.limitBW = self.limitBW_ref["min"]
        self.limitFW_ref = {"read": 0x21, "write": 0x31, "type": int(), "size": 2, "min": self.MIN_POS, "max": self.MAX_POS}
        self.limitFW = self.limitFW_ref["max"]
        self.offset_ref = {"read": 0x22, "write": 0x32, "type": bytes(), "size": 1, "min": -127, "max": +127}
        self.offset = 0
        self.deadBand_ref = {"read": 0x23, "write": 0x33, "type": int(), "size": 2, "min": 0, "max": 400}
        self.deadBand = self.deadBand_ref["min"]

        self.kpPunch_ref = {"read": 0x24, "write": 0x34, "type": float(), "size": 4, "min": 0, "max": 655.35}
        self.kpPunch = self.kpPunch_ref["min"]
        self.kdDumping_ref = {"read": 0x25, "write": 0x35, "type": float(), "size": 4, "min": 0, "max": 655.35}
        self.kdDumping = self.kdDumping_ref["min"]
        self.kiStretch_ref = {"read": 0x26, "write": 0x36, "type": float(), "size": 4, "min": 0, "max": 655.35}
        self.kiStretch = self.kiStretch_ref["min"]
        self.sensibility_ref = {"read": 0x27, "write": 0x37, "type": bytes(), "size": 1, "min": 0, "max": 255}
        self.sensibility = 0

        self.currentMaxSet_ref = {"read": 0x28, "write": 0x38, "type": bytes(), "size": 1, "min": 1, "max": 50}
        self.currentMaxSet = 4.0
        self.protectionGoSet_ref = {"read": 0x29, "write": 0x39, "type": bytes(), "size": 1, "min": 10, "max": 255}
        self.protectionGoSet = 20
        self.temperatureMaxSet_ref = {"read": 0x2A, "write": 0x3A, "type": bytes(), "size": 1, "min": 1, "max": 255}
        self.temperatureMaxSet = 102

        self.positionCurrent_ref = {"read": 0x40, "write": 0x50, "type": int(), "size": 2, "min": self.limitBW,
                                    "max": self.limitFW}
        self.positionCurrent = 90
        self.speedCurrent_ref = {"read": 0x41, "write": 0x51, "type": bytes(), "size": 1, "min": 0, "max": 255}
        self.speedCurrent = 0

        self.currentCurrent_ref = {"read": 0x42, "type": bytes(), "size": 1}
        self.currentCurrent = 0
        self.temperatureCurrent_ref = {"read": 0x43, "type": float(), "size": 4}
        self.temperatureCurrent = 0.0
        self.protectionCurrent_ref = {"read": 0x44, "type": bytes(), "size": 1}
        self.protectionCurrent = 0
        self.portD_ref = {"read": 0x45, "type": bytes(), "size": 1}
        self.portD = 0x00
        self.pinA2_ref = {"read": 0x46, "type": int(), "size": 2}
        self.pinA2 = 0
        self.pinA3_ref = {"read": 0x47, "type": int(), "size": 2}
        self.pinA3 = 0
        self.contactBWFW_ref = {"read": 0x48, "type": bytes(), "size": 1}
        self.contactBWFW = 0

    ############
    def serial_Last_putByte(self, output):
        if output < 128:
            self.serial.write(chr(0).encode('utf-8'))
        self.serial.write(chr(output).encode('utf-8'))

    def serial_putByte(self, value):
        self.serial.write(struct.pack('>B', value))

    def serial_putInt(self, value):
        c1, c2 = value & 255, value >> 8
        self.serial.write(struct.pack('>BB', c1, c2))

    ############

    def servoInit(self, pin):
        if g.serial_port != '':
            self.serial_putByte(self.SERVO_INITSINGLE)
            self.serial_putByte(pin)

    def servoOffset(self, pin, offset):
        self.serial_putByte(self.SERVO_INITOFFSET)
        self.serial_putByte(pin)
        offset = offset + 90
        self.serial_putByte(offset)

    def servoWrite(self, pin, pos):
        if self.orientation == 'indirect':
                pos = self.MAX_POS - pos
        self.serial_putByte(self.SERVO_MOVESINGLE)
        self.serial_putByte(pin)
        self.serial_putByte(pos)

    def fct_moveTime(self, pin, time, pos):
        if self.orientation == 'indirect':
            pos = self.MAX_POS - pos
        self.serial_putByte(self.SERVO_MOVETIME)
        self.serial_putByte(pin)
        time = int(time / 10)
        self.serial_putInt(time)
        self.serial_putByte(pos)

    def fct_moveServos(self, time, nbre, pin, pos, orientation):
        self.serial_putByte(self.SERVO_MOVESERVOS)
        if time < 10:
            time = 1
        else:
            time = int(time / 10)
        self.serial_putInt(time)
        self.serial_putByte(nbre)
        i = 0
        while i < nbre:
            if orientation[i] == 'indirect':
                pos[i] = self.MAX_POS - pos[i]
            # print('pin {}, pos {}, orientation={}'.format(pin[i], pos[i], orientation[i]))
            self.serial_putByte(pin[i])
            self.serial_putByte(pos[i])
            i += 1

    def fct_oscillateServos(self, cycle, T, nbre, pin, A, O, Ph):
        self.serial_putByte(self.SERVO_OSCILLATESERVOS)
        self.serial_putByte(cycle)
        if T <10:
            T = 1
        else:
            T = int(T / 10)
        self.serial_putInt(T)
        self.serial_putByte(nbre)

        for cle in pin:
            self.serial_putByte(pin[cle])
            self.serial_putByte(A[cle] + 90)
            self.serial_putByte(O[cle] + 90)
            self.serial_putInt(Ph[cle] + 180)

    def close(self):
        self.serial.close()

    def pinMode(self, pin, mode):
        self.serial.write(chr(self.PIN_MODE).encode('utf-8'))
        self.serial.write(chr(pin).encode('utf-8'))
        self.serial.write(chr(mode).encode('utf-8'))

    def digitalWrite(self, pin, output):
        self.serial.write(chr(self.DIGITAL_WRITE).encode('utf-8'))
        self.serial.write(chr(pin).encode('utf-8'))
        self.serial.write(chr(output).encode('utf-8'))

    def digitalRead(self, pin):
        self.serial.write(chr(self.DIGITAL_READ).encode('utf-8'))
        self.serial.write(chr(pin).encode('utf-8'))
        x = self.serial.read(1)
        return ord(x)

    def analogWrite(self, pin, output):
        self.serial.write(chr(self.ANALOG_WRITE).encode('utf-8'))
        self.serial.write(chr(pin).encode('utf-8'))
        self.serial.write(chr(output).encode('utf-8'))

    def analogRead(self, pin):
        self.serial.write(chr(self.ANALOG_READ).encode('utf-8'))
        self.serial.write(chr(pin).encode('utf-8'))
        c1 = ord(self.serial.read(1))
        c2 = ord(self.serial.read(1))
        return c1 * 0x100 + c2

    ############

    def return_vlib(self):
        return (self.version)

    def return_id(self):
        return (self.id)

    def return_positionCurrent(self):
        return (self.positionCurrent)

    def return_speedCurrent(self):
        return (self.speedCurrent)

    def return_versionCode(self):
        return (self.versionCode)

    def return_infoConfig(self):
        return (self.infoConfig)

    def return_skeletonPosition(self):
        return (self.skeletonPosition)

    def return_state(self):
        return (self.state)

    def return_mode(self):
        return (self.mode)

    def return_limitBW(self):
        return (self.limitBW)

    def return_limitFW(self):
        return (self.limitFW)

    def return_offset(self):
        return (self.offset)

    def return_deadBand(self):
        return (self.deadBand)

    def return_kpPunch(self):
        return (self.kpPunch)

    def return_kdDumping(self):
        return (self.kdDumping)

    def return_kiStretch(self):
        return (self.kiStretch)

    def return_sensibility(self):
        return (self.sensibility)

    def return_currentMaxSet(self):
        return (self.currentMaxSet)

    def return_protectionGoSet(self):
        return (self.protectionGoSet)

    def return_temperatureMaxSet(self):
        return (self.temperatureMaxSet)

    def return_currentCurrent(self):
        return (self.currentCurrent)

    def return_currentCurrent(self):
        return (self.currentCurrent)

    def return_temperatureCurrent(self):
        return (self.temperatureCurrent)

    def return_protectionCurrent(self):
        return (self.protectionCurrent)

    def return_portD(self):
        return (self.portD)

    def return_pinA2(self):
        return (self.pinA2)

    def return_pinA3(self):
        return (self.pinA3)

    def return_contactBWFW(self):
        return (self.contactBWFW)

    ############

    def get_versionCode(self):
        self.versionCode = self.versionCode

    def get_infoConfig(self):
        self.infoConfig = self.infoConfig

    def get_skeletonPosition(self):
        self.skeletonPosition = self.skeletonPosition

    def get_state(self):
        self.state = ''

    def get_mode(self):
        self.mode = self.mode

    def get_limitBW(self):
        self.limitBW = self.limitBW

    def get_limitFW(self):
        self.limitFW = self.limitFW

    def get_offset(self):
        self.offset = self.offset

    def get_deadBand(self):
        self.deadBand = self.deadBand

    def get_kpPunch(self):
        self.kpPunch = self.kpPunch

    def get_kdDumping(self):
        self.kdDumping = self.kdDumping

    def get_kiStretch(self):
        self.kiStretch = self.kiStretch

    def get_sensibility(self):
        self.sensibility = self.sensibility

    def get_currentMaxSet(self):
        self.currentMaxSet = self.currentMaxSet

    def get_protectionGoSet(self):
        self.protectionGoSet = self.protectionGoSet

    def get_temperatureMaxSet(self):
        self.temperatureMaxSet = self.temperatureMaxSet

    def get_positionCurrent(self):
        self.positionCurrent = self.positionCurrent

    def get_speedCurrent(self):
        self.speedCurrent = self.speedCurrent

    def get_currentCurrent(self):
        self.currentCurrent = self.currentCurrent

    def get_temperatureCurrent(self):
        self.temperatureCurrent = self.temperatureCurrent

    def get_protectionCurrent(self):
        self.protectionCurrent = self.protectionCurrent

    def get_portD(self):
        self.portD = self.portD

    def get_pinA2(self):
        self.pinA2 = self.pinA2

    def get_pinA3(self):
        self.pinA3 = self.pinA3

    def get_contactBWFW(self):
        self.contactBWFW = self.contactBWFW

    def get(self, adresse):
        self.id = adresse
        self.i2c = self.id
        self.get_versionCode()
        self.get_infoConfig()
        self.get_skeletonPosition()
        self.get_state()
        self.get_mode()
        self.get_limitBW()
        self.get_limitFW()
        self.get_offset()
        self.get_deadBand()
        self.get_kpPunch()
        self.get_kdDumping()
        self.get_kiStretch()
        self.get_sensibility()
        self.get_currentMaxSet()
        self.get_protectionGoSet()
        self.get_temperatureMaxSet()
        self.get_positionCurrent()
        self.get_speedCurrent()
        self.get_currentCurrent()
        self.get_temperatureCurrent()
        self.get_protectionCurrent()
        self.get_portD()
        self.get_pinA2()
        self.get_pinA3()
        self.get_contactBWFW()

    def get_realtime(self):
        self.get_state()
        self.get_positionCurrent()
        self.get_speedCurrent()
        self.get_currentCurrent()
        self.get_temperatureCurrent()
        self.get_protectionCurrent()
        self.get_portD()
        self.get_pinA2()
        self.get_pinA3()
        self.get_contactBWFW()

    ############

    def saveDico(self):
        dico = {}
        dico['id'] = self.id
        dico['versionCode'] = self.versionCode
        dico['infoConfig'] = self.infoConfig
        dico['skeletonPosition'] = self.skeletonPosition
        dico['mode'] = self.mode
        dico['limitBW'] = self.limitBW
        dico['limitFW'] = self.limitBW
        dico['offset'] = self.offset
        dico['deadBand'] = self.deadBand
        dico['kpPunch'] = self.kpPunch
        dico['kdDumping'] = self.kdDumping
        dico['kiStretch'] = self.kiStretch
        dico['sensibility'] = self.currentMaxSet
        dico['currentMaxSet'] = self.currentMaxSet
        dico['protectionGoSet'] = self.protectionGoSet
        dico['temperatureMaxSet'] = self.temperatureMaxSet
        dico['positionCurrent'] = self.positionCurrent
        dico['speedCurrent'] = self.speedCurrent
        dico['currentCurrent'] = self.currentCurrent
        dico['temperatureCurrent'] = self.temperatureCurrent
        dico['protectionCurrent'] = self.protectionCurrent
        dico['portD'] = self.portD
        dico['pinA2'] = self.pinA2
        dico['pinA3'] = self.pinA3
        dico['contactBWFW'] = self.contactBWFW

        return dico

    ############

    def loadDico(self, dico):
        self.id = dico['id']
        self.versionCode = dico['versionCode']
        self.infoConfig = dico['infoConfig']
        self.skeletonPosition = dico['skeletonPosition']
        self.mode = dico['mode']
        self.limitBW = dico['limitBW']
        self.limitBW = dico['limitFW']
        self.offset = dico['offset']
        self.deadBand = dico['deadBand']
        self.kpPunch = dico['kpPunch']
        self.kdDumping = dico['kdDumping']
        self.kiStretch = dico['kiStretch']
        self.currentMaxSet = dico['sensibility']
        self.currentMaxSet = dico['currentMaxSet']
        self.protectionGoSet = dico['protectionGoSet']
        self.temperatureMaxSet = dico['temperatureMaxSet']
        self.positionCurrent = dico['positionCurrent']
        self.speedCurrent = dico['speedCurrent']
        self.currentCurrent = dico['currentCurrent']
        self.temperatureCurrent = dico['temperatureCurrent']
        self.protectionCurrent = dico['protectionCurrent']
        self.portD = dico['portD']
        self.pinA2 = dico['pinA2']
        self.pinA3 = dico['pinA3']
        self.contactBWFW = dico['contactBWFW']

    ############

    def set_versionCode(self, value):
        return False

    def set_infoConfig(self, value):
        return False

    def set_skeletonPosition(self, value):
        self.skeletonPosition= value[0:self.skeletonPosition_ref["size"]]
        return False

    def set_mode(self, value):
        return False

    def set_limitBW(self, value):
        if value < self.limitBW_ref["min"]: value = self.limitBW_ref["min"]
        if value > self.limitBW_ref["max"]: value = self.limitBW_ref["max"]
        self.limitBW= value
        return False

    def set_limitFW(self, value):
        if value < self.limitFW_ref["min"]: value = self.limitFW_ref["min"]
        if value > self.limitFW_ref["max"]: value = self.limitFW_ref["max"]
        self.limitFW= value
        return False

    def set_offset(self, value):
        if value < self.offset_ref["min"]: value = self.offset_ref["min"]
        if value > self.offset_ref["max"]: value = self.offset_ref["max"]
        self.offset= value
        self.servoOffset(self.id, value)
        return False

    def set_deadBand(self, value):
        return False

    def set_kpPunch(self, value):
        return False

    def set_kdDumping(self, value):
        return False

    def set_kiStretch(self, value):
        return False

    def set_sensibility(self, value):
        return False

    def set_currentMaxSet(self, value):
        return False

    def set_protectionGoSet(self, value):
        return False

    def set_temperatureMaxSet(self, value):
        return False

    def set_positionCurrent(self, value):
        #value = value + self.offset
        if value < self.limitBW_ref["min"]: value = self.limitBW_ref["min"]
        if value > self.limitFW_ref["max"]: value = self.limitFW_ref["max"]
        self.servoWrite(self.id, value)
        return False

    def set_rotationBW(self):
        return False

    def set_rotationFW(self):
        return False

    def set_speedCurrent(self, value):
        return False

    def set(self):
        self.set_versionCode(self.versionCode)
        self.set_infoConfig(self.infoConfig)
        self.set_skeletonPosition(self.skeletonPosition)
        self.set_mode(self.mode)
        self.set_limitBW(self.limitBW)
        self.set_limitFW(self.limitFW)
        self.set_sensibility(self.sensibility)
        self.set_offset(self.offset)
        self.set_deadBand(self.deadBand)
        self.set_kpPunch(self.kpPunch)
        self.set_kdDumping(self.kdDumping)
        self.set_kiStretch(self.kiStretch)
        self.set_currentMaxSet(self.currentMaxSet)
        self.set_protectionGoSet(self.protectionGoSet)
        self.set_temperatureMaxSet(self.temperatureMaxSet)
        self.set_positionCurrent(self.positionCurrent)
        self.set_speedCurrent(self.speedCurrent)

    ############

    def cmd_eepromLoad(self):
        time.sleep(1)

    def cmd_eepromSave(self):
        time.sleep(1)
