import argparse, re, os, shutil, subprocess, sys, inspect 

import myConditionsAndResults as mcar
import myLibrarySetting as mls 
import myLogicCell as mlc
import myExport as me
import numpy as np
from myFunc import my_exit

def runFlop(targetLib, targetCell, expectationList2):
	harnessList = []   # harness for each trial
	harnessList2 = []  # list of harnessList

	D_val = None
	CLK_val = None
	SET_val = None
	RST_val = None
	Q_val = None

	for trial in range(len(expectationList2)):
		tmp_Harness = mcar.MyConditionsAndResults() 
		if(targetCell.logic == 'DFF_PCPU_NRNS'):
			D_val, CLK_val, SET_val, RST_val, Q_val = expectationList2[trial]
		elif(targetCell.logic == 'DFF_PCPU_NR'):
			D_val, CLK_val, RST_val, Q_val = expectationList2[trial]
		else:
			print("Error! target cell "+str(targetCell.logic)+" is not defined!")
			my_exit()


		tmp_Harness.set_target_inport (targetCell.inports[0], D_val)
		tmp_Harness.set_target_outport (targetCell.outports[0], targetCell.functions[0], Q_val)
		tmp_Harness.set_target_clock (targetCell.clock, CLK_val)
		#tmp_Harness.set_nontarget_outport (targetCell.outports[1])
		tmp_Harness.set_timing_flop_clock(CLK_val)

		# select simulation type: clock(D2Q, D2C, C2Q, C2D), reset, set
		# normal operation (clock edge)
		if((CLK_val == '01') or (CLK_val == '10')):
			tmp_Harness.set_timing_flop_inout(D_val, Q_val)
		# reset operation (reset edge)
		elif((RST_val == '01') or (RST_val == '10')):
			tmp_Harness.set_timing_flop_reset(RST_val, Q_val)
		# set operation (set edge)
		elif((SET_val == '01') or (SET_val == '10')):
			tmp_Harness.set_timing_flop_set(SET_val, Q_val)
		else:
			print("any input vector is inputted! error\n")
			my_exit()

		# activate RST and SET if defined
		#print("RST:"+str(RST_val))
		#print("SET:"+str(SET_val))
		if((RST_val != None)and(SET_val != None)):
			tmp_Harness.set_target_set (targetCell.set, SET_val)
			tmp_Harness.set_target_reset (targetCell.reset, RST_val)
			spicef = "c2q1_"+str(targetCell.cell)+"_"\
					+str(targetCell.inports[0])+str(D_val)+"_"\
					+str(targetCell.clock)+str(CLK_val)+"_"\
					+str(targetCell.set)+str(SET_val)+"_"\
					+str(targetCell.reset)+str(RST_val)+"_"\
					+str(targetCell.outports[0])+str(Q_val)
		elif(SET_val != None):
			tmp_Harness.set_target_set (targetCell.set, SET_val)
			spicef = "c2q1_"+str(targetCell.cell)+"_"\
					+str(targetCell.inports[0])+str(D_val)+"_"\
					+str(targetCell.clock)+str(CLK_val)+"_"\
					+str(targetCell.set)+str(SET_val)+"_"\
					+str(targetCell.outports[0])+str(Q_val)
		elif(RST_val != None):
			tmp_Harness.set_target_reset (targetCell.reset, RST_val)
			spicef = "c2q1_"+str(targetCell.cell)+"_"\
					+str(targetCell.inports[0])+str(D_val)+"_"\
					+str(targetCell.clock)+str(CLK_val)+"_"\
					+str(targetCell.reset)+str(RST_val)+"_"\
					+str(targetCell.outports[0])+str(Q_val)
		else:	
			spicef = "c2q1_"+str(targetCell.cell)+"_"\
					+str(targetCell.inports[0])+str(D_val)+"_"\
					+str(targetCell.clock)+str(CLK_val)+"_"\
					+str(targetCell.outports[0])+str(Q_val)

		# run spice and store result
		runSpiceFlopDelay(targetLib, targetCell, tmp_Harness, spicef)
		harnessList.append(tmp_Harness)
		harnessList2.append(harnessList)

	return harnessList2

