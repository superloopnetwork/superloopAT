import initialize
import getpass

def adduserpass():

	initialize.credentials = []
	username = raw_input('PLEASE ENTER THE USERNAME THAT YOU WOULD LIKE TO ADD: ')
	initialize.credentials.append(username)
	password = getpass.getpass(prompt="PLEASE ENTER THE PASSWORD THAT YOU WOULD LIKE TO SET: ")
	initialize.credentials.append(password)

	return initialize.credentials
