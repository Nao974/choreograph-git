import struct
import time
from servoserial.serial_dummy import Ah_I2C

from random import randint

# ===========================================================================
#   2019-11: creation by the copy of the class mboxe
#
# ===========================================================================

class Sserial():
    """Classe définissant le paramétrage et commande d'une M-BOXE
    voir docucment de Specification Fonctionnelle"""

    version = '1.0_2019-11'
    debug = True
    reg_list = {}
    reg_list[0x00] = 'Mode Interactif'
    reg_list[0x01] = 'Mode Roue Libre'
    reg_list[0x02] = 'PID Position'
    reg_list[0x03] = 'PID Vitesse'
    reg_list[0x10] = 'chargement Config depuis l’EEPROM'
    reg_list[0x11] = 'Enregistrement Config dans l’EEPROM'
    reg_list[0x20] = 'demande config limitBW => 2 bytes'
    reg_list[0x21] = 'demande config limitFW => 2 bytes'
    reg_list[0x22] = 'demande config offSet => 1 byte'
    reg_list[0x23] = 'demande config deadBand => 2 bytes'
    reg_list[0x24] = 'demande config kp => 4 bytes'
    reg_list[0x25] = 'demande config kd => 4 bytes'
    reg_list[0x26] = 'demande config ki => 4 bytes'
    reg_list[0x27] = 'demande config sensibility'
    reg_list[0x28] = 'demande config currentMaxSet => 1 byte'
    reg_list[0x29] = 'demande config ProtectionGoSet => 1 byte'
    reg_list[0x2A] = 'demande config temperatureMaxSet => 1 byte'
    reg_list[0x2B] = 'demande config versionCode => 4 bytes'
    reg_list[0x2C] = 'demande config infoConfig (15car) => 15 bytes'
    reg_list[0x2D] = 'demande config skeletonPosition (4car) => 4 bytes'
    reg_list[0x2E] = 'demande mode Fonctionnement <= 1 byte'
    reg_list[0x2F] = 'demande Etat => 1 byte'
    reg_list[0x30] = 'envoi config limitBW <= 2 bytes'
    reg_list[0x31] = 'envoi config limitFW <= 2 bytes'
    reg_list[0x32] = 'envoi config offSet <= 1 byte'
    reg_list[0x33] = 'envoi config deadBand <= 2 bytes'
    reg_list[0x34] = 'envoi config kp <= 4 bytes'
    reg_list[0x35] = 'envoi config kd <= 4 bytes'
    reg_list[0x36] = 'envoi config ki <= 4 bytes'
    reg_list[0x37] = 'envoi config sensibility'
    reg_list[0x38] = 'envoi config currentMaxSet <= 1 byte'
    reg_list[0x39] = 'envoi config ProtectionGoSet <= 1 byte'
    reg_list[0x3A] = 'envoi config temperatureMaxSet <= 1 byte'
    reg_list[0x3B] = 'envoi config versionCode <= 4 bytes'
    reg_list[0x3C] = 'envoi config infoConfig (15car)<= 15 bytes'
    reg_list[0x3D] = 'envoi config skeletonPosition (4 car)<= 4 bytes'
    reg_list[0x3E] = 'envoi mode Fonctionnement <= 1 byte'
    reg_list[0x40] = 'demande position <= 2 Bytes'
    reg_list[0x41] = 'demande vitesse <= 1 Byte'
    reg_list[0x42] = 'demande courant <= 1 Byte'
    reg_list[0x43] = 'demande température <= 4 bytes'
    reg_list[0x44] = 'demande protection <= 1 Byte'
    reg_list[0x45] = 'demande PORTD <= 1 Byte'
    reg_list[0x46] = 'demande valeur Analogique PINA2 <= 2 bytes'
    reg_list[0x47] = 'demande valeur Analogique PINA3 <= 2 bytes'
    reg_list[0x48] = 'demande Etat Contact BW FW <= 1 byte'
    reg_list[0x50] = 'Consigne Position => 2 bytes'
    reg_list[0x51] = 'Consigne Vitesse => 1 byte'

    def __init__(self, adresse):
        self.i2c = Ah_I2C(adresse)
        self.vi2c = self.i2c.get_vi2c()

        self.id_ref = {"type": int(), "size": 2, "min": 3, "max": 119}
        self.id = adresse
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
        self.state = randint(0,1)  #pour Dummy

        self.mode_ref = {"read": 0x2E, "write": 0x3E, "type": bytes(), "size": 1, "min": 0, "max": 3}
        self.mode_list = {0: "Mode Interactif"}
        self.mode_list[1] = "Mode roue libre"
        self.mode_list[2] = "Mode PID Position"
        self.mode_list[3] = "Mode PID Vitesse"
        self.mode = 0

        self.limitBW_ref = {"read": 0x20, "write": 0x30, "type": int(), "size": 2, "min": 0, "max": 180}
        self.limitBW = self.limitBW_ref["min"]
        self.limitFW_ref = {"read": 0x21, "write": 0x31, "type": int(), "size": 2, "min": 0, "max": 180}
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
        self.positionCurrent = int((self.limitFW-self.limitBW)/2)
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

    def i2c_test(self):
        try:
            i2c = Ah_I2C(0x00)
            version = i2c.get_vi2c()
            bus = i2c.getPiI2CBusNumber()
            return (version, bus)
        except:
            return ('?', True)

    def get_Float(self, code):
        (lstData, error) = self.i2c.readList(code, 4)
        if error: return (0, error)
        sData = bytearray(4)
        i = 0
        for aByte in lstData:
            sData[i] = aByte
            i += 1
        r_data, = struct.unpack('<f', sData)
        return (r_data, error)

    def set_Float(self, code, value):
        sData = struct.pack('<f', value)
        return (self.i2c.writeList(code, [c for c in sData]))

    def get_String(self, code, lenght):
        (lstData, error) = self.i2c.readList(code, lenght)
        sData = ''
        for aByte in lstData:
            if aByte != 0: sData = sData + chr(aByte)
        data = ''.join(sData)
        return (data, error)

    def set_String(self, code, value, lenght):
        return (self.i2c.writeList(code, [ord(c) for c in value[0:lenght]]))

    def get_UChar(self, code):
        return (self.i2c.readU8(code))

    def get_SChar(self, code):
        return (self.i2c.readS8(code))

    def set_Byte(self, code, value):
        return (self.i2c.write8(code, value))

    def get_Int(self, code):
        (lstData, error) = self.i2c.readList(code, 2)
        if error: return (0, error)
        sData = bytearray(2)
        data = 0
        i = 0
        for aByte in lstData:
            sData[i] = aByte
            i += 1
        data, = struct.unpack('<H', sData)
        return (data, error)

    def set_Int(self, code, value):
        return (self.i2c.write16(code, value))

    ############

    def get_versionCode(self):
        reg = self.versionCode_ref["read"]
        (self.versionCode, error) = self.get_Float(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_infoConfig(self):
        reg = self.infoConfig_ref["read"]
        (self.infoConfig, error) = self.get_String(reg, self.infoConfig_ref["size"])
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_skeletonPosition(self):
        reg = self.skeletonPosition_ref["read"]
        (self.skeletonPosition, error) = self.get_String(reg, self.skeletonPosition_ref["size"])
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_state(self):
        self.state = randint(0 , 1)

    def get_mode(self):
        reg = self.mode_ref["read"]
        (self.mode, error) = self.get_UChar(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_limitBW(self):
        reg = self.limitBW_ref["read"]
        (self.limitBW, error) = self.get_Int(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_limitFW(self):
        reg = self.limitFW_ref["read"]
        (self.limitFW, error) = self.get_Int(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_offset(self):
        reg = self.offset_ref["read"]
        (self.offset, error) = self.get_SChar(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_deadBand(self):
        reg = self.deadBand_ref["read"]
        (self.deadBand, error) = self.get_Int(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_kpPunch(self):
        reg = self.kpPunch_ref["read"]
        (self.kpPunch, error) = self.get_Float(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_kdDumping(self):
        reg = self.kdDumping_ref["read"]
        (self.kdDumping, error) = self.get_Float(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_kiStretch(self):
        reg = self.kiStretch_ref["read"]
        (self.kiStretch, error) = self.get_Float(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_sensibility(self):
        reg = self.currentMaxSet_ref["read"]
        (self.sensibility, error) = self.get_UChar(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_currentMaxSet(self):
        reg = self.currentMaxSet_ref["read"]
        (value, error) = self.get_UChar(reg)
        self.currentMaxSet = value / 10
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_protectionGoSet(self):
        reg = self.protectionGoSet_ref["read"]
        (self.protectionGoSet, error) = self.get_UChar(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_temperatureMaxSet(self):
        reg = self.temperatureMaxSet_ref["read"]
        (self.temperatureMaxSet, error) = self.get_UChar(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_positionCurrent(self):
        reg = self.positionCurrent_ref["read"]
        (self.positionCurrent, error) = self.get_Int(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_speedCurrent(self):
        reg = self.speedCurrent_ref["read"]
        (self.speedCurrent, error) = self.get_UChar(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_currentCurrent(self):
        reg = self.currentCurrent_ref["read"]
        (current, error) = self.get_UChar(reg)
        if current > 0:
            self.currentCurrent = current / 10
        else:
            self.currentCurrent = 0
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_temperatureCurrent(self):
        reg = self.temperatureCurrent_ref["read"]
        (self.temperatureCurrent, error) = self.get_Float(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_protectionCurrent(self):
        reg = self.protectionCurrent_ref["read"]
        (self.protectionCurrent, error) = self.get_UChar(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_portD(self):
        reg = self.portD_ref["read"]
        (self.portD, error) = self.get_UChar(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_pinA2(self):
        reg = self.pinA2_ref["read"]
        (self.pinA2, error) = self.get_Int(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_pinA3(self):
        reg = self.pinA3_ref["read"]
        (self.pinA3, error) = self.get_Int(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get_contactBWFW(self):
        reg = self.contactBWFW_ref["read"]
        (self.contactBWFW, error) = self.get_UChar(reg)
        if self.debug & error:
            print("Error reading address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))

    def get(self, adresse):
        self.id = adresse
        self.i2c = Ah_I2C(adresse)
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
        reg = self.versionCode_ref["write"]
        result = self.set_Float(reg, value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.versionCode = value
        return (result)

    def set_infoConfig(self, value):
        reg = self.infoConfig_ref["write"]
        result = self.set_String(reg, value, self.infoConfig_ref["size"])
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.infoConfig = value
        return (result)

    def set_skeletonPosition(self, value):
        reg = self.skeletonPosition_ref["write"]
        result = self.set_String(reg, value, self.skeletonPosition_ref["size"])
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.skeletonPosition = value
        return (result)

    def set_mode(self, value):
        reg = self.mode_ref["write"]
        result = True
        if value >= self.mode_ref["min"] and value <= self.mode_ref["max"]:
            result = self.set_Byte(reg, value)
            if result & self.debug:
                print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.mode = value
        return (result)

    def set_limitBW(self, value):
        reg = self.limitBW_ref["write"]
        if value < self.limitBW_ref["min"]: value = self.limitBW_ref["min"]
        if value > self.limitBW_ref["max"]: value = self.limitBW_ref["max"]
        result = self.set_Int(reg, value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.limitBW = value
        return (result)

    def set_limitFW(self, value):
        reg = self.limitFW_ref["write"]
        if value < self.limitFW_ref["min"]: value = self.limitFW_ref["min"]
        if value > self.limitFW_ref["max"]: value = self.limitFW_ref["max"]
        result = self.set_Int(reg, value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.limitFW = value
        return (result)

    def set_offset(self, value):
        reg = self.offset_ref["write"]
        if value < self.offset_ref["min"]: value = self.offset_ref["min"]
        if value > self.offset_ref["max"]: value = self.offset_ref["max"]
        result = self.set_Byte(reg, value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.offset = value
        return (result)

    def set_deadBand(self, value):
        reg = self.deadBand_ref["write"]
        if value < self.deadBand_ref["min"]: value = self.deadBand_ref["min"]
        if value > self.deadBand_ref["max"]: value = self.deadBand_ref["max"]
        result = self.set_Int(reg, value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.deadBand = value
        return (result)

    def set_kpPunch(self, value):
        reg = self.kpPunch_ref["write"]
        if value < self.kpPunch_ref["min"]: value = self.kpPunch_ref["min"]
        if value > self.kpPunch_ref["max"]: value = self.kpPunch_ref["max"]
        result = self.set_Float(reg, value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.kpPunch = value
        return (result)

    def set_kdDumping(self, value):
        reg = self.kdDumping_ref["write"]
        if value < self.kdDumping_ref["min"]: value = self.kdDumping_ref["min"]
        if value > self.kdDumping_ref["max"]: value = self.kdDumping_ref["max"]
        result = self.set_Float(reg, value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.kdDumping = value
        return (result)

    def set_kiStretch(self, value):
        reg = self.kiStretch_ref["write"]
        if value < self.kiStretch_ref["min"]: value = self.kiStretch_ref["min"]
        if value > self.kiStretch_ref["max"]: value = self.kiStretch_ref["max"]
        result = self.set_Float(reg, value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.kiStretch = value
        return (result)

    def set_sensibility(self, value):
        reg = ''
        if value < self.sensibility_ref["min"]: value = self.sensibility_ref["min"]
        if value > self.sensibility_ref["max"]: value = self.sensibility_ref["max"]
        result = self.set_Byte(self.sensibility_ref["write"], value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.sensibility = value
        return (result)

    def set_currentMaxSet(self, value):
        value = int(value * 10)
        reg = self.currentMaxSet_ref["write"]
        if value < self.currentMaxSet_ref["min"]: value = self.currentMaxSet_ref["min"]
        if value > self.currentMaxSet_ref["max"]: value = self.currentMaxSet_ref["max"]
        result = self.set_Byte(reg, value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.currentMaxSet = value
        return (result)

    def set_protectionGoSet(self, value):
        reg = ''
        if value < self.protectionGoSet_ref["min"]: value = self.protectionGoSet_ref["min"]
        if value > self.protectionGoSet_ref["max"]: value = self.protectionGoSet_ref["max"]
        result = self.set_Byte(self.protectionGoSet_ref["write"], value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.protectionGoSet = value
        return (result)

    def set_temperatureMaxSet(self, value):
        reg = ''
        if value < self.temperatureMaxSet_ref["min"]: value = self.temperatureMaxSet_ref["min"]
        if value > self.temperatureMaxSet_ref["max"]: value = self.temperatureMaxSet_ref["max"]
        result = self.set_Byte(self.temperatureMaxSet_ref["write"], value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.temperatureMaxSet = value
        return (result)

    def set_positionCurrent(self, value):
        reg = ''
        if value < self.limitBW_ref["min"]: value = self.limitBW_ref["min"]
        if value > self.limitFW_ref["max"]: value = self.limitFW_ref["max"]
        result = self.set_Int(self.positionCurrent_ref["write"], value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.positionCurrent= value
        return (result)

    def set_rotationBW(self):
        self.set_Int(self.positionCurrent_ref["write"], 5000)

    def set_rotationFW(self):
        self.set_Int(self.positionCurrent_ref["write"], -5000)

    def set_speedCurrent(self, value):
        reg = ''
        if value < self.speedCurrent_ref["min"]: value = self.speedCurrent_ref["min"]
        if value > self.speedCurrent_ref["max"]: value = self.speedCurrent_ref["max"]
        result = self.set_Byte(self.speedCurrent_ref["write"], value)
        if result & self.debug:
            print("Error writing address: %d, reg: 0x%02X-%s" % (self.id, reg, self.reg_list[reg]))
        else: self.speedCurrent = value
        return (result)

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
        self.i2c.write8(0x10, 0x01)
        time.sleep(1)

    def cmd_eepromSave(self):
        self.i2c.write8(0x11, 0x01)
        time.sleep(1)
