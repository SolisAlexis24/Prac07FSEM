#! /usr/bin/env python3

from temperature import get_temperature
import lcd
from time import sleep

def main():
	global LCD
	LCD = lcd.display(lcd.LCD_ADDR, lcd.I2C_BUS)
	# Imprime nombres
	LCD.setCursor(0,0)
	LCD.printText("Solis Hernandez")
	# Imprime unidades (Estaticas)
	LCD.setCursor(5,1)
	LCD.printTempUnits(lcd.CELSIUS)
	LCD.setCursor(13,1)
	LCD.printTempUnits(lcd.FAHRENHEIT)
	# Imprime temperatura (Dinamicas)
	while True:
		try:
			temp = get_temperature()
			LCD.setCursor(0,1)
			LCD.printText(format(temp, ".2f"))
			LCD.setCursor(8,1)
			LCD.printText(format(temp*9/5 + 32, ".2f"))
			sleep(1)
		except KeyboardInterrupt:
			LCD.clear()
			print("\n")
			return


if __name__ == '__main__':
	main()
