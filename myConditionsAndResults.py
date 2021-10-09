import argparse, re, os, shutil, subprocess

class MyConditionsAndResults:
	def __init__ (self):
		self.instance = None
		self.target_inport = None
		self.target_outport = None
		self.stable_inport = []
		self.stable_inport_val = [] 
		self.nontarget_outport = []
	
	def set_direction(self, outport="tmp"):
		if(outport == '01'):
			self.set_direction_rise()
		elif(outport == '10'):
			self.set_direction_fall()
		else:
			print("Illegal input: "+self.outport+", check direction \n")

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
			print("Illegal input: "+self.outport+", check unate \n")

	def set_timing_sense_pos(self):
		self.timing_sense = "positive_unate"

	def set_timing_sense_neg(self):
		self.timing_sense = "negative_unate"

	def set_timing_type_seqFall(self):
		self.timing_type_edge = "falling_edge"
		self.timing_type_setup = "setup_falling"
		self.timing_type_hold = "hold_falling"

	def set_timing_type_seqRise(self):
		self.timing_type_edge = "riseing_edge"
		self.timing_type_setup = "setup_riseing"
		self.timing_type_hold = "hold_riseing"

	def set_function(self, function="tmp"):
		self.function = function 

	def set_target_inport(self, inport="tmp", val="01"):
		self.target_inport = inport
		self.target_inport_val = val
		print(self.target_inport_val)
		print(self.target_inport)

	def set_target_outport(self, outport="tmp", function="tmp", val="01"):
		self.target_outport = outport
		self.target_function = function
		self.target_outport_val = val
		print(self.target_outport_val)
		print(self.target_outport)
		print(self.target_function)

	def set_stable_inport(self, inport="tmp", val="1"):
		self.stable_inport.append(inport)
		self.stable_inport_val.append(val)
		print(self.stable_inport)
		print(self.stable_inport_val)

	def set_nontarget_outport(self, outport="tmp"):
		self.stable_nontarget.append(outport)
		print(self.outport)

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