def runSpiceFlopDelay(targetLib, targetCell, targetHarness, spicef):
		list2_prop =   []
		list2_setup =   []
		list2_hold =   []
		list2_tran =   []
		list2_estart = []
		list2_eend =   []
		for tmp_load in targetCell.load:
			tmp_list_prop =   []  # C2Q
			tmp_list_setup =  []  # D2C(setup)
			tmp_list_hold =   []  # C2D(hold)
			tmp_list_tran =   []
			tmp_list_estart = []
			tmp_list_eend =   []
			for tmp_slope in targetCell.slope:
				tmp_max_val_loop = 100
				tmp_min_prop_in_out   = tmp_max_val_loop # temporal value for D2Qmin search
				tmp_min_prop_cin_out  = tmp_max_val_loop # temporal value for D2Qmin search
				tmp_min_trans_out     = tmp_max_val_loop # temporal value for D2Qmin search
				tmp_min_energy_start  = tmp_max_val_loop # temporal value for D2Qmin search
				tmp_min_energy_end    = tmp_max_val_loop # temporal value for D2Qmin search
				tmp_min_setup = tmp_max_val_loop # temporal value for setup 
				tmp_min_hold  = tmp_max_val_loop # temporal value for setup 
				# C2Q and setup search
				#print ("targetCell.sim_setup_lowest: "+  str(targetCell.sim_setup_lowest ))
				#print ("targetCell.sim_setup_highest: "+ str(targetCell.sim_setup_highest))
				#print ("targetCell.sim_setup_timestep: "+str(targetCell.sim_setup_timestep))
				for tsetup in np.arange (targetCell.sim_setup_lowest, targetCell.sim_setup_highest, targetCell.sim_setup_timestep):
					print("tsetup: "+str(f'{tsetup:,.4f}'))
					cap_line = ".param cap ="+str(tmp_load)+str(targetLib.capacitance_unit)+"\n"
					slew_line = ".param slew ="+str(tmp_slope)+str(targetLib.time_unit)+"\n"
					cslew_line = ".param cslew ="+str(targetCell.cslope)+str(targetLib.time_unit)+"\n"
					tsetup_line = ".param tsetup ="+str(tsetup)+str(targetLib.time_unit)+"\n"
					thold_line = ".param thold ="+str(tmp_min_hold)+str(targetLib.time_unit)+"\n"
					spicefo = str(spicef)+"_"+str(tmp_load)+"_"+str(tmp_slope)+"_setup"+str(f'{tsetup:,.4f}')+"_hold"+str(f'{tmp_min_hold:,.4f}')+".sp"
          
					res_prop_in_out, res_prop_cin_out, res_trans_out, res_energy_start, res_energy_end, res_setup, res_hold,\
						= genFileFlop_trial1(targetLib, targetCell, targetHarness, cap_line, slew_line, cslew_line,\
																tsetup_line, thold_line, spicefo)
					
					# if (current D2Q > prev. D2Q), exceeds min D2Q
					if((res_prop_cin_out == "failed")or(float(res_prop_cin_out) > tmp_min_prop_cin_out)):
						if(tmp_max_val_loop == tmp_min_prop_cin_out):
							print("Error: simulation failed! Check spice deck!")
							print("spice deck:"+spicefo)
							my_exit()
						print("Min. D2Q found. Break loop at tsetup: "+str(f'{tsetup:,.4f}'))
						break
					
					# update C2Q(res_prop_in_out) 
					tmp_min_prop_in_out  = float(res_prop_in_out)
					tmp_min_prop_cin_out = float(res_prop_cin_out)
					tmp_min_trans_out    = float(res_trans_out)
					tmp_min_energy_start = float(res_energy_start)
					tmp_min_energy_end   = float(res_energy_end)
					tmp_min_setup = float(res_setup)
					tmp_min_hold = float(res_hold)

				#tmp_list_prop.append(tmp_min_prop_in_out) # store D2Q 
				tmp_list_prop.append(tmp_min_prop_cin_out) # store C2Q (not D2Q)
				tmp_list_setup.append(tmp_min_setup)
				tmp_list_hold.append(tmp_min_hold)
				tmp_list_tran.append(tmp_min_trans_out)
				tmp_list_estart.append(tmp_min_energy_start)
				tmp_list_eend.append(tmp_min_energy_end)
			list2_prop.append(tmp_list_prop)
			list2_setup.append(tmp_list_setup)
			list2_hold.append(tmp_list_hold)
			list2_tran.append(tmp_list_tran)
			list2_estart.append(tmp_list_estart)
			list2_eend.append(tmp_list_eend)

		#print(list2_prop)

		targetHarness.set_list2_prop(list2_prop)
		#targetHarness.print_list2_prop(targetCell.load, targetCell.slope)
		targetHarness.write_list2_prop(targetLib, targetCell.load, targetCell.slope)
		#targetHarness.print_lut_prop()
		targetHarness.set_list2_setup(list2_setup)
		#targetHarness.print_list2_setup(targetCell.load, targetCell.slope)
		targetHarness.write_list2_setup(targetLib, targetCell.load, targetCell.slope)
		#targetHarness.print_lut_setup()
		targetHarness.set_list2_hold(list2_hold)
		#targetHarness.print_list2_hold(targetCell.load, targetCell.slope)
		targetHarness.write_list2_hold(targetLib, targetCell.load, targetCell.slope)
		#targetHarness.print_lut_hold()
		targetHarness.set_list2_tran(list2_tran)
		#targetHarness.print_list2_tran(targetCell.load, targetCell.slope)
		targetHarness.write_list2_tran(targetLib, targetCell.load, targetCell.slope)
		#targetHarness.print_lut_tran()
		

