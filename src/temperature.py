#! /usr/bin/env python3
# Este archivo lee la temperatura del sensor 1-wire conectado y la despliega
# en consola aproximadamente cada segundo


import os
import sys
import re
import subprocess as sp
from time import sleep

DEVICE = "28-0b4b1b356461"
PATH = "/sys/bus/w1/devices/" + DEVICE + "/w1_slave"
CMD = ["cat", PATH]
FIVE_NUM_PATTERN = '[0-9][0-9][0-9][0-9][0-9]'


def main() -> None:
	while True:
		try:
			print(f'Temperratura: {get_temperature(): .4f} °C')
			sleep(1)
		except KeyboardInterrupt:
			print("\n")
			return


def get_temperature():
	try:
		proc = sp.run(CMD, capture_output=True, check=True, text=True)

	except sp.CalledProcessError as e:
		sys.exit(e.stderr)

	temp = float(re.findall(FIVE_NUM_PATTERN, proc.stdout)[0])*1.0E-3
	return temp if temp >= -55.0 and temp <= 150.0 else 0.0


if __name__ == '__main__':
	main()
