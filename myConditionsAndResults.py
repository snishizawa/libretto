import argparse, re, os, shutil, subprocess

class MyConditionsAndResults:
	def __init__ (self):
		self.instance = None          # instance name
		self.target_inport = None     # target inport name
		self.target_outport = None    # target outport name
		self.stable_inport = []       # stable imports
		self.stable_inport_val = []   # stable imports val
		self.nontarget_outport = []   # nontarget outport
		self.target_clock     = None  # target clock name
		self.target_clock_val = None  # target clock value
		self.target_reset     = None  # target reset name
		self.target_reset_val = None  # target reset val
		self.target_set     = None    # target set name
		self.target_set_val = None    # target set val
	
	def set_direction(self, outport="tmp"):
		if(outport == '01'):
			self.set_direction_rise()
		elif(outport == '10'):
			self.set_direction_fall()
		else:
			print("Illegal input: "+self.outport+", check direction")

	def set_direction_rise(self):
		self.direction_prop = "cell_rise"
		self.direction_tran = "rise_transition"

	def set_direction_fall(self):
		self.direction_prop = "cell_fall"
		self.direction_tran = "fall_transition"

	def set_timing_type_comb(self):
		self.timing_type = "combinational"

	def set_timing_sense(self, unate="tmp"):
		if(unate == 'pos'):
			self.timing_sense = "positive_unate"
		elif(unate == 'neg'):
			self.timing_sense = "negative_unate"
		elif(unate == 'non'):
			self.timing_sense = "non_unate"
		else:
			print("Illegal input: "+self.outport+", check unate")

	def set_timing_sense_pos(self):
		self.timing_sense = "positive_unate"

	def set_timing_sense_neg(self):
		self.timing_sense = "negative_unate"

	# set timing_sense and timing_type for input/output
	def set_timing_flop_inout(self, inport="tmp", outport="tmp"):
		# inport
		if((inport == 'pos')or(inport == '01')):
			self.timing_sense_setup = "rise_constraint"
			self.timing_sense_hold  = "rise_constraint"
			self.timing_type_setup = "setup_rising"
			self.timing_type_hold  = "hold_rising"
		elif((inport == 'neg')or(inport == '10')):
			self.timing_sense_setup = "fall_constraint"
			self.timing_sense_hold  = "fall_constraint"
			self.timing_type_setup = "setup_falling"
			self.timing_type_hold  = "hold_falling"
		else:
			print("Illegal input: "+self.outport+", check unate")
		# outport
		if((outport == 'pos')or(outport == '01')):
			self.timing_type_out = "rising_edge"
		elif((outport == 'neg')or(outport == '10')):
			self.timing_type_out = "falling_edge"
		else:
			print("Illegal input: "+self.outport+", check unate")
	
	def set_timing_flop_clock(self, inport="01", outport="01"):
		# inport
		if((inport == "01")or(inport.upper() == "RISE")or(inport.upper() == "pos")or(inport.upper() == "posedge")):
			self.timing_type_edge = "riseing_edge"
			self.timing_type_setup = "setup_riseing"
			self.timing_type_hold = "hold_riseing"
		elif((inport == "10")or(inport.upper() == "FALL")or(inport.upper() == "neg")or(inport.upper() == "negedge")):
			self.timing_type_edge = "falling_edge"
			self.timing_type_setup = "setup_falling"
			self.timing_type_hold = "hold_falling"
		else:
			self.timing_type_edge  = "NONE"
			self.timing_type_setup = "NONE"
			self.timing_type_hold  = "NONE"
		# outport
		if((outport == 'pos')or(outport == '01')):
			self.direction_clock_prop = "cell_rise"
			self.direction_clock_tran = "rise_transaction"
		elif((outport == 'neg')or(outport == '10')):
			self.direction_clock_prop = "cell_rise"
			self.direction_clock_tran = "rise_transaction"
		else:
			print("Illegal input: "+self.outport+", check unate")

	def set_timing_flop_set(self, inport="01", outport="01"):
		# inport
		if((inport == "01")or(inport.upper() == "RISE")):
			self.timing_sense_set = "positive_unate"
		elif((inport == "10")or(inport.upper() == "FALL")):
			self.timing_sense_set = "negative_unate"
		else:
			print("Warning: illigal inport type at set_timing_type_set: "+str(inport))
		# outport
		if((outport == "01")or(outport.upper() == "RISE")):
			self.timing_type_set = "preset"
			self.direction_set_prop = "cell_rise"
			self.direction_set_tran = "rise_transaction"
		elif((outport == "10")or(outport.upper() == "FALL")):
			self.timing_type_set = "clear"
			self.direction_set_prop = "cell_rise"
			self.direction_set_tran = "rise_transaction"
		else:
			print("Warning: illigal outport type at set_timing_type_set: "+str(inport))

	def set_timing_flop_reset(self, inport="01", outport="01"):
		# inport
		if((inport == "01")or(inport.upper() == "RISE")):
			self.timing_sense_reset = "positive_unate"
		elif((inport == "10")or(inport.upper() == "FALL")):
			self.timing_sense_reset = "negative_unate"
		else:
			print("Warning: illigal inport type at reset_timing_type_reset: "+str(inport))
		# outport
		if((outport == "01")or(outport.upper() == "RISE")):
			self.timing_type_reset = "preset"
			self.direction_reset_prop = "cell_rise"
			self.direction_reset_tran = "rise_transaction"
		elif((outport == "10")or(outport.upper() == "FALL")):
			self.timing_type_reset = "clear"
			self.direction_reset_prop = "cell_rise"
			self.direction_reset_tran = "rise_transaction"
		else:
			print("Warning: illigal outport type at set_timing_type_reset: "+str(inport))

	def set_function(self, function="tmp"):
		self.function = function 

	def set_target_inport(self, inport="tmp", val="01"):
		self.target_inport = inport
		self.target_inport_val = val
		#print(self.target_inport_val)
		#print(self.target_inport)

	def set_target_outport(self, outport="tmp", function="tmp", val="01"):
		self.target_outport = outport
		self.target_function = function
		self.target_outport_val = val
		#print(self.target_outport_val)
		#print(self.target_outport)
		#print(self.target_function)

	def set_stable_inport(self, inport="tmp", val="1"):
		self.stable_inport.append(inport)
		self.stable_inport_val.append(val)
		#print(self.stable_inport)
		#print(self.stable_inport_val)

	def set_nontarget_outport(self, outport="tmp"):
		self.stable_nontarget.append(outport)
		#print(self.outport)

	def set_target_clock(self, inport="tmp", val="01"):
		self.target_clock = inport
		self.target_clock_val = val
		#print(self.target_clock_val)
		#print(self.target_clock)

	def set_target_reset(self, inport="tmp", val="01"):
		self.target_reset = inport
		self.target_reset_val = val
		#print(self.target_reset_val)
		#print(self.target_reset)

	def set_target_set(self, inport="tmp", val="01"):
		self.target_set = inport
		self.target_set_val = val
		#print(self.target_set_val)
		#print(self.target_set)

	def set_list2_prop(self, list2_prop=[]):
		self.list2_prop = list2_prop 

	def print_list2_prop(self, ilist, jlist):
		for i in range(len(ilist)):
			for j in range(len(jlist)):
				print(self.list2_prop[i][j])
	
	def print_lut_prop(self):
		for i in range(len(self.lut_prop)):
			print(self.lut_prop[i])

	def write_list2_prop(self, targetLib, ilist, jlist):
		# index_1
		outline = "index_1(\""
		self.lut_prop = []
		for j in range(len(jlist)-1):
			outline += str(jlist[j])+", " 
		outline += str(jlist[len(jlist)-1])+"\");" 
		#print(outline)
		self.lut_prop.append(outline)
		# index_2
		outline = "index_2(\""
		for i in range(len(ilist)-1):
			outline += str(ilist[i])+", " 
		outline += str(ilist[len(ilist)-1])+"\");" 
		self.lut_prop.append(outline)
		# values
		self.lut_prop.append("values ( \\")
		for i in range(len(ilist)):
			outline = "\""
			for j in range(len(jlist)-1):
				outline += str(self.list2_prop[i][j])+", "
			# do not add "," for last line
			if(i == (len(ilist)-1)): 
				outline += str(self.list2_prop[i][len(jlist)-1])+"\" \\"
			#  add "," for else 
			else:	
				outline += str(self.list2_prop[i][len(jlist)-1])+"\", \\"
			self.lut_prop.append(outline)
		self.lut_prop.append(");")

	def set_list2_setup(self, list2_setup=[]):
		self.list2_setup = list2_setup 

	def print_list2_setup(self, ilist, jlist):
		for i in range(len(ilist)):
			for j in range(len(jlist)):
				print(self.list2_setup[i][j])
	
	def print_lut_setup(self):
		for i in range(len(self.lut_setup)):
			print(self.lut_setup[i])

	def write_list2_setup(self, targetLib, ilist, jlist):
		# index_1
		outline = "index_1(\""
		self.lut_setup = []
		for j in range(len(jlist)-1):
			outline += str(jlist[j])+", " 
		outline += str(jlist[len(jlist)-1])+"\");" 
		#print(outline)
		self.lut_setup.append(outline)
		# index_2
		outline = "index_2(\""
		for i in range(len(ilist)-1):
			outline += str(ilist[i])+", " 
		outline += str(ilist[len(ilist)-1])+"\");" 
		self.lut_setup.append(outline)
		# values
		self.lut_setup.append("values ( \\")
		for i in range(len(ilist)):
			outline = "\""
			for j in range(len(jlist)-1):
				outline += str(self.list2_setup[i][j])+", "
			# do not add "," for last line
			if(i == (len(ilist)-1)): 
				outline += str(self.list2_setup[i][len(jlist)-1])+"\" \\"
			#  add "," for else 
			else:	
				outline += str(self.list2_setup[i][len(jlist)-1])+"\", \\"
			self.lut_setup.append(outline)
		self.lut_setup.append(");")

	def set_list2_hold(self, list2_hold=[]):
		self.list2_hold = list2_hold 

	def print_list2_hold(self, ilist, jlist):
		for i in range(len(ilist)):
			for j in range(len(jlist)):
				print(self.list2_hold[i][j])
	
	def print_lut_hold(self):
		for i in range(len(self.lut_hold)):
			print(self.lut_hold[i])

	def write_list2_hold(self, targetLib, ilist, jlist):
		# index_1
		outline = "index_1(\""
		self.lut_hold = []
		for j in range(len(jlist)-1):
			outline += str(jlist[j])+", " 
		outline += str(jlist[len(jlist)-1])+"\");" 
		#print(outline)
		self.lut_hold.append(outline)
		# index_2
		outline = "index_2(\""
		for i in range(len(ilist)-1):
			outline += str(ilist[i])+", " 
		outline += str(ilist[len(ilist)-1])+"\");" 
		self.lut_hold.append(outline)
		# values
		self.lut_hold.append("values ( \\")
		for i in range(len(ilist)):
			outline = "\""
			for j in range(len(jlist)-1):
				outline += str(self.list2_hold[i][j])+", "
			# do not add "," for last line
			if(i == (len(ilist)-1)): 
				outline += str(self.list2_hold[i][len(jlist)-1])+"\" \\"
			#  add "," for else 
			else:	
				outline += str(self.list2_hold[i][len(jlist)-1])+"\", \\"
			self.lut_hold.append(outline)
		self.lut_hold.append(");")

	def set_list2_tran(self, list2_tran=[]):
		self.list2_tran = list2_tran 

	def print_list2_tran(self, ilist, jlist):
		for i in range(len(ilist)):
			for j in range(len(jlist)):
				print(self.list2_tran[i][j])
	
	def print_lut_tran(self):
		for i in range(len(self.lut_tran)):
			print(self.lut_tran[i])

	def write_list2_tran(self, targetLib, ilist, jlist):
		# index_1
		outline = "index_1(\""
		self.lut_tran = []
		for j in range(len(jlist)-1):
			outline += str(jlist[j])+", " 
		outline += str(jlist[len(jlist)-1])+"\");" 
		#print(outline)
		self.lut_tran.append(outline)
		# index_2
		outline = "index_2(\""
		for i in range(len(ilist)-1):
			outline += str(ilist[i])+", " 
		outline += str(ilist[len(ilist)-1])+"\");" 
		# values
		self.lut_tran.append("values ( \\")
		for i in range(len(ilist)):
			outline = "\""
			for j in range(len(jlist)-1):
				outline += str(self.list2_tran[i][j])+", "
			if(i == (len(ilist)-1)): 
				outline += str(self.list2_tran[i][len(jlist)-1])+"\" \\"
			#  add "," for else 
			else:	
				outline += str(self.list2_tran[i][len(jlist)-1])+"\", \\"
			self.lut_tran.append(outline)
		self.lut_tran.append(");")
