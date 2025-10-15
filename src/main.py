#! /usr/bin/env python3

from temperature import get_temperature
import lcd
from time import sleep
import sys
import threading
import subprocess as sp

NAMES = "Solis"
DELAY_TEMP_S = 1.00
DELAY_NAMES_S = 0.60
mutex = threading.Lock()

def main():
	global LCD
	LCD = lcd.display(lcd.LCD_ADDR, lcd.I2C_BUS)
	# Imprime unidades (Estaticas)
	LCD.setCursor(5,1)
	LCD.printTempUnits(lcd.CELSIUS)
	LCD.setCursor(13,1)
	LCD.printTempUnits(lcd.FAHRENHEIT)
	threading.Thread(target=updateTempLCD, daemon=True).start()
	threading.Thread(target=LmarqueeText,args=(NAMES,), daemon=True).start()
	while True:
		try:
			sleep(0)
		except KeyboardInterrupt:
			break

	LCD.clear()
	print("\n")


# Proceso que imprime la temperatua cada X tiempo
def updateTempLCD():
	while True:
		temp = get_temperature()
		if temp == None:
			continue
		with mutex:
			LCD.setCursor(0,1)
			LCD.printText(format(temp, ".2f"))
			LCD.setCursor(8,1)
			LCD.printText(format(temp*9/5 + 32, ".2f"))

		sleep(DELAY_TEMP_S)

# Proceso que imprime mensaje animado
def LmarqueeText(msg):
	shiftCount = 15
	msgStartIdx = 0
	msgLen = len(msg)
	while True:
		with mutex:
			# Shifting normal
			if shiftCount > 0:
				# Borra el caracter que deja como estela al desplazar
				LCD.clearFR(shiftCount + msgLen, shiftCount + msgLen + 1)
				LCD.setCursor(shiftCount, 0)
				LCD.printText(msg)
				shiftCount -= 1
			# "Ocultamiento" tras la pantalla
			elif msgStartIdx <= msgLen:
				LCD.clearFR(msgLen-msgStartIdx, msgLen-msgStartIdx+1)
				LCD.setCursor(0, 0)
				LCD.printText(msg[msgStartIdx:])
				msgStartIdx += 1
			# Reinicio
			else:
				shiftCount = 15
				msgStartIdx = 0

		sleep(DELAY_NAMES_S)


if __name__ == '__main__':
	main()
