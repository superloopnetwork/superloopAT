from globalc import global_config
from switchport import switchport_config

def execute_change():

	selection = 0

	loop=True

	while loop:
		print '#' * 29, 'MAIN MENU > EXECUTE CHANGE', '#' * 29, '\n'
		print '1. GLOBAL CONFIGURATION'
  		print '2. SWITCHPORT CONFIGURATION'
  		print '3. ROUTED PORT CONFIGURATION'
		print
  		print '99. RETURN TO MAIN MENU'
  		print '\n'
  		selection = int(raw_input('PLEASE MAKE YOUR SELECTION: '))
  		print'\n'
		
		if selection == 1:
			global_config()
		elif selection == 2:
				database = raw_input('PLEASE INPUT THE FILENAME TO IMPORT: ')
				print
				switchport_config(database)
		elif selection == 99:
			loop = False

		else:
			raw_input("! ! ! ! INVALID SELECTION. PLEASE TRY AGAIN ! ! ! !\n")

