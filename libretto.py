#!/usr/bin/env pytghon
# -*- coding: utf-8 -*-

import argparse, re, os, shutil, subprocess, sys 

import myConditionsAndResults as mcar
import myLibrarySetting as mls 
import myLogicCell as mlc
import myExport as me

def main():
	parser = argparse.ArgumentParser(description='argument')
	parser.add_argument('-b','--batch', type=str, help='inport batch file')
	args = parser.parse_args()
	#print(args.batch)

	targetLib = mls.MyLibrarySetting() 

	# file open
	with open(args.batch, 'r') as f:
		lines = f.readlines()
		
		for line in lines:
			line = line.strip('\n')
#-- set function --#
			# set_lib_name
			if(line.startswith('set_lib_name')):
				targetLib.set_lib_name(line) 

			if(line.startswith('set_dotlib_name')):
				targetLib.set_dotlib_name(line) 

			if(line.startswith('set_verilog_name')):
				targetLib.set_verilog_name(line) 

			# set_cell_name_suffix
			elif(line.startswith('set_cell_name_suffix')):
				targetLib.set_cell_name_suffix(line) 

			# set_cell_name_prefix
			elif(line.startswith('set_cell_name_prefix')):
				targetLib.set_cell_name_prefix(line) 

			# set_voltage_unit
			elif(line.startswith('set_voltage_unit')):
				targetLib.set_voltage_unit(line) 

			# set_capacitance_unit
			elif(line.startswith('set_capacitance_unit')):
				targetLib.set_capacitance_unit(line) 

			# set_resistance_unit
			elif(line.startswith('set_resistance_unit')):
				targetLib.set_resistance_unit(line) 

			# set_time_unit
			elif(line.startswith('set_time_unit')):
				targetLib.set_time_unit(line) 

			# set_current_unit
			elif(line.startswith('set_current_unit')):
				targetLib.set_current_unit(line) 

			# set_leakage_power_unit
			elif(line.startswith('set_leakage_power_unit')):
				targetLib.set_leakage_power_unit(line) 

			# set_vdd_name
			elif(line.startswith('set_vdd_name')):
				targetLib.set_vdd_name(line) 

			# set_vss_name
			elif(line.startswith('set_vss_name')):
				#print(line)
				targetLib.set_vss_name(line) 

			# set_pwell_name
			elif(line.startswith('set_pwell_name')):
				#print(line)
				targetLib.set_pwell_name(line) 

			# set_nwell_name
			elif(line.startswith('set_nwell_name')):
				targetLib.set_nwell_name(line) 

			# set_process
			elif(line.startswith('set_process')):
				targetLib.set_process(line) 

			# set_temperature
			elif(line.startswith('set_temperature')):
				targetLib.set_temperature(line) 

			# set_vdd_voltage
			elif(line.startswith('set_vdd_voltage')):
				targetLib.set_vdd_voltage(line) 

			# set_vss_voltage
			elif(line.startswith('set_vss_voltage')):
				targetLib.set_vss_voltage(line) 

			# set_pwell_voltage
			elif(line.startswith('set_pwell_voltage')):
				targetLib.set_pwell_voltage(line) 

			# set_nwell_voltage
			elif(line.startswith('set_nwell_voltage')):
				targetLib.set_nwell_voltage(line) 

			# set_logic_threshold_high
			elif(line.startswith('set_logic_threshold_high')):
				targetLib.set_logic_threshold_high(line) 

			# set_logic_threshold_low
			elif(line.startswith('set_logic_threshold_low')):
				targetLib.set_logic_threshold_low(line) 

			# set_logic_high_to_low_threshold
			elif(line.startswith('set_logic_high_to_low_threshold')):
				targetLib.set_logic_high_to_low_threshold(line) 

			# set_logic_low_to_high_threshold
			elif(line.startswith('set_logic_low_to_high_threshold')):
				targetLib.set_logic_low_to_high_threshold(line) 

			# set_work_dir
			elif(line.startswith('set_work_dir')):
				targetLib.set_work_dir(line) 

			# set_simulator
			elif(line.startswith('set_simulator')):
				targetLib.set_simulator(line) 

			# set_energy_meas_low_threshold
			elif(line.startswith('set_energy_meas_low_threshold')):
				targetLib.set_energy_meas_low_threshold(line) 

			# set_energy_meas_high_threshold
			elif(line.startswith('set_energy_meas_high_threshold')):
				targetLib.set_energy_meas_high_threshold(line) 

			# set_energy_meas_time_extent
			elif(line.startswith('set_energy_meas_time_extent')):
				targetLib.set_energy_meas_time_extent(line) 

			# set_energy_meas_time_extent
			elif(line.startswith('set_operating_conditions')):
				targetLib.set_operating_conditions(line) 

#-- add function --#
			# add_cell
			elif(line.startswith('add_cell')):
				targetCell = mlc.MyLogicCell()
				targetCell.add_cell(line) 

			# add_flop
			elif(line.startswith('add_flop')):
				targetCell = mlc.MyLogicCell()
				targetCell.add_flop(line) 

			# add_flop
			elif(line.startswith('add_flop')):
				targetCell = mlc.MyLogicCell()
				targetCell.add_flop(line) 

			# add_slope
			elif(line.startswith('add_slope')):
				targetCell.add_slope(line) 

			# add_load
			elif(line.startswith('add_load')):
				targetCell.add_load(line) 

			# add_netlist
			elif(line.startswith('add_netlist')):
				targetCell.add_netlist(line) 

			# add_model
			elif(line.startswith('add_model')):
				targetCell.add_model(line) 

			# add_simulation_timestep
			elif(line.startswith('add_simulation_timestep')):
				targetCell.add_simulation_timestep(line) 
#-- execution --#
			# initialize
			elif(line.startswith('create')):
				initializeFiles(targetLib, targetCell) 

			# create
			elif(line.startswith('characterize')):
				harnessList2 = characterizeFiles(targetLib, targetCell) 
				os.chdir("../")
				#print(len(harnessList))

			# export
			elif(line.startswith('export')):
				me.exportFiles(targetLib, targetCell, harnessList2) 

			# exit
			elif(line.startswith('quit') or line.startswith('exit')):
				me.exitFiles(targetLib) 



def initializeFiles(targetLib, targetCell):
	# initialize working directory
	if os.path.exists(targetLib.work_dir):
		shutil.rmtree(targetLib.work_dir)
	os.mkdir(targetLib.work_dir)

