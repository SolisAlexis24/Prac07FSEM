#! /usr/bin/env python3
# Este archivo lee la temperatura del sensor 1-wire conectado y la despliega
# en consola aproximadamente cada segundo


import os
import sys
import re
import threading
import subprocess as sp
from time import sleep

DEVICE = "28-0b4b1b356461"
PATH = "/sys/bus/w1/devices/" + DEVICE + "/w1_slave"
CMD = ["cat", PATH]
FIVE_NUM_PATTERN = '[0-9][0-9][0-9][0-9][0-9]'
LAST_TEMPERATURE = 0.0


def getTemperature():
	global LAST_TEMPERATURE
	while True:
		try:
			proc = sp.run(CMD, capture_output=True, check=True, text=True)

		except sp.CalledProcessError as e:
			print(e.stderr)
			return None

		LAST_TEMPERATURE = float(re.findall(FIVE_NUM_PATTERN, proc.stdout)[0])*1.0E-3
		sleep(0.25)

def BackgroundTempSensing():
	threading.Thread(target=getTemperature, daemon=True).start()

