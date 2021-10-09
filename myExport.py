
import argparse, re, os, shutil, subprocess, sys 

def exportFiles(targetLib, targetCell, harnessList2):
	if(targetLib.isexport == 0):
		exportLib(targetLib, targetCell)
	if((targetLib.isexport == 1) and (targetCell.isexport == 0)):
		exportHarness(targetLib, targetCell, harnessList2)
		exportVerilog(targetLib, targetCell)

# export library definition to .lib
def exportLib(targetLib, targetCell):
	with open(targetLib.dotlib_name, 'w') as f:
		outlines = []
		# general settings
		outlines.append("library ("+targetLib.lib_name+"){\n")
		outlines.append("  delay_model : \""+targetLib.delay_model+"\";\n")
		outlines.append("  capacitive_load_unit (1,"+targetLib.capacitance_unit+");\n")
		outlines.append("  current_unit : \"1"+targetLib.current_unit+"\";\n")
		outlines.append("  leakage_power_unit : \"1"+targetLib.leakage_power_unit+"\";\n")
		outlines.append("  pulling_resistance_unit : \"1"+targetLib.resistance_unit+"\";\n")
		outlines.append("  time_unit : \"1"+targetLib.time_unit+"\";\n")
		outlines.append("  voltage_unit : \"1"+targetLib.voltage_unit+"\";\n")
		outlines.append("  voltage_map ("+targetLib.vdd_name+", "+str(targetLib.vdd_voltage)+");\n")
		outlines.append("  voltage_map ("+targetLib.vss_name+", "+str(targetLib.vss_voltage)+");\n")
		outlines.append("  voltage_map (GND , "+str(targetLib.vss_voltage)+");\n")
		outlines.append("  default_cell_leakage_power : 0;\n")
		outlines.append("  default_fanout_load : 1;\n")
		outlines.append("  default_max_transition : 1000;\n")
		outlines.append("  default_input_pin_cap : 0;\n")
		outlines.append("  default_inout_pin_cap : 0;\n")
		outlines.append("  default_output_pin_cap : 0;\n")
		outlines.append("  in_place_swap_mode : match_footprint;\n")
		outlines.append("  input_threshold_pct_fall : "+str(float(targetLib.logic_high_to_low_threshold)*100)+";\n")
		outlines.append("  input_threshold_pct_rise : "+str(float(targetLib.logic_low_to_high_threshold)*100)+";\n")
		outlines.append("  nom_process : 1;\n")
		outlines.append("  nom_temperature : \""+targetLib.temperature+"\";\n")
		outlines.append("  nom_voltage : \""+targetLib.vdd_voltage+"\";\n")
		outlines.append("  output_threshold_pct_fall : "+str(float(targetLib.logic_high_to_low_threshold)*100)+";\n")
		outlines.append("  output_threshold_pct_rise : "+str(float(targetLib.logic_low_to_high_threshold)*100)+";\n")
		outlines.append("  slew_derate_from_library : 1;\n")
		outlines.append("  slew_lower_threshold_pct_fall : "+str(float(targetLib.logic_threshold_low)*100)+";\n")
		outlines.append("  slew_lower_threshold_pct_rise : "+str(float(targetLib.logic_threshold_low)*100)+";\n")
		outlines.append("  slew_upper_threshold_pct_fall : "+str(float(targetLib.logic_threshold_high)*100)+";\n")
		outlines.append("  slew_upper_threshold_pct_rise : "+str(float(targetLib.logic_threshold_high)*100)+";\n")
		# operating conditions
		outlines.append("  operating_conditions ("+targetLib.operating_conditions+") {\n")
		outlines.append("    process : 1;\n")
		outlines.append("    temperature : "+targetLib.temperature+";\n")
		outlines.append("    voltage : "+targetLib.vdd_voltage+";\n")
		outlines.append("  }\n")
		outlines.append("  default_operating_conditions : "+targetLib.operating_conditions+";\n")
		outlines.append("  lu_table_template (constraint_template) {\n")
		outlines.append("    variable_1 : constrained_pin_transition;\n")
		outlines.append("    variable_2 : related_pin_transition;\n")
		outlines.append("    index_1 "+targetCell.return_slope()+"\n")
		outlines.append("    index_2 "+targetCell.return_slope()+"\n")
		outlines.append("  }\n")
		outlines.append("  lu_table_template (delay_template) {\n")
		outlines.append("    variable_1 : input_net_transition;\n")
		outlines.append("    variable_2 : total_output_net_capacitance;\n")
		outlines.append("    index_1 "+targetCell.return_slope()+"\n")
		outlines.append("    index_2 "+targetCell.return_load()+"\n")
		outlines.append("  }\n")
		outlines.append("  lu_table_template (mpw_constraint_template) {\n")
		outlines.append("    variable_1 : constrained_pin_transition;\n")
		outlines.append("    index_1 "+targetCell.return_slope()+"\n")
		outlines.append("  }\n")
		outlines.append("  power_lut_template (passive_power_template) {\n")
		outlines.append("    variable_1 : input_transition_time;\n")
		outlines.append("    index_1 "+targetCell.return_slope()+"\n")
		outlines.append("  }\n")
		outlines.append("  power_lut_template (power_template) {\n")
		outlines.append("    variable_1 : input_transition_time;\n")
		outlines.append("    variable_2 : total_output_net_capacitance;\n")
		outlines.append("    index_1 "+targetCell.return_slope()+"\n")
		outlines.append("    index_2 "+targetCell.return_load()+"\n")
		outlines.append("  }\n")
		outlines.append("  input_voltage (default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_input) {\n")
		outlines.append("    vil : "+targetLib.vss_voltage+";\n")
		outlines.append("    vih : "+targetLib.vdd_voltage+";\n")
		outlines.append("    vimin : "+targetLib.vss_voltage+";\n")
		outlines.append("    vimax : "+targetLib.vdd_voltage+";\n")
		outlines.append("  }\n")
		outlines.append("  output_voltage (default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_output) {\n")
		outlines.append("    vol : "+targetLib.vss_voltage+";\n")
		outlines.append("    voh : "+targetLib.vdd_voltage+";\n")
		outlines.append("    vomin : "+targetLib.vss_voltage+";\n")
		outlines.append("    vomax : "+targetLib.vdd_voltage+";\n")
		outlines.append("  }\n")
	
		f.writelines(outlines)
	f.close()
	targetLib.set_exported()

	# for verilog file 
	outlines = []
	with open(targetLib.verilog_name, 'w') as f:
		outlines.append("// Verilog model for "+targetLib.lib_name+"; \n")
		f.writelines(outlines)
	f.close()