def characterizeFiles(targetLib, targetCell):
	print ("characterize\n")
	os.chdir(targetLib.work_dir)

	# Branch to each logic function
	if(targetCell.logic == 'INV'):
		print ("INV\n")
		# [in0, in1, out0]
		expectationList2 = [['01','10'],['10','01']]
		return runCombIn1Out1(targetLib, targetCell, expectationList2,"neg")

	elif(targetCell.logic == 'AND2'):
		print ("AND2\n")
		# [in0, in1, out0]
		expectationList2 = [['01','1','01'],['10','1','10'],['1','01','01'],['1','10','10']]
		return runCombIn2Out1(targetLib, targetCell, expectationList2,"pos")

	elif(targetCell.logic == 'NAND2'):
		print ("NAND2\n")
		# [in0, in1, out0]
		expectationList2 = [['01','1','10'],['10','1','01'],['1','01','10'],['1','10','01']]
		return runCombIn2Out1(targetLib, targetCell, expectationList2,"neg")

	elif(targetCell.logic == 'NAND3'):
		print ("NAND3\n")
		# [in0, in1, in2, out0]
		expectationList2 = [['01','1','1','10'],['10','1','1','01'],\
												['1','01','1','10'],['1','10','1','01'],\
												['1','1','01','10'],['1','1','10','01']]
		return runCombIn3Out1(targetLib, targetCell, expectationList2,"neg")

	elif(targetCell.logic == 'NAND4'):
		print ("NAND4\n")
		# [in0, in1, in2, out0]
		expectationList2 = [['01','1','1','1','10'],['10','1','1','1','01'],\
												['1','01','1','1','10'],['1','10','1','1','01'],\
												['1','1','01','1','10'],['1','1','10','1','01'],\
												['1','1','1','01','10'],['1','1','1','10','01']]
		return runCombIn4Out1(targetLib, targetCell, expectationList2,"neg")

	elif(targetCell.logic == 'NOR2'):
		print ("NOR2\n")
		# [in0, in1, out0]
		expectationList2 = [['01','0','10'],['10','0','01'],['0','01','10'],['0','10','01']]
		return runCombIn2Out1(targetLib, targetCell, expectationList2,"neg")

	elif(targetCell.logic == 'NOR3'):
		print ("NOR3\n")
		# [in0, in1, out0]
		expectationList2 = [['01','0','0','10'],['10','0','0','01'],\
												['0','01','0','10'],['0','10','0','01'],\
												['0','0','01','10'],['0','0','10','01']]
		return runCombIn3Out1(targetLib, targetCell, expectationList2,"neg")

	elif(targetCell.logic == 'NOR4'):
		print ("NOR4\n")
		# [in0, in1, out0]
		expectationList2 = [['01','0','0','0','10'],['10','0','0','0','01'],\
												['0','01','0','0','10'],['0','10','0','0','01'],\
												['0','0','01','0','10'],['0','0','10','0','01'],\
												['0','0','0','01','10'],['0','0','0','10','01']]
		return runCombIn4Out1(targetLib, targetCell, expectationList2,"neg")

	elif(targetCell.logic == 'XOR2'):
		print ("XOR2\n")
		# [in0, in1, out0]
		expectationList2 = [['01','0','01'],['10','0','10'],\
												['01','1','10'],['10','1','01'],\
												['0','01','01'],['0','10','10'],\
												['1','01','10'],['1','10','01']]
		return runCombIn2Out1(targetLib, targetCell, expectationList2,"pos")

	elif(targetCell.logic == 'XNOR2'):
		print ("XNOR2\n")
		# [in0, in1, out0]
		expectationList2 = [['01','0','10'],['10','0','01'],\
												['01','1','01'],['10','1','10'],\
												['0','01','10'],['0','10','01'],\
												['1','01','01'],['1','10','10']]
		return runCombIn2Out1(targetLib, targetCell, expectationList2,"pos")

	elif(targetCell.logic == 'SEL2'):
		print ("SEL2\n")
		# [in0, in1, sel, out]
		expectationList2 = [['01','0','0','01'],['10','0','0','10'],\
												['0','01','1','01'],['0','10','1','10'],\
												['1','0','01','10'],['1','0','10','01'],\
												['0','1','01','01'],['0','1','10','10']]
		return runCombIn3Out1(targetLib, targetCell, expectationList2,"pos")


	# Branch to sequencial logics
	# DFF, both unate, async reset, async set
	elif(targetCell.logic == 'DFF_PCBU_ARAS'):
		print ("DFF, positive clock, both unate, async reset, async set\n")
		# D1 & C01 -> Q01 QN10
		# D0 & C01 -> Q10 QN01
		# R01      -> Q10 QN01
		# S01      -> Q01 QN10
		# 									 [D,   C,  S,   R,    Q,  QN]
		expectationList2 = [['1','01','0', '0', '01','10'], \
										  	['0','01','0', '0', '10','01'], \
										  	['0','0','01', '0', '01','10'], \
										  	['0','0', '0','01', '10','01']]
		# run spice deck for flop
		return runFlop(targetLib, targetCell, expectationList2)

	else:
		print ("Target logic:"+targetCell.logic+" is not registered for characterization!\n")
		print ("Add characterization function for this program! -> die\n")
		sys.exit()

def runFlop(targetLib, targetCell, expectationList2):
	# Harness #0
	targetHarness0 = mcar.MyConditionsAndResults() # Q_val 01
	targetHarness1 = mcar.MyConditionsAndResults() # QN_val 10
	targetHarness2 = mcar.MyConditionsAndResults() # Q_val 10
	targetHarness3 = mcar.MyConditionsAndResults() # QN_val 01
	targetHarness4 = mcar.MyConditionsAndResults() # SET Q_val 01
	targetHarness5 = mcar.MyConditionsAndResults() # SET QN_val 10
	targetHarness6 = mcar.MyConditionsAndResults() # RST Q_val 10
	targetHarness7 = mcar.MyConditionsAndResults() # RST QN_val 01
	D_val = None
	CLK_val = None
	SET_val = None
	RST_val = None
	Q_val = None
	QN_val = None

	# both unate, async reset, async set
	if(targetCell.logic == 'DFF_PCBU_ARAS'):
		D_val, CLK_val, SET_val, RST_val, Q_val, QN_val = expectationList2[0]
		targetHarness0.set_timing_type_seqRise()
		targetHarness0.set_timing_sense(non)
		targetHarness0.set_target_inport (targetCell.inports[0], D_val)
		targetHarness0.set_target_outport (targetCell.outports[0], targetCell.functions[0], Q_val)
		targetHarness0.set_nontarget_outport (targetCell.outports[1])
		targetHarness0.set_stable_inport (targetCell.clock, CLK_val)
		targetHarness0.set_stable_inport (targetCell.reset, RST_val)
		targetHarness0.set_stable_inport (targetCell.set, SET_val)
	
		spicef = "c2q1_"+str(targetCell.cell)+"_"\
					+str(targetCell.inports[0])+str(D_val)+"_"\
					+str(targetCell.clock)+str(CLK_val)+"_"\
					+str(targetCell.reset)+str(RST_val)+"_"\
					+str(targetCell.set)+str(SET_val)+"_"\
					+str(targetCell.outports[0])+str(Q_val)
		# run spice and store result
		runSpiceFlopDelay(targetLib, targetCell, targetHarness0, spicef)

def runSpiceFlopDelay(targetLib, targetCell, targetHarness, spicef):
		list2_prop =   []
		list2_tran =   []
		list2_estart = []
		list2_eend =   []
		for tmp_load in targetCell.load:
			tmp_list_prop =   []
			tmp_list_tran =   []
			tmp_list_estart = []
			tmp_list_eend =   []
			for tmp_slope in targetCell.slope:
				cap_line = ".param cap ="+str(tmp_load)+str(targetLib.capacitance_unit)+"\n"
				slew_line = ".param slew ="+str(tmp_slope)+str(targetLib.time_unit)+"\n"
				cslew_line = ".param cslew ="+str(targetCell.cslope)+str(targetLib.time_unit)+"\n"
				spicefo = str(spicef)+"_"+str(tmp_load)+"_"+str(tmp_slope)+".sp"

				res_prop_in_out, res_trans_out, res_energy_start, res_energy_end \
					= genFileFlop_trial1(targetLib, targetCell, targetHarness, cap_line, slew_line, cslew_line, spicefo)
#				print(str(res_prop_in_out)+" "+str(res_trans_out)+" "+str(res_energy_start)+" "+str(res_energy_end))
				tmp_list_prop.append(res_prop_in_out)
				tmp_list_tran.append(res_trans_out)
				tmp_list_estart.append(res_energy_start)
				tmp_list_eend.append(res_energy_end)
			list2_prop.append(tmp_list_prop)
			list2_tran.append(tmp_list_tran)
			list2_estart.append(tmp_list_estart)
			list2_eend.append(tmp_list_eend)

		#print(list2_prop)

		targetHarness.set_list2_prop(list2_prop)
		#targetHarness.print_list2_prop(targetCell.load, targetCell.slope)
		targetHarness.write_list2_prop(targetLib, targetCell.load, targetCell.slope)
		#targetHarness.print_lut_prop()
		targetHarness.set_list2_tran(list2_tran)
		#targetHarness.print_list2_tran(targetCell.load, targetCell.slope)
		targetHarness.write_list2_tran(targetLib, targetCell.load, targetCell.slope)
		#targetHarness.print_lut_tran()
