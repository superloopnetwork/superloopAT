######################## FUNCTIONS ##############################

from credentials import credentials
from display import view_interfaces
from parser import parse_engine
from multithread import multithread_engine
import initialize
import getpass


def switchport_config(database):

	del initialize.switchport[:]
	del initialize.credentials[:]
	check = 'interface_list'
	controller = 'switchport_config'
	parse_engine(database,check)
	view_interfaces(initialize.switchport)
	initialize.credentials = credentials()
	multithread_engine(initialize.switchport,controller,initialize.credentials)