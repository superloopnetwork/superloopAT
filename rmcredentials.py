######################## FUNCTIONS ##############################
from rmuser import rmuser
from multithread import multithread_engine
import initialize

def rmcredentials():
	del initialize.credentials[:]
	controller = 'rm_credentials'
	initialize.credentials = rmuser()
	multithread_engine(initialize.ntw_device,controller,initialize.credentials)