##
## 
##
def runCombIn1Out1(targetLib, targetCell, expectationList2, unate):
	harnessList = []   # harness for each trial
	harnessList2 = []  # list of harnessList

	for trial in range(len(expectationList2)):
		tmp_Harness = mcar.MyConditionsAndResults()
		tmp_Harness.set_timing_type_comb()
		tmp_Harness.set_timing_sense(unate)
		tmp_inp0_val, tmp_outp0_val=expectationList2[trial]
		tmp_Harness.set_direction(tmp_outp0_val)
		#print ("**"+targetCell.outports[0]+" "+targetCell.functions[0]+" "+ tmp_outp0_val)
		tmp_Harness.set_target_outport (targetCell.outports[0], targetCell.functions[0], tmp_outp0_val)
		# case input0 is target input pin
		if ((tmp_inp0_val == '01') or (tmp_inp0_val == '10')):
			tmp_Harness.set_target_inport (targetCell.inports[0], tmp_inp0_val)
			tmp_Harness.set_stable_inport ("NULL", "NULL")
		else:
			print ("Illiegal input vector type!!\n")
			print ("Check logic definition of this program!!\n")
			
		#tmp_Harness.set_leak_inportval ("1")
		#tmp_Harness.set_nontarget_outport (targetCell.outports[0], "01")
		spicef = "delay1_"+str(targetCell.cell)+"_"+str(targetCell.inports[0])\
			+str(tmp_inp0_val)+"_"+str(targetCell.outports[0])+str(tmp_outp0_val)
		# run spice and store result
		runSpiceCombDelay(targetLib, targetCell, tmp_Harness, spicef)
		harnessList.append(tmp_Harness)
		harnessList2.append(harnessList)

	return harnessList2

def runCombIn2Out1(targetLib, targetCell, expectationList2, unate):
	harnessList = []
	harnessList2 = []

	for trial in range(len(expectationList2)):
		tmp_Harness = mcar.MyConditionsAndResults()
		tmp_Harness.set_timing_type_comb()
		tmp_Harness.set_timing_sense(unate)
		tmp_inp0_val, tmp_inp1_val, tmp_outp0_val=expectationList2[trial]
		tmp_Harness.set_direction(tmp_outp0_val)
		tmp_Harness.set_target_outport (targetCell.outports[0], targetCell.functions[0], tmp_outp0_val)
		# case input0 is target input pin
		if ((tmp_inp0_val == '01') or (tmp_inp0_val == '10')):
			tmp_Harness.set_target_inport (targetCell.inports[0], tmp_inp0_val)
			tmp_Harness.set_stable_inport (targetCell.inports[1], tmp_inp1_val)
		# case input0 is target input pin
		elif ((tmp_inp1_val == '01') or (tmp_inp1_val == '10')):
			tmp_Harness.set_target_inport (targetCell.inports[1], tmp_inp1_val)
			tmp_Harness.set_stable_inport (targetCell.inports[0], tmp_inp0_val)
		else:
			print ("Illiegal input vector type!!\n")
			print ("Check logic definition of this program!!\n")
			
		#tmp_Harness.set_leak_inportval ("1")
		#tmp_Harness.set_nontarget_outport (targetCell.outports[0], "01")
		spicef = "delay1_"+str(targetCell.cell)+"_"+str(targetCell.inports[0])\
			+str(tmp_inp0_val)+"_"+str(targetCell.inports[1])+str(tmp_inp1_val)\
			+"_"+str(targetCell.outports[0])+str(tmp_outp0_val)
		# run spice and store result
		runSpiceCombDelay(targetLib, targetCell, tmp_Harness, spicef)
		harnessList.append(tmp_Harness)
		harnessList2.append(harnessList)

	return harnessList2

def runCombIn3Out1(targetLib, targetCell, expectationList2, unate):
	harnessList = []
	harnessList2 = []

	for trial in range(len(expectationList2)):
		tmp_Harness = mcar.MyConditionsAndResults()
		tmp_Harness.set_timing_type_comb()
		tmp_Harness.set_timing_sense(unate)
		tmp_inp0_val, tmp_inp1_val, tmp_inp2_val, tmp_outp0_val=expectationList2[trial]
		tmp_Harness.set_direction(tmp_outp0_val)
		tmp_Harness.set_target_outport (targetCell.outports[0], targetCell.functions[0], tmp_outp0_val)
		# case input0 is target input pin
		if ((tmp_inp0_val == '01') or (tmp_inp0_val == '10')):
			tmp_Harness.set_target_inport (targetCell.inports[0], tmp_inp0_val)
			tmp_Harness.set_stable_inport (targetCell.inports[1], tmp_inp1_val)
			tmp_Harness.set_stable_inport (targetCell.inports[2], tmp_inp2_val)
		# case input1 is target input pin
		elif ((tmp_inp1_val == '01') or (tmp_inp1_val == '10')):
			tmp_Harness.set_target_inport (targetCell.inports[1], tmp_inp1_val)
			tmp_Harness.set_stable_inport (targetCell.inports[0], tmp_inp0_val)
			tmp_Harness.set_stable_inport (targetCell.inports[2], tmp_inp2_val)
		# case input2 is target input pin
		elif ((tmp_inp2_val == '01') or (tmp_inp2_val == '10')):
			tmp_Harness.set_target_inport (targetCell.inports[2], tmp_inp2_val)
			tmp_Harness.set_stable_inport (targetCell.inports[0], tmp_inp0_val)
			tmp_Harness.set_stable_inport (targetCell.inports[1], tmp_inp1_val)
		else:
			print ("Illiegal input vector type!!\n")
			print ("Check logic definition of this program!!\n")
			
		#tmp_Harness.set_leak_inportval ("1")
		#tmp_Harness.set_nontarget_outport (targetCell.outports[0], "01")
		spicef = "delay1_"+str(targetCell.cell)+"_"\
			+str(targetCell.inports[0])+str(tmp_inp0_val)\
			+"_"+str(targetCell.inports[1])+str(tmp_inp1_val)\
			+"_"+str(targetCell.inports[2])+str(tmp_inp2_val)\
			+"_"+str(targetCell.outports[0])+str(tmp_outp0_val)
		# run spice and store result
		runSpiceCombDelay(targetLib, targetCell, tmp_Harness, spicef)
		harnessList.append(tmp_Harness)
		harnessList2.append(harnessList)

	return harnessList2

