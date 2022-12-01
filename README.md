# ACQ_Python_ESP
App for collecting data from ESP device

## Recommended software:

anaconda prompt

	conda activate ampy
	ampy --port COM8 --baud 115200 <command>
					get
					put
					ls
					reset

putty

## MICROPython
### available libraries on board
  help('modules')
### Check of avalible memory
import gc
import os

	def df():
 		s = os.statvfs('//')
  		return ('{0} MB'.format((s[0]*s[3])/1048576))

	def free(full=False):
  		F = gc.mem_free()
  		A = gc.mem_alloc()
  		T = F+A
  		P = '{0:.2f}%'.format(F/T*100)
  		if not full: return P
  		else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))

## Whireshark
### IP address filter
	ip.addr == 192.168.1.101
