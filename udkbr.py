'''
UDK Build & Run

Orginally writen by Arash Jafari [arashrj@gmail.com] in C#
__author__ = 'Hamed Nemati Ziabari - hitech.innovative@gmail.com'
__copyright__ = "Copyright (C) 2013 New Idea Game Studio - http://nigstudio.com/en/"
__license__ = "GPLv3"
__version__ = "1.1"
'''

import logging, time, os, sys
from subprocess import Popen, PIPE

import win32gui

class BuildRun():
	"""Build & Run Class"""
	def __init__(self):
		logger = logging.getLogger("udkbr")
		logger.setLevel(logging.ERROR)
		ch = logging.StreamHandler()
		ch.setLevel(logging.ERROR)
		logger.addHandler(ch)

		_succ = False
		self.timeout = 5
		udk_path = ''
		command = ''
		config = open('config.ini')
		lines = config.read().replace("\r", "").split('\n')

		for line in lines:
			if not line.startswith('#') and not line.endswith('udk') and line != '' and os.path.exists(line):
				udk_path = line
			if not line.startswith('#') and line.endswith('udk') and line != '':
				command = line
				break

		if udk_path == '':
			print 'set udk path in config.ini then run'
			input()
			sys.exit(0)

		if command:
			p = Popen( [udk_path + "UDK.com", "editor " + command], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		else:			
			p = Popen( [udk_path + "UDK.com", "editor"], stdin=PIPE, stdout=PIPE, stderr=PIPE)

		h = self.check_exist()
		if (h):
			self.click_yes()
			result = p.stdout.read()			
			strArr = result.replace("\r", "").split('\n')

			for output in strArr:
				if 'Success' in output:
					_succ = True
					if command:
						p = Popen( [udk_path + "UDK.com", "editor " + command])
					else:						
						p = Popen( [udk_path + "UDK.com", "editor"])
					sys.exit(0)
			_succ = False
			new_output = ''
			for output in strArr:
				if 'Error' in output:
					new_output += output + '\n'
			logger.error(new_output)
			raw_input()
			sys.exit(0)
		else:
			print 'Start'
			sys.exit(0)

	def click_cancel(self):	
		hwnd = win32gui.FindWindowEx(0, 0, 32770, "Message")
		hwnd = win32gui.FindWindowEx(hwnd, 0, "Button", "Cancel")
		message = 0xf5
		win32gui.SendMessage(hwnd, message, 0, 0)	
	
	def click_yes(self):
		message = 0xf5
		hwnd = win32gui.FindWindow("#32770", "Message")		
		hwnd2 = win32gui.FindWindowEx(hwnd, 0, "Button", "&Yes")       
		win32gui.SendMessage(hwnd2, message, 0, 0)

	def check_exist(self):
		hwnd = win32gui.FindWindow("#32770","Message")
		remaining = 5
		while hwnd == 0:
			time.sleep(0.05)
			hwnd = win32gui.FindWindow("#32770","Message")
			remaining -= 0.05
			if remaining <= 0:
				return False
		else:
			hwnd = win32gui.FindWindowEx(hwnd, 0, "Button", "&Yes")
	        if hwnd == 0:
	        	return False       
	        else:
				return hwnd

if __name__ == '__main__':
	br = BuildRun()