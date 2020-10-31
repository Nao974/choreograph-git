#!/usr/bin/python
import re
# import smbus

# ===========================================================================
# from Ah_I2C Class
#   2016-08: update from Python 3
#   + ...
# ===========================================================================


class Ah_I2C(object):

  version='1.0_2016_08'

  def get_vi2c(self):
    return self.version
  
  @staticmethod
  def getPiRevision():
    "Gets the version number of the Raspberry Pi board"
    return 2

  @staticmethod
  def getPiI2CBusNumber():
    # Gets the I2C bus number /dev/i2c#
    return 1 if Ah_I2C.getPiRevision() > 1 else 0

  def __init__(self, address, busnum=-1, debug=False):
    self.address = address
    # By default, the correct I2C bus is auto-detected using /proc/cpuinfo
    # Alternatively, you can hard-code the bus version below:
    # self.bus = smbus.SMBus(0); # Force I2C0 (early 256MB Pi's)
    # self.bus = smbus.SMBus(1); # Force I2C1 (512MB Pi's)
    self.bus = Ah_I2C.getPiI2CBusNumber()
    self.debug = debug
    
  def reverseByteOrder(self, data):
    "Reverses the byte order of an int (16-bit) or long (32-bit) value"
    # Courtesy Vishal Sapre
    byteCount = len(hex(data)[2:].replace('L','')[::2])
    val       = 0
    for i in range(byteCount):
      val    = (val << 8) | (data & 0xff)
      data >>= 8
    return val

  def errMsg(self,reg=0x00):
    print ("Error accessing address: 0x%02X, reg: 0x%02X-%s" % (self.address, reg, self.reg_list[reg]))
    return False

  def write8(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    return False

  def write16(self, reg, value):
    "Writes a 16-bit value to the specified register/address pair"
    return False

  def writeRaw8(self, value):
    "Writes an 8-bit value on the bus"
    return False

  def writeList(self, reg, list):
    "Writes an array of bytes using I2C format"
    return False

  def readList(self, reg, length):
    "Read a list of bytes from the I2C device"
    sData = bytearray(length)
    i = 0
    while i < length:
      sData[i] = 0
      i += 1

    return (sData, False)

  def readU8(self, reg):
    "Read an unsigned byte from the I2C device"
    return (0,False)

  def readU8_Test(self, reg):
    return (1)

  def readS8(self, reg):
    "Reads a signed byte from the I2C device"
    return (0,False)

  def readU16(self, reg, little_endian=True):
    return (0,False)

  def readS16(self, reg, little_endian=True):
    return (0, False)

if __name__ == '__main__':
  try:
    bus = Ah_I2C(address=0)
    print ("Default I2C bus is accessible")
  except:
    print ("Error accessing default I2C bus")
