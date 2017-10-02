######################## FUNCTIONS ##############################
from adduserpass import adduserpass
from multithread import multithread_engine
import initialize

def addcredentials():
	del initialize.credentials[:]
	controller = 'add_credentials'
	initialize.credentials = adduserpass()
	multithread_engine(initialize.ntw_device,controller,initialize.credentials)