# export harness data to .lib
def exportHarness(targetLib, targetCell, harnessList2):
	with open(targetLib.dotlib_name, 'a') as f:
		outlines = []
		outlines.append("  cell ("+targetCell.cell+") {\n") ## cell start
#		outlines.append("    area : "+targetCell.area+";\n")
#		outlines.append("    cell_leakage_power : "+targetCell.leak+";\n")
		outlines.append("    pg_pin ("+targetLib.vdd_name+"){\n")
		outlines.append("      pg_type : primary_power;\n")
		outlines.append("      voltage_name : \""+targetLib.vdd_name+"\";\n")
		outlines.append("    }\n")
		outlines.append("    pg_pin ("+targetLib.vss_name+"){\n")
		outlines.append("      pg_type : primary_ground;\n")
		outlines.append("      voltage_name : \""+targetLib.vss_name+"\";\n")
		outlines.append("    }\n")

		# select one output pin from pinlist(target_outports) 
		for target_outport in targetCell.outports:
			index1 = targetCell.outports.index(target_outport) 
			outlines.append("    pin ("+target_outport+"){\n") ## out pin start
			outlines.append("      direction : output;\n")
			outlines.append("      function : \"("+targetCell.functions[index1]+")\"\n")
			outlines.append("      related_power_pin : \""+targetLib.vdd_name+"\";\n")
			outlines.append("      related_ground_pin : \""+targetLib.vss_name+"\";\n")
