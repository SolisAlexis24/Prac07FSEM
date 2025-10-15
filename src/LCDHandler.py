#! /usr/bin/env python3

from temperature import get_temperature
import lcd
from time import sleep
import sys
import threading
import subprocess as sp

NAMES = "Solis"
DELAY_TEMP_S = 1.00
DELAY_MSG_S = 0.60
showingCelsius = False
showingFahrenheit = False
mutex = threading.Lock()
LCD = lcd.display(lcd.LCD_ADDR, lcd.I2C_BUS)


def beginLCD():
	threading.Thread(target=updateTempLCD, daemon=True).start()
	threading.Thread(target=LmarqueeText,args=(NAMES,), daemon=True).start()

def updateSpeed(delay):
	global DELAY_MSG_S
	DELAY_MSG_S = delay

def updateUnits(CelsiusState, Fahrenheitstate):
	global showingCelsius, showingFahrenheit
	showingCelsius = CelsiusState
	showingFahrenheit = Fahrenheitstate

# Proceso que imprime la temperatua cada X tiempo
def updateTempLCD():
	global showingCelsius, showingFahrenheit, LCD
	while True:
		temp = get_temperature()
		firstClearCelsius = True
		firstClearFahrenheit = True
		firstRenderCUnits = True
		firstRenderFUnits = True
		if temp == None:
			continue
		with mutex:
			if showingCelsius:
				LCD.setCursor(0,lcd.SECOND_ROW)
				LCD.printText(format(temp, ".2f"))
				firstClearCelsius = True
				if firstRenderCUnits:
					LCD.printTempUnits(lcd.CELSIUS)
					firstRenderCUnits = False
			elif firstClearCelsius:
				LCD.clearRangeRow(lcd.SECOND_ROW, 0, 7)
				firstClearCelsius = False
				firstRenderCUnits = True

			if showingFahrenheit:
				LCD.setCursor(8,lcd.SECOND_ROW)
				LCD.printText(format(temp*9/5 + 32, ".2f"))
				firstClearFahrenheit = True
				if firstRenderFUnits:
					LCD.printTempUnits(lcd.FAHRENHEIT)
					FirstRenderCUnits = False

			elif firstClearFahrenheit:
				LCD.clearRangeRow(lcd.SECOND_ROW, 8, 15)
				firstClearFahrenheit = False
				FirstRenderFUnits = True

		sleep(DELAY_TEMP_S)

# Proceso que imprime mensaje animado
def LmarqueeText(msg):
	global LCD, DELAY_MSG_S
	shiftCount = 15
	msgStartIdx = 0
	msgLen = len(msg)
	while True:
		with mutex:
			# Shifting normal
			if shiftCount > 0:
				# Borra el caracter que deja como estela al desplazar
				LCD.clearRangeRow(lcd.FIRST_ROW, shiftCount + msgLen, shiftCount + msgLen + 1)
				LCD.setCursor(shiftCount, 0)
				LCD.printText(msg)
				shiftCount -= 1
			# "Ocultamiento" tras la pantalla
			elif msgStartIdx <= msgLen:
				LCD.clearRangeRow(lcd.FIRST_ROW, msgLen-msgStartIdx, msgLen-msgStartIdx+1)
				LCD.setCursor(0, 0)
				LCD.printText(msg[msgStartIdx:])
				msgStartIdx += 1
			# Reinicio
			else:
				shiftCount = 15
				msgStartIdx = 0

		sleep(DELAY_MSG_S)
