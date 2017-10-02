from addcredentials import addcredentials
from rmcredentials import rmcredentials

def addrmcredentials():

	selection = 0

	loop = True

	while loop:
		print '#' * 17, 'MAIN MENU > EXECUTE CHANGE > ADD/REMOVE CREDENTIAL', '#' * 17, '\n'
		print '1. ADD CREDENTIALS'
		print '2. REMOVE CREDENTIALS'
		print
		print '99. RETURN TO MAIN MENU'
		print '\n'
		selection = int(raw_input('PLEASE MAKE YOUR SELECTION: '))
		print'\n'
		if selection == 1:
			addcredentials()
		elif selection == 2:
			rmcredentials()
		elif selection == 99:
			loop = False
		else:
			raw_input('! ! ! ! INVALID SELECTION. PLEASE TRY AGAIN ! ! ! !\n')
