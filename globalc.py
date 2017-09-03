from engines import multithread_engine
import initialize

def global_config():

	selection = 0

	while (selection !=4):
		print '#' * 19, 'CONFIG CENTER > EXECUTE CHANGE > GLOBAL CHANGE', '#' * 19, '\n'
		print '1. ADD/REMOVE CREDENTIALS'
  		print '2. SNMP CONFIGURATION'
  		print '3. SYSLOG CONFIGURATION'
  		print '4. RETURN TO EXECUTE CHANGE MENU'
  		print '\n'
  		selection = int(raw_input('PLEASE MAKE YOUR SELECTION: '))
  		print("\n")

		if selection == 3:
			controller = 'syslog_config'
			multithread_engine(initialize.ntw_device,controller,initialize.credentials)
		elif selection == 4:
			loop = False
		else:
			raw_input('Wrong option selection. Enter any key to try again..')

