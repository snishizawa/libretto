
import sys, inspect 

def my_exit(depth=0):
	frame = inspect.currentframe().f_back
	path = frame.f_code.co_filename.split('/')
	print("file:"+path[-1] +" in:"+frame.f_code.co_name+", line:"+str(frame.f_lineno))
	sys.exit()