def genFileFlop_trial1(targetLib, targetCell, targetHarness, cap_line, slew_line, cslew_line, tsetup_line, thold_line, spicef):
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
		outlines.append(".param tsetup = 100p \n")
		outlines.append(".param thold = 100p \n")
		outlines.append(".param _tslew = slew\n")
		outlines.append(".param _tclk1 = slew\n")                # ^ first clock
		outlines.append(".param _tclk2 = '_tclk1 + cslew '\n")   # | 
		outlines.append(".param _tclk3 = '_tclk2 + slew * 10 '\n")    # | 
		outlines.append(".param _tclk4 = '_tclk3 + cslew '\n")   # v 
		outlines.append(".param _tstart1 = 'slew * 30 + tsetup'\n")    # ^ data input start 
		outlines.append(".param _tstart2 = '_tstart1 + _tslew'\n")     # v varied w/ dedge
		outlines.append(".param _tend1 = '_tstart2 + thold'\n")   # ^ data input end
		outlines.append(".param _tend2 = '_tend1 + _tslew'\n")    # v varied w/ dedge
		outlines.append(".param _tclk5 = 'slew * 30'\n")             # ^ second clock
		outlines.append(".param _tclk6 = '_tclk5 + cslew '\n")    # v 
		outlines.append(".param _tsimend = '_tslew * 1000' \n")
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
		# target Vinput
		V_in_target = None 
		
		# DATA
		if(targetHarness.target_inport_val == "01"):
			outlines.append("VIN VIN 0 PWL(0 '_vss' '_tstart1' '_vss' '_tstart2' '_vdd' '_tend1' '_vdd' '_tend2' '_vss' '_tsimend' '_vss') \n")
			V_in_target = 'VIN'
		elif(targetHarness.target_inport_val == "10"):
			outlines.append("VIN VIN 0 PWL(0 '_vdd' '_tstart1' '_vdd' '_tstart2' '_vss' '_tend1' '_vss' '_tend2' '_vdd' '_tsimend' '_vdd') \n")
			V_in_target = 'VIN'
		elif((targetHarness.target_inport_val == "1") or (targetHarness.target_inport_val == "11")):
			outlines.append("VIN VIN 0 DC '_vdd' \n")
		elif((targetHarness.target_inport_val == "0") or (targetHarness.target_inport_val == "00")):
			outlines.append("VIN VIN 0 DC '_vss' \n")
		else:
			print("Error: no VIN difinition!")
			my_exit()
		outlines.append("VHIGH VHIGH 0 DC '_vdd' \n")
		outlines.append("VLOW VLOW 0 DC '_vss' \n")

		# CLOCK
		if(targetHarness.target_clock_val == "01"):
			outlines.append("VCIN VCIN 0 PWL(0 '_vss' '_tclk1' '_vss' '_tclk2' '_vdd' '_tclk3' '_vdd' '_tclk4' '_vss' '_tclk5' '_vss' '_tclk6' '_vdd' '_tsimend' '_vdd') \n")
			#V_in_target = 'VCIN'
		elif(targetHarness.target_clock_val == "10"):
			outlines.append("VCIN VCIN 0 PWL(0 '_vdd' '_tclk1' '_vdd' '_tclk2' '_vss' '_tclk3' '_vss' '_tclk4' '_vdd' '_tclk5' '_vdd' '_tclk6' '_vss' '_tsimend' '_vss') \n")
			#V_in_target = 'VCIN'
		elif((targetHarness.target_clock_val == "11")or(targetHarness.target_clock_val == "1")):
			outlines.append("VCIN VCIN 0 DC '_vdd' \n")
		elif((targetHarness.target_clock_val == "00")or(targetHarness.target_clock_val == "0")):
			outlines.append("VCIN VCIN 0 DC '_vss' \n")
		else:
			print("Error: no VCIN difinition!")
			my_exit()
		
		# RST
		if(targetHarness.target_reset_val == "01"):
			outlines.append("VRIN VRIN 0 PWL(0 '_vss' '_tstart1' '_vss' '_tstart2' '_vdd' '_tend1' '_vdd' '_tend2' '_vss' '_tsimend' '_vss') \n")
			V_in_target = 'VRIN'
		elif(targetHarness.target_reset_val == "10"):
			outlines.append("VRIN VRIN 0 PWL(0 '_vdd' '_tstart1' '_vdd' '_tstart2' '_vss' '_tend1' '_vss' '_tend2' '_vdd' '_tsimend' '_vdd') \n")
			V_in_target = 'VRIN'
		elif((targetHarness.target_reset_val == "11")or(targetHarness.target_reset_val == "1")):
			outlines.append("VRIN VRIN 0 DC '_vdd' \n")
		elif((targetHarness.target_reset_val == "00")or(targetHarness.target_reset_val == "0")):
			outlines.append("VRIN VRIN 0 DC '_vss' \n")
		elif(targetHarness.target_reset != None):
			print("Error: Reset is difined as "+str(targetHarness.target_reset)+" but not VRIN is not defined!")
			my_exit()

		# SET
		if(targetHarness.target_set_val == "01"):
			outlines.append("VSIN VSIN 0 PWL(0 '_vss' '_tstart1' '_vss' '_tstart2' '_vdd' '_tend1' '_vdd' '_tend2' '_vss' '_tsimend' '_vss') \n")
			V_in_target = 'VSIN'
		elif(targetHarness.target_set_val == "10"):
			outlines.append("VSIN VSIN 0 PWL(0 '_vdd' '_tstart1' '_vdd' '_tstart2' '_vss' '_tend1' '_vss' '_tend2' '_vdd' '_tsimend' '_vdd') \n")
			V_in_target = 'VSIN'
		elif((targetHarness.target_set_val == "11")or(targetHarness.target_set_val == "1")):
			outlines.append("VSIN VSIN 0 DC '_vdd' \n")
		elif((targetHarness.target_set_val == "00")or(targetHarness.target_set_val == "0")):
			outlines.append("VSIN VSIN 0 DC '_vss' \n")
		elif(targetHarness.target_set != None):
			print("Error: Set is difined as "+str(targetHarness.target_set)+" but not VSIN is not defined!")
			my_exit()

		# candidate of input: D, RST, SET
		# measure D2Q
		outlines.append("** Delay \n")
		outlines.append("* Prop delay (D2Q)\n")
		# case, input 01 -> output 10
		if(((targetHarness.target_inport_val == "01")or(targetHarness.target_set_val == "01")or(targetHarness.target_reset_val == "01"))and(targetHarness.target_outport_val == "10")):
			outlines.append(".measure Tran PROP_IN_OUT trig v("+V_in_target+") val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n") 
			outlines.append(".measure Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage))+"' fall=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage ))+"' fall=1 \n")
			outlines.append(".measure Tran ENERGY_START when v("+V_in_target+")='"+str(targetLib.energy_meas_low_threshold)+"' rise=1 \n")
			outlines.append(".measure Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_low_threshold)+"' fall=1 \n")
		# case, input 01 -> output 01
		elif(((targetHarness.target_inport_val == "01")or(targetHarness.target_set_val == "01")or(targetHarness.target_reset_val == "01"))and(targetHarness.target_outport_val == "01")):
			outlines.append(".measure Tran PROP_IN_OUT trig v("+V_in_target+") val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n") 
			outlines.append(".measure Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage))+"' rise=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage ))+"' rise=1 \n")
			outlines.append(".measure Tran ENERGY_START when v("+V_in_target+")='"+str(targetLib.energy_meas_low_threshold)+"' rise=1 \n")
			outlines.append(".measure Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_high_threshold)+"' rise=1 \n")
		# case, input 10 -> output 01
		elif(((targetHarness.target_inport_val == "10")or(targetHarness.target_set_val == "10")or(targetHarness.target_reset_val == "10"))and(targetHarness.target_outport_val == "01")):
			outlines.append(".measure Tran PROP_IN_OUT trig v("+V_in_target+") val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
			outlines.append(".measure Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage))+"' rise=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage ))+"' rise=1 \n")
			outlines.append(".measure Tran ENERGY_START when v("+V_in_target+")='"+str(targetLib.energy_meas_high_threshold)+"' fall=1 \n")
			outlines.append(".measure Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_high_threshold)+"' rise=1 \n")
		# case, input 10 -> output 10
		elif(((targetHarness.target_inport_val == "10")or(targetHarness.target_set_val == "10")or(targetHarness.target_reset_val == "10"))and(targetHarness.target_outport_val == "10")):
			outlines.append(".measure Tran PROP_IN_OUT trig v("+V_in_target+") val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
			outlines.append(".measure Tran TRANS_OUT trig v(VOUT) val='"+str(float(targetLib.logic_threshold_high)*float(targetLib.vdd_voltage))+"' fall=1\n")
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_threshold_low)*float(targetLib.vdd_voltage ))+"' fall=1 \n")
			outlines.append(".measure Tran ENERGY_START when v("+V_in_target+")='"+str(targetLib.energy_meas_high_threshold)+"' fall=1 \n")
			outlines.append(".measure Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_low_threshold)+"' fall=1 \n")
		else:
			print ("Target input of DFF is not registered for characterization!, die!")
			print ("inport_val:"+str(targetHarness.target_inport_val))
			print ("set_val:"+str(targetHarness.target_set_val))
			print ("reset_val:"+str(targetHarness.target_reset_val))
			print ("outport_val:"+str(targetHarness.target_outport_val))
			my_exit()

		outlines.append("* Prop delay (C2Q)\n")
		# case, clock 01 -> output 10
		if((targetHarness.target_clock_val == "01")and(targetHarness.target_outport_val == "10")):
			outlines.append(".measure Tran PROP_CIN_OUT trig v(VCIN) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=2 \n") # meas. 2nd clock
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n") 
		# case, clock 01 -> output 01
		elif((targetHarness.target_clock_val == "01")and(targetHarness.target_outport_val == "01")):
			outlines.append(".measure Tran PROP_CIN_OUT trig v(VCIN) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=2 \n") # meas. 2nd clock
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n") 
		# case, clock 10 -> output 10
		elif((targetHarness.target_clock_val == "10")and(targetHarness.target_outport_val == "10")):
			outlines.append(".measure Tran PROP_CIN_OUT trig v(VCIN) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=2 \n") # meas. 2nd clock
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n") 
		# case, clock 10 -> output 01
		elif((targetHarness.target_clock_val == "01")and(targetHarness.target_outport_val == "01")):
			outlines.append(".measure Tran PROP_CIN_OUT trig v(VCIN) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=2 \n") # meas. 2nd clock
			outlines.append("+ targ v(VOUT) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n") 
		else:
			print ("Skip C2Q simulation")


		# measure D2C(setup)
		outlines.append("* Prop delay (D2C,setup)\n")
		# case, D 01 -> CLK 01
		if((targetHarness.target_inport_val == "01")and(targetHarness.target_clock_val == "01")):
			outlines.append(".measure Tran PROP_IN_D2C trig v("+V_in_target+") val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
			outlines.append("+ targ v(VCIN) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=2 \n") # meas. 2nd clock  
		# case, D 10 -> CLK 01
		elif((targetHarness.target_inport_val == "10")and(targetHarness.target_clock_val == "01")):
			outlines.append(".measure Tran PROP_IN_D2C trig v("+V_in_target+") val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
			outlines.append("+ targ v(VCIN) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=2 \n") # meas. 2nd clock  
		# case, D 01 -> CLK 10
		elif((targetHarness.target_inport_val == "01")and(targetHarness.target_clock_val == "10")):
			outlines.append(".measure Tran PROP_IN_D2C trig v("+V_in_target+") val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n")
			outlines.append("+ targ v(VCIN) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=2 \n") # meas. 2nd clock  
		# case, D 10 -> CLK 10
		elif((targetHarness.target_inport_val == "10")and(targetHarness.target_clock_val == "10")):
			outlines.append(".measure Tran PROP_IN_D2C trig v("+V_in_target+") val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n")
			outlines.append("+ targ v(VCIN) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=2 \n") # meas. 2nd clock  
		else:
			print ("Skip D2C(setup) simulation")

		# measure C2D(HOLD)
		outlines.append("* Prop delay (C2D,HOLD)\n")
		
		# case, CLK 01 -> D (01->)10 
		if((targetHarness.target_inport_val == "01")and(targetHarness.target_clock_val == "01")):
			outlines.append(".measure Tran PROP_IN_C2D trig v(VCIN) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=2 \n") # meas. 2nd clock
			outlines.append("+ targ v("+V_in_target+") val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n") 
		# case, CLK 01 -> D (10->)01 
		elif((targetHarness.target_inport_val == "10")and(targetHarness.target_clock_val == "01")):
			outlines.append(".measure Tran PROP_IN_C2D trig v(VCIN) val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=2 \n") # meas. 2nd clock
			outlines.append("+ targ v("+V_in_target+") val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n") 
		# case, CLK 10 -> D (01->)10 
		elif((targetHarness.target_inport_val == "01")and(targetHarness.target_clock_val == "10")):
			outlines.append(".measure Tran PROP_IN_C2D trig v(VCIN) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=2 \n") # meas. 2nd clock
			outlines.append("+ targ v("+V_in_target+") val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=1 \n") 
		# case, CLK 10 -> D (10->)01 
		elif((targetHarness.target_inport_val == "10")and(targetHarness.target_clock_val == "10")):
			outlines.append(".measure Tran PROP_IN_C2D trig v(VCIN) val='"+str(float(targetLib.logic_high_to_low_threshold)*float(targetLib.vdd_voltage))+"' fall=2 \n") # meas. 2nd clock
			outlines.append("+ targ v("+V_in_target+") val='"+str(float(targetLib.logic_low_to_high_threshold)*float(targetLib.vdd_voltage))+"' rise=1 \n") 
		else:
			print ("Skip C2D(hold) simulation")


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
		outlines.append("XDFF VIN VCIN VRIN VSIN VOUT VHIGH VLOW VDD_DYN VSS_DYN VNW_DYN VPW_DYN DUT \n")
		outlines.append("C0 VOUT VSS_DYN 'cap'\n")
		outlines.append(" \n")
		outlines.append(".SUBCKT DUT IN CIN RIN SIN OUT HIGH LOW VDD VSS VNW VPW \n")
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
						print('Illigal input value for stable input')
			# search target clock
			w2 = targetHarness.target_clock
			if(w1 == w2):
				tmp_line += ' CIN'
			# search target reset
			w2 = targetHarness.target_reset
			if(w1 == w2):
				tmp_line += ' RIN'
			# search target set
			w2 = targetHarness.target_set
			if(w1 == w2):
				tmp_line += ' SIN'
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
			# search VDD/VSS/VNW/VPW
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
		outlines.append(tsetup_line)
		outlines.append(thold_line)
				
## for ngspice batch mode 
		outlines.append("*enable .control to show graph in ngspice \n")
		outlines.append("*.control \n")
		outlines.append("*run \n")
		outlines.append("*plot V("+V_in_target+") V(VOUT) V(VCIN) \n")
		outlines.append("*.endc \n")
		outlines.append(".end \n") 
		f.writelines(outlines)
	f.close()

	spicelis = spicef
	spicelis += ".lis"

	# run simulation
	cmd = str(targetLib.simulator)+" -b "+str(spicef)+" 1> "+str(spicelis)+" 2> /dev/null \n"
	#cmd = str(targetLib.simulator)+" -b "+str(spicef)+" > "+str(spicelis)+"\n"
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
			elif(re.match("prop_cin_out", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_prop_cin_out = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("trans_out", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_trans_out = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("energy_start", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_energy_start = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("energy_end", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_energy_end = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("prop_in_d2c", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_setup = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)
			elif(re.match("prop_in_c2d", inline)):
				sparray = re.split(" +", inline) # separate words with spaces (use re.split)
				res_hold = "{:e}".format(float(sparray[2].strip())/targetLib.time_mag)

	f.close()
	#print(str(res_prop_in_out)+" "+str(res_trans_out)+" "+str(res_energy_start)+" "+str(res_energy_end))
	# check spice finish successfully
	try:
		res_prop_in_out
	except NameError:
		print("Value res_prop_in_out is not defined!!")
		print("DFF simulation failed!!")
		res_prop_in_out = "failed"	
	try:
		res_prop_cin_out
	except NameError:
		print("Value res_cprop_in_out is not defined!!")
		print("DFF simulation failed!!")
		res_prop_cin_out = "failed"	
	try:
		res_trans_out
	except NameError:
		print("Value res_trans_out is not defined!!")
		print("DFF simulation failed!!")
		res_trans_out = "failed"	
	try:
		res_energy_start
	except NameError:
		print("Value res_energy_start is not defined!!")
		print("DFF simulation failed!!")
		res_energy_start = "failed"	
	try:
		res_energy_end
	except NameError:
		print("Value res_energy_end is not defined!!")
		print("DFF simulation failed!!")
		res_energy_end = "failed"	
	try:
		res_setup
	except NameError:
		print("Value res_setup is not defined!!")
		print("DFF simulation failed!!")
		res_setup = "failed"	
	try:
		res_hold
	except NameError:
		print("Value res_hold is not defined!!")
		print("DFF simulation failed!!")
		res_hold = "failed"	
	return res_prop_in_out, res_prop_cin_out, res_trans_out, \
					res_energy_start, res_energy_end, res_setup, res_hold
	
