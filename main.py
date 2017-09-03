#!/usr/bin/env/python

from display import view_devices
from display import view_interfaces
from engines import parse_engine
from engines import multithread_engine
from execute import execute_change
import initialize
import os

parse = True

# GLOBAL VARIABLE OF NTW_DEVICE & SWITCHPORT OF TYPE LIST

############################ MENU SCREENS ############################

def main():

		os.system('clear')
		initialize.variable()
		global parse		

		if (parse == True):
			database = 'master_device_list'
			check = 'device_list'
			parse_engine(database,check)
			parse = False

		loop=True

		while loop:
			print '#' * 30, 'NETWORK AUTOMATION TOOLS', '#' * 30, '\n'
  			print '1. VIEW DEVICE LIST'
  			print '2. CONFIGURATION BACKUP'
  			print '3. EXECUTE CHANGE'
  			print '4. EXIT TO SHELL'
  			print '\n'
  			selection = int(raw_input('PLEASE MAKE YOUR SELECTION: '))
  			print '\n' 

			if selection == 1:
				view_devices(initialize.ntw_device)

			elif selection == 2:
				controller = 'config_backup'
				multithread_engine(initialize.ntw_device,controller,initialize.credentials)
			
			elif selection == 3:
				execute_change()

			elif selection == 4:
				loop = False

			else:
				raw_input("! ! ! ! INVALID SELECTION. PLEASE TRY AGAIN ! ! ! !\n")


if __name__ == '__main__':
	main()
