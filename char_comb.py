import argparse, re, os, shutil, subprocess, sys, inspect 

import myConditionsAndResults as mcar
import myLibrarySetting as mls 
import myLogicCell as mlc
import myExport as me
import numpy as np
from myFunc import my_exit

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
#end runCombIn1Out1
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
#end runCombIn2Out1

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
#end runCombIn3Out1
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
#end  runCombIn4Out1

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
