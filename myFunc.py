
import sys, inspect 

def my_exit():
	frame = inspect.currentframe().f_back
	path = frame.f_code.co_filename.split('/')
	print("file:"+path[-1] +" in:"+frame.f_code.co_name+", line:"+str(frame.f_lineno))
	sys.exit()

def startup():
	print("  ")
	print("  libretto: Cell library characterizer")
	print("  Version: 0.2")
	print("  https://github.com/snishizawa/libretto")
	print("  ")

def history():
	print("  Version: 0.2")
	print("  + Support multiple slope load conditions")
	print("  Version: 0.1")
	print("  + Very basic version")
	print("  + Support combinational cells")
	print("  +++ Propagation delay, transition delay")
	print("  +++ Dynamic power, leakage power")
	print("  + Support sequential cells")
	print("  ++ D-Flip-Flops, include both pos-neg edge clock, asyncronous set reset")
	print("  +++ C2Q delay, setup, hold, recovery, removal")
	print("  +++ Setup is defined by minimum D2Q, hold is defined by minimum D2Q")

