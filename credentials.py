import initialize
import getpass

def credentials():
	initialize.credentials = []
	username = raw_input('PLEASE ENTER YOUR USERNAME: ')
	initialize.credentials.append(username)
	password = getpass.getpass(prompt="PLEASE ENTER YOUR PASSWORD: ")
	initialize.credentials.append(password)

	return initialize.credentials