def runCombIn4Out1(targetLib, targetCell, expectationList2, unate):
	harnessList = []
	harnessList2 = []

	for trial in range(len(expectationList2)):
		tmp_Harness = mcar.MyConditionsAndResults()
		tmp_Harness.set_timing_type_comb()
		tmp_Harness.set_timing_sense(unate)
		tmp_inp0_val, tmp_inp1_val, tmp_inp2_val, tmp_inp3_val, tmp_outp0_val=expectationList2[trial]
		tmp_Harness.set_direction(tmp_outp0_val)
		tmp_Harness.set_target_outport (targetCell.outports[0], targetCell.functions[0], tmp_outp0_val)
		# case input0 is target input pin
		if ((tmp_inp0_val == '01') or (tmp_inp0_val == '10')):
			tmp_Harness.set_target_inport (targetCell.inports[0], tmp_inp0_val)
			tmp_Harness.set_stable_inport (targetCell.inports[1], tmp_inp1_val)
			tmp_Harness.set_stable_inport (targetCell.inports[2], tmp_inp2_val)
			tmp_Harness.set_stable_inport (targetCell.inports[3], tmp_inp3_val)
		# case input1 is target input pin
		elif ((tmp_inp1_val == '01') or (tmp_inp1_val == '10')):
			tmp_Harness.set_target_inport (targetCell.inports[1], tmp_inp1_val)
			tmp_Harness.set_stable_inport (targetCell.inports[0], tmp_inp0_val)
			tmp_Harness.set_stable_inport (targetCell.inports[2], tmp_inp2_val)
			tmp_Harness.set_stable_inport (targetCell.inports[3], tmp_inp3_val)
		# case input2 is target input pin
		elif ((tmp_inp2_val == '01') or (tmp_inp2_val == '10')):
			tmp_Harness.set_target_inport (targetCell.inports[2], tmp_inp2_val)
			tmp_Harness.set_stable_inport (targetCell.inports[0], tmp_inp0_val)
			tmp_Harness.set_stable_inport (targetCell.inports[1], tmp_inp1_val)
			tmp_Harness.set_stable_inport (targetCell.inports[3], tmp_inp3_val)
		elif ((tmp_inp3_val == '01') or (tmp_inp3_val == '10')):
			tmp_Harness.set_target_inport (targetCell.inports[3], tmp_inp3_val)
			tmp_Harness.set_stable_inport (targetCell.inports[0], tmp_inp0_val)
			tmp_Harness.set_stable_inport (targetCell.inports[1], tmp_inp1_val)
			tmp_Harness.set_stable_inport (targetCell.inports[2], tmp_inp2_val)
		else:
			print ("Illiegal input vector type!!\n")
			print ("Check logic definition of this program!!\n")
			
		#tmp_Harness.set_leak_inportval ("1")
		#tmp_Harness.set_nontarget_outport (targetCell.outports[0], "01")
		spicef = "delay1_"+str(targetCell.cell)+"_"\
			+str(targetCell.inports[0])+str(tmp_inp0_val)\
			+"_"+str(targetCell.inports[1])+str(tmp_inp1_val)\
			+"_"+str(targetCell.inports[2])+str(tmp_inp2_val)\
			+"_"+str(targetCell.inports[3])+str(tmp_inp3_val)\
			+"_"+str(targetCell.outports[0])+str(tmp_outp0_val)
		# run spice and store result
		runSpiceCombDelay(targetLib, targetCell, tmp_Harness, spicef)
		harnessList.append(tmp_Harness)
		harnessList2.append(harnessList)

	return harnessList2

def runSpiceCombDelay(targetLib, targetCell, targetHarness, spicef):
		list2_prop =   []
		list2_tran =   []
		list2_estart = []
		list2_eend =   []
		for tmp_load in targetCell.load:
			tmp_list_prop =   []
			tmp_list_tran =   []
			tmp_list_estart = []
			tmp_list_eend =   []
			for tmp_slope in targetCell.slope:
				cap_line = ".param cap ="+str(tmp_load)+str(targetLib.capacitance_unit)+"\n"
				slew_line = ".param slew ="+str(tmp_slope)+str(targetLib.time_unit)+"\n"
				spicefo = str(spicef)+"_"+str(tmp_load)+"_"+str(tmp_slope)+".sp"

				res_prop_in_out, res_trans_out, res_energy_start, res_energy_end \
					= genFileLogic_trial1(targetLib, targetCell, targetHarness, cap_line, slew_line, spicefo)
#				print(str(res_prop_in_out)+" "+str(res_trans_out)+" "+str(res_energy_start)+" "+str(res_energy_end))
				tmp_list_prop.append(res_prop_in_out)
				tmp_list_tran.append(res_trans_out)
				tmp_list_estart.append(res_energy_start)
				tmp_list_eend.append(res_energy_end)
			list2_prop.append(tmp_list_prop)
			list2_tran.append(tmp_list_tran)
			list2_estart.append(tmp_list_estart)
			list2_eend.append(tmp_list_eend)

		#print(list2_prop)

		targetHarness.set_list2_prop(list2_prop)
		#targetHarness.print_list2_prop(targetCell.load, targetCell.slope)
		targetHarness.write_list2_prop(targetLib, targetCell.load, targetCell.slope)
		#targetHarness.print_lut_prop()
		targetHarness.set_list2_tran(list2_tran)
		#targetHarness.print_list2_tran(targetCell.load, targetCell.slope)
		targetHarness.write_list2_tran(targetLib, targetCell.load, targetCell.slope)
		#targetHarness.print_lut_tran()
		


