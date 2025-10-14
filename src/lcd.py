#! /usr/bin/env python3


import smbus2
from time import sleep

LCD_ADDR = 0x27
I2C_BUS = 1
BLEN = 1
CELSIUS = "C"
FAHRENHEIT = "F"
KELVIN = "K"

class display():
	def __init__(self, i2cAddr, i2c_bus):
		self.addr = i2cAddr
		self.bus = smbus2.SMBus(i2c_bus)
		self.__COMMAND = False
		self.__DATA = True
		self.__DATA_FLAGS = 0x05
		self.__COMMAND_FLAGS = 0x04
		self._initLCD()

	def _initLCD(self):
		self._sendByte(0x33, self.__COMMAND)
		sleep(0.005)
		self._sendByte(0x32, self.__COMMAND)
		sleep(0.005)
		self._sendByte(0x28, self.__COMMAND)
		sleep(0.005)
		self._sendByte(0x0c, self.__COMMAND)
		sleep(0.005)
		self._sendByte(0x01, self.__COMMAND)
		sleep(0.005)


	def printText(self, text):
		for ch in text:
			self._sendByte(ord(ch), self.__DATA)


	def printTempUnits(self, units):
		self._sendByte(0xdf, self.__DATA)
		self._sendByte(ord(units), self.__DATA)

	def setCursor(self, x, y):
		pos = 0x80 + 0x40 * y + x
		self._sendByte(pos, self.__COMMAND)

	def clear(self):
		self._sendByte(0x01, self.__COMMAND)

	def _sendByte(self, byte, isData):
		if isData:
			flags = self.__DATA_FLAGS
		else:
			flags = self.__COMMAND_FLAGS

		buffer = byte & 0xf0
		buffer |= flags
		self._sendWord(buffer)
		sleep(0.002)
		buffer &= 0xfb
		self._sendWord(buffer)

		buffer = (byte & 0x0f) << 4
		buffer |= flags
		self._sendWord(buffer)
		sleep(0.002)
		buffer &= 0xfb
		self._sendWord(buffer)

	def _sendWord(self, data):
		global BLEN
		temp = data
		if BLEN == 1:
			temp |= 0x08
		else:
			temp &= 0xF7
		self.bus.write_byte(self.addr ,temp)



#def main():
#	myLCD = display(LCD_ADDR, I2C_BUS)
#	myLCD.setCursor(0,0)
#	myLCD.printText("Solis")


#if __name__ == '__main__':
#	main()
