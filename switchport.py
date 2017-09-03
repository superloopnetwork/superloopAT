######################## FUNCTIONS ##############################

from display import view_interfaces
from parser import parse_engine
from multithread import multithread_engine
import initialize
import getpass


def switchport_config(database):

	initialize.switchport
	initialize.credentials
	del initialize.switchport[:]
	del initialize.credentials[:]
	check = 'interface_list'
	controller = 'switchport_config'
	parse_engine(database,check)
	view_interfaces(initialize.switchport)
	username = raw_input('PLEASE ENTER YOUR USERNAME: ')
	initialize.credentials.append(username)
	password = getpass.getpass(prompt="PLEASE ENTER YOUR PASSWORD: ")
	initialize.credentials.append(password)
	multithread_engine(initialize.switchport,controller,initialize.credentials)

