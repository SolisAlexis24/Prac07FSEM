#! /usr/bin/env python3

from temperature import get_temperature
import lcd
from time import sleep

def main():
	LCD = lcd.display(lcd.LCD_ADDR, lcd.I2C_BUS)
	# Imprime nombres
	LCD.setCursor(0,0)
	LCD.printText("Solis Hernandez")
	# Imprime unidades (Estaticas)
	LCD.setCursor(5,1)
	LCD.printTempUnits(lcd.CELSIUS)
	# Imprime temperatura (Dinamicas)
	while True:
		LCD.setCursor(0,1)
		LCD.printText(format(get_temperature(), ".2f"))
		sleep(1)


if __name__ == '__main__':
	main()