#			outlines.append("      max_capacitance : \""+targetLib.vss_name+"\";\n")
			outlines.append("      output_voltage : default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_output;\n")
			for target_inport in targetCell.inports:
				outlines.append("      timing () {\n")
				index2 = targetCell.inports.index(target_inport) 
				outlines.append("        related_pin : \""+target_inport+"\";\n")
				outlines.append("        timing_sense : \""+harnessList2[index1][index2*2].timing_sense+"\";\n")
				outlines.append("        timing_type : \""+harnessList2[index1][index2*2].timing_type+"\";\n")
				## rise
				# propagation delay
				outlines.append("        "+harnessList2[index1][index2*2].direction_prop+" (delay_template) {\n")
				for lut_line in harnessList2[index1][index2*2].lut_prop:
					outlines.append("          "+lut_line+"\n")
				outlines.append("        }\n") 
				# transition delay
				outlines.append("        "+harnessList2[index1][index2*2].direction_tran+" (delay_template) {\n")
				for lut_line in harnessList2[index1][index2*2].lut_tran:
					outlines.append("          "+lut_line+"\n")
				outlines.append("        }\n") 
				## fall
				# propagation delay
				outlines.append("        "+harnessList2[index1][index2*2+1].direction_prop+" (delay_template) {\n")
				for lut_line in harnessList2[index1][index2*2].lut_prop:
					outlines.append("          "+lut_line+"\n")
				outlines.append("        }\n") 
				# transition delay
				outlines.append("        "+harnessList2[index1][index2*2+1].direction_tran+" (delay_template) {\n")
				for lut_line in harnessList2[index1][index2*2].lut_tran:
					outlines.append("          "+lut_line+"\n")
				outlines.append("        }\n") 
				outlines.append("      }\n") 
			outlines.append("    }\n") ## out pin end

		# select one input pin from pinlist(target_inports) 
		for target_inport in targetCell.inports:
			index1 = targetCell.inports.index(target_inport) 
			outlines.append("    pin ("+target_inport+"){\n") ## out pin start
			outlines.append("      direction : input; \n")
			outlines.append("      related_power_pin : "+targetLib.vdd_name+";\n")
			outlines.append("      related_ground_pin : "+targetLib.vss_name+";\n")
			outlines.append("      max_transition : "+targetCell.slope[-1]+";\n")
#			outlines.append("      max_capacitance : \""+targetLib.vss_name+"\";\n")
			outlines.append("      input_voltage : default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_input;\n")
			outlines.append("    }\n") ## in pin end


			# select one harness from harnessList
			#for targetHarness in harnessList:
		
	
		outlines.append("  }\n") ## cell end
		f.writelines(outlines)
	f.close()
	targetCell.set_exported()

# export library definition to .lib
def exportVerilog(targetLib, targetCell):
	with open(targetLib.verilog_name, 'a') as f:
		outlines = []

		# list ports in one line 
		portlist = "("
		numport = 0
		for target_outport in targetCell.outports:
			if(numport != 0):
				portlist = str(portlist)+", "
			portlist = str(portlist)+str(target_outport)
			numport += 1
		for target_inport in targetCell.inports:
			portlist = str(portlist)+","+str(target_inport)
			numport += 1
		portlist = str(portlist)+");"

		outlines.append("module "+str(targetCell.cell)+str(portlist)+"\n")

		# input/output statement
		for target_outport in targetCell.outports:
			outlines.append("output "+str(target_outport)+";\n")
		for target_inport in targetCell.inports:
			outlines.append("input "+str(target_inport)+";\n")

		# branch for sequencial cell
		if(targetCell.logic == "DFFARAS"):
			print ("This cell "+str(targetCell.logic)+" is not supported for verilog out\n")
			sys.exit

		# branch for combinational cell
		else:
		# assign statement
			for target_outport in targetCell.outports:
				index1 = targetCell.outports.index(target_outport) 
				outlines.append("assign "+str(target_outport)+" = "+str(targetCell.functions[index1])+";\n")

		outlines.append("endmodule\n\n")
		f.writelines(outlines)
	f.close()


# export harness data to .lib
def exitFiles(targetLib):
	with open(targetLib.dotlib_name, 'a') as f:
		outlines = []
		outlines.append("}\n")
		f.writelines(outlines)
	f.close()
	print("\n  dotlib file generation completed!!  \n")

