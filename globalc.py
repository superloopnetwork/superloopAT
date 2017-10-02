from multithread import multithread_engine
from default import default_interface
from systemlog import syslog_config 
from addrmcredentials import addrmcredentials
import initialize

def global_config():

	selection = 0

	loop = True
	while loop:
		print '#' * 19, 'CONFIG CENTER > EXECUTE CHANGE > GLOBAL CHANGE', '#' * 19, '\n'
		print '1. DEFAULT INTERFACE CONFIGURATION'
		print '2. ADD/REMOVE CREDENTIALS'
  		print '3. SNMP CONFIGURATION'
  		print '4. SYSLOG CONFIGURATION'
		print
  		print '99. RETURN TO EXECUTE CHANGE MENU'
  		print '\n'
  		selection = int(raw_input('PLEASE MAKE YOUR SELECTION: '))
  		print("\n")

		if selection == 1:
			default_interface()
		elif selection == 2:
			addrmcredentials()
		elif selection == 4:
			syslog_config()
		elif selection == 99:
			loop = False
		else:
			raw_input('Wrong option selection. Enter any key to try again..')