def genFileLogic_trial1(targetLib, targetCell, targetHarness, cap_line, slew_line, spicef):
	#print (spicef)
	#print ("generate AND2\n")
	#print(dir(targetLib))
	with open(spicef,'w') as f:
		outlines = []
		outlines.append("*title: delay meas.\n")
		outlines.append(".option brief nopage nomod post=1 ingold=2 autostop\n")
		outlines.append(".inc '../"+str(targetCell.model)+"'\n")
		outlines.append(".inc '../"+str(targetCell.netlist)+"'\n")
		outlines.append(".param _vdd = "+str(targetLib.vdd_voltage)+"\n")
		outlines.append(".param _vss = "+str(targetLib.vss_voltage)+"\n")
		outlines.append(".param _vnw = "+str(targetLib.nwell_voltage)+"\n")
		outlines.append(".param _vpw = "+str(targetLib.pwell_voltage)+"\n")
		outlines.append(".param cap = 10f \n")
		outlines.append(".param slew = 100p \n")
		outlines.append(".param _tslew = slew\n")
		outlines.append(".param _tstart = slew\n")
		outlines.append(".param _tend = '_tstart + _tslew'\n")
		outlines.append(".param _tsimend = '_tslew * 100000' \n")
		outlines.append(" \n")
		outlines.append("VDD_DYN VDD_DYN 0 DC '_vdd' \n")
		outlines.append("VSS_DYN VSS_DYN 0 DC '_vss' \n")
		outlines.append("VNW_DYN VNW_DYN 0 DC '_vnw' \n")
		outlines.append("VPW_DYN VPW_DYN 0 DC '_vpw' \n")
		outlines.append("VDD_LEAK VDD_LEAK 0 DC '_vdd' \n")
		outlines.append("VSS_LEAK VSS_LEAK 0 DC '_vss' \n")
		outlines.append("VNW_LEAK VNW_LEAK 0 DC '_vnw' \n")
		outlines.append("VPW_LEAK VPW_LEAK 0 DC '_vpw' \n")
		outlines.append(" \n")
		# in auto mode, simulation timestep is 1/10 of min. input slew
		# simulation runs 1000x of input slew time
		outlines.append(".tran "+str(targetCell.simulation_timestep)+str(targetLib.time_unit)+" '_tsimend'\n")
		outlines.append(" \n")
		if(targetHarness.target_inport_val == "01"):
			outlines.append("VIN VIN 0 PWL(1p '_vss' '_tstart' '_vss' '_tend' '_vdd' '_tsimend' '_vdd') \n")
		elif(targetHarness.target_inport_val == "10"):
			outlines.append("VIN VIN 0 PWL(1p '_vdd' '_tstart' '_vdd' '_tend' '_vss' '_tsimend' '_vss') \n")
		elif(targetHarness.target_inport_val == "11"):
			outlines.append("VIN VIN 0 DC '_vdd' \n")
		elif(targetHarness.target_inport_val == "00"):
			outlines.append("VIN VIN 0 DC '_vss' \n")
		outlines.append("VHIGH VHIGH 0 DC '_vdd' \n")
		outlines.append("VLOW VLOW 0 DC '_vss' \n")

		outlines.append("** Delay \n")
		outlines.append("* Prop delay \n")
		if(targetHarness.target_inport_val == "01"):
			outlines.append(".measure Tran PROP_IN_OUT trig v(VIN) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
		elif(targetHarness.target_inport_val == "10"):
			outlines.append(".measure Tran PROP_IN_OUT trig v(VIN) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
		if(targetHarness.target_outport_val == "10"):
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
		elif(targetHarness.target_outport_val == "01"):
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
		outlines.append("* Trans delay \n")

		if(targetHarness.target_outport_val == "10"):
			outlines.append(".measure Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage))+"' fall=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage ))+"' fall=1 \n")
		elif(targetHarness.target_outport_val == "01"):
			outlines.append(".measure Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage ))+"' rise=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage))+"' rise=1 \n")

		outlines.append("* For energy calculation \n")
		if(targetHarness.target_inport_val == "01"):
			outlines.append(".measure Tran ENERGY_START when v(VIN)='"+str(targetLib.energy_meas_low_threshold)+"' rise=1 \n")
		elif(targetHarness.target_inport_val == "10"):
			outlines.append(".measure Tran ENERGY_START when v(VIN)='"+str(targetLib.energy_meas_high_threshold)+"' fall=1 \n")
		if(targetHarness.target_outport_val == "01"):
			outlines.append(".measure Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_high_threshold)+"' rise=1 \n")
		elif(targetHarness.target_outport_val == "10"):
			outlines.append(".measure Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_low_threshold)+"' fall=1 \n")

## for ngspice batch mode 
		outlines.append(".control \n")
		outlines.append("run \n")
		outlines.append("plot V(VIN) V(VOUT) \n")
		if(targetHarness.target_inport_val == "01"):
			outlines.append("meas Tran PROP_IN_OUT trig v(VIN) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
		elif(targetHarness.target_inport_val == "10"):
			outlines.append("meas Tran PROP_IN_OUT trig v(VIN) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
		if(targetHarness.target_outport_val == "10"):
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
		elif(targetHarness.target_outport_val == "01"):
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
		if(targetHarness.target_outport_val == "10"):
			outlines.append("meas Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage))+"' fall=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage ))+"' fall=1 \n")
		elif(targetHarness.target_outport_val == "01"):
			outlines.append("meas Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage ))+"' rise=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage))+"' rise=1 \n")
		if(targetHarness.target_inport_val == "01"):
			outlines.append("meas Tran ENERGY_START when v(VIN)='"+str(targetLib.energy_meas_low_threshold)+"' rise=1 \n")
		elif(targetHarness.target_inport_val == "10"):
			outlines.append("meas Tran ENERGY_START when v(VIN)='"+str(targetLib.energy_meas_high_threshold)+"' fall=1 \n")
		if(targetHarness.target_outport_val == "01"):
			outlines.append("meas Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_high_threshold)+"' rise=1 \n")
		elif(targetHarness.target_outport_val == "10"):
			outlines.append("meas Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_low_threshold)+"' fall=1 \n")
		outlines.append(".endc \n")

#		outlines.append("* \n")
#		outlines.append("** Capacitance \n")
#		outlines.append("* \n")
#		outlines.append(".measure Tran Cur_IN_rd integ i(VIN_rd) from='Start_rd' to='End_rd' print=0 \n")
#		outlines.append(".measure Cap_IN_rd param='abs(Cur_IN_rd/_Effect_volt)' \n")
#		outlines.append(".measure Tran Cur_IN_fd integ i(VIN_fd) from='Start_fd' to='End_fd' print=0 \n")
#		outlines.append(".measure Cap_IN_fd param='abs(Cur_IN_fd/_Effect_volt)' \n")
#		outlines.append(" \n")
#		outlines.append("* \n")
#		outlines.append("** Energy \n")
#		outlines.append("* \n")
#		outlines.append("* Internal energy (Internal Cap, Short-Circuit) \n")
#		outlines.append(".measure Tran Cur_Vdd_rd integ i(VDD_rd) from='Start_rd' to='End_rd*_Energy_meas_end_extent' print=0 \n")
#		outlines.append(".measure Tran Cur_Vss_rd integ i(VSS_rd) from='Start_rd' to='End_rd*_Energy_meas_end_extent' print=0 \n")
#		outlines.append("* select current source includes internal cap charge/discharge \n")
#		outlines.append(".measure Flag_cur_vdd_rd param='(abs(Cur_Vdd_rd)>abs(Cur_Vss_rd))' print=0 \n")
#		outlines.append(".measure Flag_cur_vss_rd param='(abs(Cur_Vss_rd)>abs(Cur_Vdd_rd))' print=0 \n")
#		outlines.append(" \n")
#		outlines.append("* Internal energy (Internal Cap, Short-Circuit) \n")
#		outlines.append(".measure Tran Cur_Vdd_fd integ i(VDD_fd) from='Start_fd' to='End_fd*_Energy_meas_end_extent' print=0 \n")
#		outlines.append(".measure Tran Cur_Vss_fd integ i(VSS_fd) from='Start_fd' to='End_fd*_Energy_meas_end_extent' print=0 \n")
#		outlines.append("* select current source includes internal cap charge/discharge \n")
#		outlines.append(".measure Flag_cur_vdd_fd param='(abs(Cur_Vdd_fd)>abs(Cur_Vss_fd))' print=0 \n")
#		outlines.append(".measure Flag_cur_vss_fd param='(abs(Cur_Vss_fd)>abs(Cur_Vdd_fd))' print=0 \n")
#		outlines.append("* calc internal power/energy \n")
#		outlines.append(".measure Power_rd param='(abs(Cur_Vdd_rd)*Flag_cur_vdd_rd + abs(Cur_Vss_rd)*Flag_cur_vss_rd)*_Effect_volt' print=1 \n")
#		outlines.append(".measure Power_fd param='(abs(Cur_Vdd_fd)*Flag_cur_vdd_fd + abs(Cur_Vss_fd)*Flag_cur_vss_fd)*_Effect_volt' print=1 \n")
#		outlines.append(".measure Energy_rd param='Power_rd/(End_rd - Start_rd)' print=1 \n")
#		outlines.append(".measure Energy_fd param='Power_fd/(End_fd - Start_fd)' print=1 \n")
#		outlines.append(" \n")
#		outlines.append("* Static energy \n")
#		outlines.append(".measure Tran Cur_Vdd_rs integ i(VDD_rs) from='Start_rd' to='End_rd' print=0 \n")
#		outlines.append(".measure Tran Cur_Vss_rs integ i(VSS_rs) from='Start_rd' to='End_rd' print=0 \n")
#		outlines.append(".measure Tran Cur_Vdd_fs integ i(VDD_fs) from='Start_fd' to='End_fd' print=0 \n")
#		outlines.append(".measure Tran Cur_Vss_fs integ i(VSS_fs) from='Start_fd' to='End_fd' print=0 \n")
#		outlines.append(" \n")
#		outlines.append(".measure Power_rs param='(abs(Cur_Vdd_rs) + abs(Cur_Vss_rs))/2*_Effect_volt' print=0 \n")
#		outlines.append(".measure Power_fs param='(abs(Cur_Vdd_fs) + abs(Cur_Vss_fs))/2*_Effect_volt' print=0 \n")
#		outlines.append(".measure Power_avg_rs param='Power_rs/(End_rd - Start_rd)' print=1 \n")
#		outlines.append(".measure Power_avg_fs param='Power_fs/(End_fd - Start_fd)' print=1 \n")
#		outlines.append(".measure Energy_rs param='Power_rs/(End_rd - Start_rd)' print=0 \n")
#		outlines.append(".measure Energy_fs param='Power_fs/(End_fd - Start_fd)' print=0 \n")
#		outlines.append(" \n")
#		outlines.append("* Gate leak \n")
#		outlines.append(".measure Tran Cur_IN_rs integ i(VIN_rs) from='Start_rd' to='End_rd' print=0 \n")
#		outlines.append(".measure Tran Cur_IN_fs integ i(VIN_fs) from='Start_fd' to='End_fd' print=0 \n")
#		outlines.append(".measure Power_gate_IN_rs param='abs(Cur_IN_rs*_Effect_volt)' print=0 \n")
#		outlines.append(".measure Power_gate_IN_fs param='abs(Cur_IN_fs*_Effect_volt)' print=0 \n")
#		outlines.append(".measure Power_gate_avg_IN_rs param='Power_gate_IN_rs/(End_rd - Start_rd)' print=1 \n")
#		outlines.append(".measure Power_gate_avg_IN_fs param='Power_gate_IN_fs/(End_fd - Start_fd)' print=1 \n")
#		outlines.append(".measure Energy_gate_IN_rs param='Power_gate_IN_rs/(End_rd - Start_rd)' print=0 \n")
#		outlines.append(".measure Energy_gate_IN_fs param='Power_gate_IN_fs/(End_fd - Start_fd)' print=0 \n")
#		outlines.append(" \n")
#		outlines.append(" \n")
		outlines.append("XINV VIN VOUT VHIGH VLOW VDD_DYN VSS_DYN VNW_DYN VPW_DYN DUT \n")
		outlines.append("C0 VOUT VSS_DYN cap\n")
		outlines.append(" \n")
		outlines.append(".SUBCKT DUT IN OUT HIGH LOW VDD VSS VNW VPW \n")
		# parse subckt definition
		tmp_array = targetCell.instance.split()
		tmp_line = tmp_array[0] # XDUT
		#print(tmp_line)
		for w1 in tmp_array:
			# match tmp_array and harness 
			# search target inport
			w2 = targetHarness.target_inport
			if(w1 == w2):
				tmp_line += ' IN'
			# search stable inport
			for w2 in targetHarness.stable_inport:
				if(w1 == w2):
					# this is stable inport
					# search index for this port
					index_val = targetHarness.stable_inport_val[targetHarness.stable_inport.index(w2)]
					if(index_val == '1'):
						tmp_line += ' HIGH'
					elif(index_val == '0'):
						tmp_line += ' LOW'
					else:
						print('Illigal input value for stable input\n')
			# search target outport
			#print("**"+targetHarness.target_outport[0])
			#print("**"+targetHarness.target_outport[1])
			for w2 in targetHarness.target_outport:
				#print(w1+" "+w2+"\n")
				if(w1 == w2):
					tmp_line += ' OUT'
			# search non-terget outport
			for w2 in targetHarness.nontarget_outport:
				if(w1 == w2):
					# this is non-terget outport
					# search outdex for this port
					index_val = targetHarness.nontarget_outport_val[targetHarness.nontarget_outport.index(w2)]
					tmp_line += ' WFLOAT'+str(index_val)
			if(w1.upper() == targetLib.vdd_name.upper()):
					tmp_line += ' '+w1.upper() 
			if(w1.upper() == targetLib.vss_name.upper()):
					tmp_line += ' '+w1.upper() 
			if(w1.upper() == targetLib.pwell_name.upper()):
					tmp_line += ' '+w1.upper() 
			if(w1.upper() == targetLib.nwell_name.upper()):
					tmp_line += ' '+w1.upper() 
					
		tmp_line += " "+str(tmp_array[len(tmp_array)-1])+"\n" # CIRCUIT NAME
		outlines.append(tmp_line)
		#print(tmp_line)

		outlines.append(".ends \n")
		outlines.append(" \n")
		outlines.append(cap_line)
		outlines.append(slew_line)
		outlines.append(cslew_line)
				
		outlines.append(".end \n") 
		f.writelines(outlines)
	f.close()

	spicelis = spicef
	spicelis += ".lis"

	# run simulation
	cmd = str(targetLib.simulator)+" -b "+str(spicef)+" 1> "+str(spicelis)+" 2> /dev/null \n"
	with open('run.sh','w') as f:
		outlines = []
		outlines.append(cmd) 
		f.writelines(outlines)
	f.close()

	cmd = ['sh', 'run.sh']
			
	try:
		res = subprocess.check_call(cmd)
	except:
		print ("Failed to lunch spice")

	# read results
	with open(spicelis,'r') as f:
		for inline in f:
			#print(inline)
			# search measure
			if(re.match("prop_in_out", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_prop_in_out = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("trans_out", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_trans_out = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("energy_start", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_energy_start = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("energy_end", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_energy_end = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)

	f.close()
	#print(str(res_prop_in_out)+" "+str(res_trans_out)+" "+str(res_energy_start)+" "+str(res_energy_end))
	# check spice finish successfully
	try:
		res_prop_in_out
	except NameError:
		print("Value res_prop_in_out is not defined!!\n")
		print("Check simulation result in work directory\n")
		sys.exit()
	try:
		res_trans_out
	except NameError:
		print("Value res_trans_out is not defined!!\n")
		print("Check simulation result in work directory\n")
		sys.exit()
	try:
		res_energy_start
	except NameError:
		print("Value res_energy_start is not defined!!\n")
		print("Check simulation result in work directory\n")
		sys.exit()
	try:
		res_energy_end
	except NameError:
		print("Value res_energy_end is not defined!!\n")
		print("Check simulation result in work directory\n")
		sys.exit()
	return res_prop_in_out, res_trans_out, res_energy_start, res_energy_end
	
def genFileFlop_trial1(targetLib, targetCell, targetHarness, cap_line, slew_line, cslew_line, spicef):
	#print (spicef)
	#print ("generate AND2\n")
	#print(dir(targetLib))
	with open(spicef,'w') as f:
		outlines = []
		outlines.append("*title: flop delay meas.\n")
		outlines.append(".option brief nopage nomod post=1 ingold=2 autostop\n")
		outlines.append(".inc '../"+str(targetCell.model)+"'\n")
		outlines.append(".inc '../"+str(targetCell.netlist)+"'\n")
		outlines.append(".param _vdd = "+str(targetLib.vdd_voltage)+"\n")
		outlines.append(".param _vss = "+str(targetLib.vss_voltage)+"\n")
		outlines.append(".param _vnw = "+str(targetLib.nwell_voltage)+"\n")
		outlines.append(".param _vpw = "+str(targetLib.pwell_voltage)+"\n")
		outlines.append(".param cap = 10f \n")
		outlines.append(".param slew = 100p \n")
		outlines.append(".param cslew = 100p \n")
		outlines.append(".param _tslew = slew\n")
		outlines.append(".param _tclk1 = slew\n")                # ^ first clock
		outlines.append(".param _tclk2 = '_tclk1 + cslew '\n")   # | 
		outlines.append(".param _tclk3 = '_tclk2 + slew '\n")    # | 
		outlines.append(".param _tclk4 = '_tclk3 + cslew '\n")   # v 
		outlines.append(".param _tstart1 = 'slew * 20 + dedge1'\n")    # ^ data input start 
		outlines.append(".param _tstart2 = '_tstart1 + _tslew'\n")     # v varied w/ dedge
		outlines.append(".param _tend1 = '_tstart2 + dedge2'\n")   # ^ data input end
		outlines.append(".param _tend2 = '_tend1 + _tslew'\n")     # v varied w/ dedge
		outlines.append(".param _tclk5 = _tstart1\n")            # ^ second clock
		outlines.append(".param _tclk6 = '_tclk5 + cslew '\n")   # | 
		outlines.append(".param _tclk3 = '_tclk2 + slew '\n")    # | 
		outlines.append(".param _tclk4 = '_tclk3 + cslew '\n")   # v 
		outlines.append(".param _tsimend = '_tslew * 100000' \n")
		outlines.append(" \n")
		outlines.append("VDD_DYN VDD_DYN 0 DC '_vdd' \n")
		outlines.append("VSS_DYN VSS_DYN 0 DC '_vss' \n")
		outlines.append("VNW_DYN VNW_DYN 0 DC '_vnw' \n")
		outlines.append("VPW_DYN VPW_DYN 0 DC '_vpw' \n")
		outlines.append("VDD_LEAK VDD_LEAK 0 DC '_vdd' \n")
		outlines.append("VSS_LEAK VSS_LEAK 0 DC '_vss' \n")
		outlines.append("VNW_LEAK VNW_LEAK 0 DC '_vnw' \n")
		outlines.append("VPW_LEAK VPW_LEAK 0 DC '_vpw' \n")
		outlines.append(" \n")
		# in auto mode, simulation timestep is 1/10 of min. input slew
		# simulation runs 1000x of input slew time
		outlines.append(".tran "+str(targetCell.simulation_timestep)+str(targetLib.time_unit)+" '_tsimend'\n")
		outlines.append(" \n")
		if(targetHarness.target_inport_val == "01"):
			outlines.append("VIN VIN 0 PWL(1p '_vss' '_tstart1' '_vss' '_tstart2' '_vdd' '_tend1' '_vdd' '_tend2' '_vss' '_tsimend' '_vss') \n")
		elif(targetHarness.target_inport_val == "10"):
			outlines.append("VIN VIN 0 PWL(1p '_vdd' '_tstart1' '_vdd' '_tstart2' '_vss' '_tend1' '_vss' '_tend2' '_vdd' '_tsimend' '_vdd') \n")
		elif(targetHarness.target_inport_val == "11"):
			outlines.append("VIN VIN 0 DC '_vdd' \n")
		elif(targetHarness.target_inport_val == "00"):
			outlines.append("VIN VIN 0 DC '_vss' \n")
		outlines.append("VHIGH VHIGH 0 DC '_vdd' \n")
		outlines.append("VLOW VLOW 0 DC '_vss' \n")

		outlines.append("** Delay \n")
		outlines.append("* Prop delay \n")
		if(targetHarness.target_inport_val == "01"):
			outlines.append(".measure Tran PROP_IN_OUT trig v(VIN) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
		elif(targetHarness.target_inport_val == "10"):
			outlines.append(".measure Tran PROP_IN_OUT trig v(VIN) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
		if(targetHarness.target_outport_val == "10"):
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
		elif(targetHarness.target_outport_val == "01"):
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
		outlines.append("* Trans delay \n")

		if(targetHarness.target_outport_val == "10"):
			outlines.append(".measure Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage))+"' fall=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage ))+"' fall=1 \n")
		elif(targetHarness.target_outport_val == "01"):
			outlines.append(".measure Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage ))+"' rise=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage))+"' rise=1 \n")

		outlines.append("* For energy calculation \n")
		if(targetHarness.target_inport_val == "01"):
			outlines.append(".measure Tran ENERGY_START when v(VIN)='"+str(targetLib.energy_meas_low_threshold)+"' rise=1 \n")
		elif(targetHarness.target_inport_val == "10"):
			outlines.append(".measure Tran ENERGY_START when v(VIN)='"+str(targetLib.energy_meas_high_threshold)+"' fall=1 \n")
		if(targetHarness.target_outport_val == "01"):
			outlines.append(".measure Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_high_threshold)+"' rise=1 \n")
		elif(targetHarness.target_outport_val == "10"):
			outlines.append(".measure Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_low_threshold)+"' fall=1 \n")

## for ngspice batch mode 
		outlines.append(".control \n")
		outlines.append("run \n")
		outlines.append("plot V(VIN) V(VOUT) \n")
		if(targetHarness.target_inport_val == "01"):
			outlines.append("meas Tran PROP_IN_OUT trig v(VIN) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
		elif(targetHarness.target_inport_val == "10"):
			outlines.append("meas Tran PROP_IN_OUT trig v(VIN) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
		if(targetHarness.target_outport_val == "10"):
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
		elif(targetHarness.target_outport_val == "01"):
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
		if(targetHarness.target_outport_val == "10"):
			outlines.append("meas Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage))+"' fall=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage ))+"' fall=1 \n")
		elif(targetHarness.target_outport_val == "01"):
			outlines.append("meas Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage ))+"' rise=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage))+"' rise=1 \n")
		if(targetHarness.target_inport_val == "01"):
			outlines.append("meas Tran ENERGY_START when v(VIN)='"+str(targetLib.energy_meas_low_threshold)+"' rise=1 \n")
		elif(targetHarness.target_inport_val == "10"):
			outlines.append("meas Tran ENERGY_START when v(VIN)='"+str(targetLib.energy_meas_high_threshold)+"' fall=1 \n")
		if(targetHarness.target_outport_val == "01"):
			outlines.append("meas Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_high_threshold)+"' rise=1 \n")
		elif(targetHarness.target_outport_val == "10"):
			outlines.append("meas Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_low_threshold)+"' fall=1 \n")
		outlines.append(".endc \n")

#		outlines.append("* \n")
#		outlines.append("** Capacitance \n")
#		outlines.append("* \n")
#		outlines.append(".measure Tran Cur_IN_rd integ i(VIN_rd) from='Start_rd' to='End_rd' print=0 \n")
#		outlines.append(".measure Cap_IN_rd param='abs(Cur_IN_rd/_Effect_volt)' \n")
#		outlines.append(".measure Tran Cur_IN_fd integ i(VIN_fd) from='Start_fd' to='End_fd' print=0 \n")
#		outlines.append(".measure Cap_IN_fd param='abs(Cur_IN_fd/_Effect_volt)' \n")
#		outlines.append(" \n")
#		outlines.append("* \n")
#		outlines.append("** Energy \n")
#		outlines.append("* \n")
#		outlines.append("* Internal energy (Internal Cap, Short-Circuit) \n")
#		outlines.append(".measure Tran Cur_Vdd_rd integ i(VDD_rd) from='Start_rd' to='End_rd*_Energy_meas_end_extent' print=0 \n")
#		outlines.append(".measure Tran Cur_Vss_rd integ i(VSS_rd) from='Start_rd' to='End_rd*_Energy_meas_end_extent' print=0 \n")
#		outlines.append("* select current source includes internal cap charge/discharge \n")
#		outlines.append(".measure Flag_cur_vdd_rd param='(abs(Cur_Vdd_rd)>abs(Cur_Vss_rd))' print=0 \n")
#		outlines.append(".measure Flag_cur_vss_rd param='(abs(Cur_Vss_rd)>abs(Cur_Vdd_rd))' print=0 \n")
#		outlines.append(" \n")
#		outlines.append("* Internal energy (Internal Cap, Short-Circuit) \n")
#		outlines.append(".measure Tran Cur_Vdd_fd integ i(VDD_fd) from='Start_fd' to='End_fd*_Energy_meas_end_extent' print=0 \n")
#		outlines.append(".measure Tran Cur_Vss_fd integ i(VSS_fd) from='Start_fd' to='End_fd*_Energy_meas_end_extent' print=0 \n")
#		outlines.append("* select current source includes internal cap charge/discharge \n")
#		outlines.append(".measure Flag_cur_vdd_fd param='(abs(Cur_Vdd_fd)>abs(Cur_Vss_fd))' print=0 \n")
#		outlines.append(".measure Flag_cur_vss_fd param='(abs(Cur_Vss_fd)>abs(Cur_Vdd_fd))' print=0 \n")
#		outlines.append("* calc internal power/energy \n")
#		outlines.append(".measure Power_rd param='(abs(Cur_Vdd_rd)*Flag_cur_vdd_rd + abs(Cur_Vss_rd)*Flag_cur_vss_rd)*_Effect_volt' print=1 \n")
#		outlines.append(".measure Power_fd param='(abs(Cur_Vdd_fd)*Flag_cur_vdd_fd + abs(Cur_Vss_fd)*Flag_cur_vss_fd)*_Effect_volt' print=1 \n")
#		outlines.append(".measure Energy_rd param='Power_rd/(End_rd - Start_rd)' print=1 \n")
#		outlines.append(".measure Energy_fd param='Power_fd/(End_fd - Start_fd)' print=1 \n")
#		outlines.append(" \n")
#		outlines.append("* Static energy \n")
#		outlines.append(".measure Tran Cur_Vdd_rs integ i(VDD_rs) from='Start_rd' to='End_rd' print=0 \n")
#		outlines.append(".measure Tran Cur_Vss_rs integ i(VSS_rs) from='Start_rd' to='End_rd' print=0 \n")
#		outlines.append(".measure Tran Cur_Vdd_fs integ i(VDD_fs) from='Start_fd' to='End_fd' print=0 \n")
#		outlines.append(".measure Tran Cur_Vss_fs integ i(VSS_fs) from='Start_fd' to='End_fd' print=0 \n")
#		outlines.append(" \n")
#		outlines.append(".measure Power_rs param='(abs(Cur_Vdd_rs) + abs(Cur_Vss_rs))/2*_Effect_volt' print=0 \n")
#		outlines.append(".measure Power_fs param='(abs(Cur_Vdd_fs) + abs(Cur_Vss_fs))/2*_Effect_volt' print=0 \n")
#		outlines.append(".measure Power_avg_rs param='Power_rs/(End_rd - Start_rd)' print=1 \n")
#		outlines.append(".measure Power_avg_fs param='Power_fs/(End_fd - Start_fd)' print=1 \n")
#		outlines.append(".measure Energy_rs param='Power_rs/(End_rd - Start_rd)' print=0 \n")
#		outlines.append(".measure Energy_fs param='Power_fs/(End_fd - Start_fd)' print=0 \n")
#		outlines.append(" \n")
#		outlines.append("* Gate leak \n")
#		outlines.append(".measure Tran Cur_IN_rs integ i(VIN_rs) from='Start_rd' to='End_rd' print=0 \n")
#		outlines.append(".measure Tran Cur_IN_fs integ i(VIN_fs) from='Start_fd' to='End_fd' print=0 \n")
#		outlines.append(".measure Power_gate_IN_rs param='abs(Cur_IN_rs*_Effect_volt)' print=0 \n")
#		outlines.append(".measure Power_gate_IN_fs param='abs(Cur_IN_fs*_Effect_volt)' print=0 \n")
#		outlines.append(".measure Power_gate_avg_IN_rs param='Power_gate_IN_rs/(End_rd - Start_rd)' print=1 \n")
#		outlines.append(".measure Power_gate_avg_IN_fs param='Power_gate_IN_fs/(End_fd - Start_fd)' print=1 \n")
#		outlines.append(".measure Energy_gate_IN_rs param='Power_gate_IN_rs/(End_rd - Start_rd)' print=0 \n")
#		outlines.append(".measure Energy_gate_IN_fs param='Power_gate_IN_fs/(End_fd - Start_fd)' print=0 \n")
#		outlines.append(" \n")
#		outlines.append(" \n")
		outlines.append("XINV VIN VOUT VHIGH VLOW VDD_DYN VSS_DYN VNW_DYN VPW_DYN DUT \n")
		outlines.append("C0 VOUT VSS_DYN cap\n")
		outlines.append(" \n")
		outlines.append(".SUBCKT DUT IN OUT HIGH LOW VDD VSS VNW VPW \n")
		# parse subckt definition
		tmp_array = targetCell.instance.split()
		tmp_line = tmp_array[0] # XDUT
		#print(tmp_line)
		for w1 in tmp_array:
			# match tmp_array and harness 
			# search target inport
			w2 = targetHarness.target_inport
			if(w1 == w2):
				tmp_line += ' IN'
			# search stable inport
			for w2 in targetHarness.stable_inport:
				if(w1 == w2):
					# this is stable inport
					# search index for this port
					index_val = targetHarness.stable_inport_val[targetHarness.stable_inport.index(w2)]
					if(index_val == '1'):
						tmp_line += ' HIGH'
					elif(index_val == '0'):
						tmp_line += ' LOW'
					else:
						print('Illigal input value for stable input\n')
			# search target outport
			#print("**"+targetHarness.target_outport[0])
			#print("**"+targetHarness.target_outport[1])
			for w2 in targetHarness.target_outport:
				#print(w1+" "+w2+"\n")
				if(w1 == w2):
					tmp_line += ' OUT'
			# search non-terget outport
			for w2 in targetHarness.nontarget_outport:
				if(w1 == w2):
					# this is non-terget outport
					# search outdex for this port
					index_val = targetHarness.nontarget_outport_val[targetHarness.nontarget_outport.index(w2)]
					tmp_line += ' WFLOAT'+str(index_val)
			if(w1.upper() == targetLib.vdd_name.upper()):
					tmp_line += ' '+w1.upper() 
			if(w1.upper() == targetLib.vss_name.upper()):
					tmp_line += ' '+w1.upper() 
			if(w1.upper() == targetLib.pwell_name.upper()):
					tmp_line += ' '+w1.upper() 
			if(w1.upper() == targetLib.nwell_name.upper()):
					tmp_line += ' '+w1.upper() 
					
		tmp_line += " "+str(tmp_array[len(tmp_array)-1])+"\n" # CIRCUIT NAME
		outlines.append(tmp_line)
		#print(tmp_line)

		outlines.append(".ends \n")
		outlines.append(" \n")
		outlines.append(cap_line)
		outlines.append(slew_line)
				
		outlines.append(".end \n") 
		f.writelines(outlines)
	f.close()

	spicelis = spicef
	spicelis += ".lis"

	# run simulation
	cmd = str(targetLib.simulator)+" -b "+str(spicef)+" 1> "+str(spicelis)+" 2> /dev/null \n"
	with open('run.sh','w') as f:
		outlines = []
		outlines.append(cmd) 
		f.writelines(outlines)
	f.close()

	cmd = ['sh', 'run.sh']
			
	try:
		res = subprocess.check_call(cmd)
	except:
		print ("Failed to lunch spice")

	# read results
	with open(spicelis,'r') as f:
		for inline in f:
			#print(inline)
			# search measure
			if(re.match("prop_in_out", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_prop_in_out = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("trans_out", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_trans_out = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("energy_start", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_energy_start = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("energy_end", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_energy_end = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)

	f.close()
	#print(str(res_prop_in_out)+" "+str(res_trans_out)+" "+str(res_energy_start)+" "+str(res_energy_end))
	# check spice finish successfully
	try:
		res_prop_in_out
	except NameError:
		print("Value res_prop_in_out is not defined!!\n")
		print("Check simulation result in work directory\n")
		sys.exit()
	try:
		res_trans_out
	except NameError:
		print("Value res_trans_out is not defined!!\n")
		print("Check simulation result in work directory\n")
		sys.exit()
	try:
		res_energy_start
	except NameError:
		print("Value res_energy_start is not defined!!\n")
		print("Check simulation result in work directory\n")
		sys.exit()
	try:
		res_energy_end
	except NameError:
		print("Value res_energy_end is not defined!!\n")
		print("Check simulation result in work directory\n")
		sys.exit()
	return res_prop_in_out, res_trans_out, res_energy_start, res_energy_end
	
#
#
#
#

def my_error(line):
	print(line)


if __name__ == '__main__':
 main()

