######################## FUNCTIONS ##############################

from credentials import credentials
from display import view_interfaces
from parser import parse_engine
from multithread import multithread_engine
import initialize
import getpass


def default_interface(database):

	del initialize.credentials[:]
	controller = 'default_interface'
	initialize.credentials = credentials()
	multithread_engine(initialize.ntw_device,controller,credentials)
