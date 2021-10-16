import argparse, re, os, shutil, subprocess

class MyLogicCell:
	def __init__ (self):
		self.cell = None    # cell name
		self.functions = [] # cell function
		self.inports = []   # inport pins
		self.clock = None   # clock pin for flop
		self.set = None     # set pin for flop
		self.reset = None   # reset pin for flop 
		self.outports = []  # outport pins
		self.flops = []     # registers 
		self.functions = [] # logic/flop functions 
		self.slope = []     # inport slope
		self.cslope = 0     # inport slope
		self.load = []      # outport load
		self.isexport = 0

	def add_cell(self, line="tmp"):
		tmp_array = line.split('-')
		# expected format : add_cell -n(name) AND_X1 
		#                            -l(logic) AND2 
		#														 -i(inports) A B 
		#														 -o(outports) YB
		#														 -f(function) YB=A*B
		for options in tmp_array:

			# add_cell command 
			if(re.match("^add_cell", options)):
				continue
			# -n option
			elif(re.match("^n ", options)):
				tmp_array2 = options.split() 
				self.cell = tmp_array2[1] 
				#print (self.cell)
			# -l option
			elif(re.match("^l ", options)):
				tmp_array2 = options.split() 
				self.logic = tmp_array2[1] 
				print (self.logic)
			# -i option
			elif(re.match("^i ", options)):
				tmp_array2 = options.split() 
				for w in tmp_array2:
					self.inports.append(w)
				self.inports.pop(0) # delete first object("-i")
				print (self.inports)
			# -o option
			# -f option override -o option
			# currently, -o is not used
			elif(re.match("^o ", options)):
				tmp_array2 = options.split() 
				#for w in tmp_array2:
				#	self.outports.append(w)
				#self.outports.pop(0) # delete first object("-o")
				#print (self.outports)
			# -f option
			elif(re.match("^f ", options)):
				tmp_array2 = options.split() 
				#print (tmp_array2)
				tmp_array2.pop(0) # delete first object("-f")
				for w in tmp_array2:
					tmp_array3 = w.split('=') 
					self.outports.append(tmp_array3[0])
					self.functions.append(tmp_array3[1])
				#self.functions.pop(0) # delete first object("-f")
				#self.outports.pop(0) # delete first object("-o")
				print (self.functions)
				print (self.outports)
			# undefined option 
			else:
				print("ERROR: undefined option:"+options+"\n")	
		print ("finish add_cell")

	def add_flop(self, line="tmp"):
		tmp_array = line.split('-')
		# expected format : add_floop -n(name) DFFRS_X1 /
		#                             -l(logic)    DFFARAS : DFF w async RST and async SET
		#														  -i(inports)  DATA 
		#														  -c(clock)    CLK 
		#														  -s(set)      SET   (if used) 
		#														  -r(reset)    RESET (if used)
		#														  -o(outports) Q QN
		#														  -q(flops)    IQ IQN
		#														  -f(function) Q=IQ QN=IQN
		for options in tmp_array:

			# add_flop command 
			if(re.match("^add_flop", options)):
				continue
			# -n option (subckt name)
			elif(re.match("^n ", options)):
				tmp_array2 = options.split() 
				self.cell = tmp_array2[1] 
				#print (self.cell)
			# -l option (logic type)
			elif(re.match("^l ", options)):
				tmp_array2 = options.split() 
				self.logic = tmp_array2[1] 
				print (self.logic)
			# -i option (input name)
			elif(re.match("^i ", options)):
				tmp_array2 = options.split() 
				for w in tmp_array2:
					self.inports.append(w)
				self.inports.pop(0) # delete first object("-i")
				print (self.inports)
			# -c option (clock name)
			elif(re.match("^c ", options)):
				tmp_array2 = options.split() 
				self.clock = tmp_array2[1] 
				print (self.clock)
			# -s option (set name)
			elif(re.match("^s ", options)):
				tmp_array2 = options.split() 
				self.set = tmp_array2[1] 
				print (self.set)
			# -r option (reset name)
			elif(re.match("^r ", options)):
				tmp_array2 = options.split() 
				self.reset = tmp_array2[1] 
				print (self.reset)
			# -o option (output name)
			# -f option override -o option
			# currently, -o is meaningful
			elif(re.match("^o ", options)):
				tmp_array2 = options.split() 
				#for w in tmp_array2:
				#	self.outports.append(w)
				#self.outports.pop(0) # delete first object("-o")
				#print (self.outports)
			# -q option (storage name)
			elif(re.match("^q ", options)):
				tmp_array2 = options.split() 
				for w in tmp_array2:
					self.flops.append(w)
				self.flops.pop(0) # delete first object("-i")
				print (self.flops)
			# -f option (function name)
			elif(re.match("^f ", options)):
				tmp_array2 = options.split() 
				#print (tmp_array2)
				tmp_array2.pop(0) # delete first object("-f")
				for w in tmp_array2:
					tmp_array3 = w.split('=') 
					self.outports.append(tmp_array3[0])
					self.functions.append(tmp_array3[1])
				print (self.functions)
				print (self.outports)
			# undefined option 
			else:
				print("ERROR: undefined option:"+options+"\n")	
				sys.exit()
		print ("finish add_flop")

	def add_slope(self, line="tmp"):
		line = re.sub('\{','',line)
		line = re.sub('\}','',line)
		tmp_array = line.split()
		for w in tmp_array:
			self.slope.append(w)
		self.slope.pop(0) # delete first object("add_slope")
		print (self.slope)

	def add_load(self, line="tmp"):
		line = re.sub('\{','',line)
		line = re.sub('\}','',line)
		tmp_array = line.split()
		for w in tmp_array:
			self.load.append(w)
		self.load.pop(0) # delete first object("add_load")
		print (self.load)

	def return_slope(self):
		jlist = self.slope
		outline = "(\""
		self.lut_prop = []
		for j in range(len(jlist)-1):
			outline += str(jlist[j])+", " 
		outline += str(jlist[len(jlist)-1])+"\");" 
		return outline

	def return_load(self):
		jlist = self.load
		outline = "(\""
		self.lut_prop = []
		for j in range(len(jlist)-1):
			outline += str(jlist[j])+", " 
		outline += str(jlist[len(jlist)-1])+"\");" 
		return outline

	def add_netlist(self, line="tmp"):
		tmp_array = line.split()
		self.netlist = tmp_array[1]
		self.definition = None 
		self.instance = None 
		lines = open(self.netlist, "r")
		# search cell name in the netlist
		for line in lines:
			#print("self.cell.lower:"+str(self.cell.lower()))
			#print("line.lower:"+str(line.lower()))
			if((self.cell.lower() in line.lower()) and (".subckt" in line.lower())):
				print("Cell definition found!\n")
				#print(line)
				self.definition = line
				# generate circuit call
				line = re.sub('\$.*$','',line)
				tmp_array2 = line.split()
				#print (tmp_array2)
				tmp_array2.pop(0) # delete .subckt
				#print (tmp_array2)
				tmp_str = tmp_array2.pop(0)
				#print (tmp_array2)
				tmp_array2.append(tmp_str) # move circuit name to last
				#print (tmp_array2)
				tmp_array2.insert(0,"XDUT") # insert instance name 
				#print (tmp_array2)
				self.instance = ' '.join(tmp_array2) # convert array into string
				
				
		# if cell name is not found, show error
		if(self.definition == None):
			print("Cell definition not found. Please use add_cell command to add your cell\n")
			sys.exit()

	def add_model(self, line="tmp"):
		tmp_array = line.split()
		self.model = tmp_array[1] 

	def add_simulation_timestep(self, line="tmp"):
		tmp_array = line.split()
		# if auto, amd slope is defined, use 1/10 of min slope
		if ((tmp_array[1] == 'auto') and (self.slope[0] != None)):
			self.simulation_timestep = float(self.slope[0])/10 
			print ("auto set simulation timestep\n")
		else:
			self.simulation_timestep = tmp_array[1] 
			
	def add_clock_slope(self, line="tmp"):
		tmp_array = line.split()
		# if auto, amd slope is defined, use 1/10 of min slope
		if (tmp_array[1] == 'auto')):
			self.cslope = float(self.slope[0]) 
			print ("auto set clock slope as mininum slope.\n")
		else:
			self.cslope = tmp_array[1] 
			
	def set_exported(self):
		self.isexport = 1 
