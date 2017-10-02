import initialize
import getpass

def rmuser():
	initialize.credentials = []
	username = raw_input('PLEASE ENTER THE USERNAME THAT YOU WOULD LIKE TO REMOVE: ')
	initialize.credentials.append(username)

	return initialize.credentials
