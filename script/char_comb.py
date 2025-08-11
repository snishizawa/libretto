import argparse, re, os, shutil, subprocess, sys, inspect, threading 

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
    ## case input0 is target input pin
    if ((tmp_inp0_val == '01') or (tmp_inp0_val == '10')):
      tmp_Harness.set_target_inport (targetCell.inports[0], tmp_inp0_val)
      tmp_Harness.set_stable_inport ("NULL", "NULL")
    else:
      print ("Illiegal input vector type!!")
      print ("Check logic definition of this program!!")
      
    #tmp_Harness.set_leak_inportval ("1")
    #tmp_Harness.set_nontarget_outport (targetCell.outports[0], "01")
    spicef = "vt_"+str(targetLib.vdd_voltage)+"_"+str(targetLib.temperature)+"_"\
      +"delay1_"+str(targetCell.cell)+"_"+str(targetCell.inports[0])\
      +str(tmp_inp0_val)+"_"+str(targetCell.outports[0])+str(tmp_outp0_val)
    ## run spice and store result
    runSpiceCombDelayMultiThread(targetLib, targetCell, tmp_Harness, spicef)
    harnessList.append(tmp_Harness)
    harnessList2.append(harnessList)


  ## average cin of each harness
  targetCell.set_cin_avg(targetLib, harnessList) 

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
      print ("Illiegal input vector type!!")
      print ("Check logic definition of this program!!")
      
    #tmp_Harness.set_leak_inportval ("1")
    #tmp_Harness.set_nontarget_outport (targetCell.outports[0], "01")
    spicef = "vt_"+str(targetLib.vdd_voltage)+"_"+str(targetLib.temperature)+"_"\
      +"delay1_"+str(targetCell.cell)+"_"+str(targetCell.inports[0])\
      +str(tmp_inp0_val)+"_"+str(targetCell.inports[1])+str(tmp_inp1_val)\
      +"_"+str(targetCell.outports[0])+str(tmp_outp0_val)
    # run spice and store result
    runSpiceCombDelayMultiThread(targetLib, targetCell, tmp_Harness, spicef)
    harnessList.append(tmp_Harness)
    harnessList2.append(harnessList)

    # calculate avg of pleak
    #if ((tmp_inp0_val == '01') or (tmp_inp0_val == '10')):
    # targetCell.set_inport_cap_pleak(0, tmp_Harness)
    # case input0 is target input pin
    #elif ((tmp_inp1_val == '01') or (tmp_inp1_val == '10')):
    # targetCell.set_inport_cap_pleak(1, tmp_Harness)

  ## average cin of each harness
  targetCell.set_cin_avg(targetLib, harnessList) 

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
      print ("Illiegal input vector type!!")
      print ("Check logic definition of this program!!")
      
    #tmp_Harness.set_leak_inportval ("1")
    #tmp_Harness.set_nontarget_outport (targetCell.outports[0], "01")
    spicef = "vt_"+str(targetLib.vdd_voltage)+"_"+str(targetLib.temperature)+"_"\
      +"delay1_"+str(targetCell.cell)+"_"\
      +str(targetCell.inports[0])+str(tmp_inp0_val)\
      +"_"+str(targetCell.inports[1])+str(tmp_inp1_val)\
      +"_"+str(targetCell.inports[2])+str(tmp_inp2_val)\
      +"_"+str(targetCell.outports[0])+str(tmp_outp0_val)
    # run spice and store result
    runSpiceCombDelayMultiThread(targetLib, targetCell, tmp_Harness, spicef)
    harnessList.append(tmp_Harness)
    harnessList2.append(harnessList)

  ## average cin of each harness
  targetCell.set_cin_avg(targetLib, harnessList) 

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
      print ("Illiegal input vector type!!")
      print ("Check logic definition of this program!!")
      
    #tmp_Harness.set_leak_inportval ("1")
    #tmp_Harness.set_nontarget_outport (targetCell.outports[0], "01")
    spicef = "vt_"+str(targetLib.vdd_voltage)+"_"+str(targetLib.temperature)+"_"\
      +"delay1_"+str(targetCell.cell)+"_"\
      +str(targetCell.inports[0])+str(tmp_inp0_val)\
      +"_"+str(targetCell.inports[1])+str(tmp_inp1_val)\
      +"_"+str(targetCell.inports[2])+str(tmp_inp2_val)\
      +"_"+str(targetCell.inports[3])+str(tmp_inp3_val)\
      +"_"+str(targetCell.outports[0])+str(tmp_outp0_val)
    # run spice and store result
    runSpiceCombDelayMultiThread(targetLib, targetCell, tmp_Harness, spicef)
    harnessList.append(tmp_Harness)
    harnessList2.append(harnessList)
  
  ## average cin of each harness
  targetCell.set_cin_avg(targetLib, harnessList) 

  return harnessList2
#end  runCombIn4Out1

def runSpiceCombDelayMultiThread(targetLib, targetCell, targetHarness, spicef):
  list2_prop =   []
  list2_tran =   []
  list2_estart = []
  list2_eend =   []
  list2_eintl =   []
  list2_ein =   []
  list2_cin =   []
  list2_pleak =   []
  ## calculate whole slope length from logic threshold
  tmp_slope_mag = 1 / (targetLib.logic_threshold_high - targetLib.logic_threshold_low)

  thread_id = 0

  # Limit number of threads
  # define semaphore 
  pool_sema = threading.BoundedSemaphore(targetLib.num_thread)
  targetLib.print_msg("Num threads for simulation:"+str(targetLib.num_thread))

  results_prop_in_out  = dict()
  results_trans_out    = dict()
  results_energy_start = dict()
  results_energy_end   = dict()
  results_q_in_dyn     = dict()
  results_q_out_dyn    = dict()
  results_q_vdd_dyn    = dict()
  results_q_vss_dyn    = dict()
  results_i_in_leak    = dict()
  results_i_vdd_leak   = dict()
  results_i_vss_leak   = dict()
  threadlist = list()
  for tmp_load in targetCell.load:
    for tmp_slope in targetCell.slope:
      thread = threading.Thread(target=runSpiceCombDelaySingle, \
              args=([pool_sema, targetLib, targetCell, targetHarness, spicef, \
                  tmp_slope, tmp_load, tmp_slope_mag, \
                  results_prop_in_out, results_trans_out,\
                  results_energy_start, results_energy_end,\
                  results_q_in_dyn, results_q_out_dyn, results_q_vdd_dyn, results_q_vss_dyn, \
                  results_i_in_leak, results_i_vdd_leak, results_i_vss_leak]),  \
              name="%d" % thread_id)
      threadlist.append(thread)
      thread_id += 1

  for thread in threadlist:
    thread.start() 

  for thread in threadlist:
    thread.join() 

  thread_id = 0
  for tmp_load in targetCell.load:
    tmp_list_prop =   []
    tmp_list_tran =   []
    tmp_list_estart = []
    tmp_list_eend =   []
    tmp_list_eintl =   []
    tmp_list_ein =   []
    tmp_list_cin =   []
    tmp_list_pleak =   []
    for tmp_slope in targetCell.slope:
#      targetLib.print_msg(str(thread_id))
#      targetLib.print_msg(str(results_prop_in_out))
#      targetLib.print_msg(str(results_prop_in_out[str(thread_id)]))
      tmp_list_prop.append(results_prop_in_out[str(thread_id)])
      tmp_list_tran.append(results_trans_out[str(thread_id)])

      ## intl. energy calculation
      ## intl. energy is the sum of short-circuit energy and drain-diffusion charge/discharge energy
      ## larger Ql: intl. Q, load Q 
      ## smaller Qs: intl. Q
      ## Eintl = QsV
      if(abs(results_q_vdd_dyn[str(thread_id)]) < abs(results_q_vss_dyn[str(thread_id)])):
        res_q = results_q_vdd_dyn[str(thread_id)]
      else:
        res_q = results_q_vss_dyn[str(thread_id)]
      tmp_list_eintl.append(abs(res_q*targetLib.vdd_voltage*targetLib.energy_meas_high_threshold \
        - abs((results_energy_end[str(thread_id)] - results_energy_start[str(thread_id)])*((abs(results_i_vdd_leak[str(thread_id)]) \
        + abs(results_i_vss_leak[str(thread_id)]))/2)*(targetLib.vdd_voltage*targetLib.energy_meas_high_threshold))))

      ## input energy
      tmp_list_ein.append(abs(results_q_in_dyn[str(thread_id)])*targetLib.vdd_voltage)

      ## Cin = Qin / V
      tmp_list_cin.append(abs(results_q_in_dyn[str(thread_id)])/(targetLib.vdd_voltage))

      ## Pleak = average of Pleak_vdd and Pleak_vss
      ## P = I * V
      tmp_list_pleak.append(((abs(results_i_vdd_leak[str(thread_id)])+abs(results_i_vss_leak[str(thread_id)]))/2)*(targetLib.vdd_voltage)) #
      thread_id += 1

    list2_prop.append(tmp_list_prop)
    list2_tran.append(tmp_list_tran)
    #list2_estart.append(tmp_list_estart)
    #list2_eend.append(tmp_list_eend)
    list2_eintl.append(tmp_list_eintl)
    list2_ein.append(tmp_list_ein)
    list2_cin.append(tmp_list_cin)
    list2_pleak.append(tmp_list_pleak)


  targetHarness.set_list2_prop(list2_prop)
  targetHarness.write_list2_prop(targetLib, targetCell.load, targetCell.slope)
  targetHarness.set_list2_tran(list2_tran)
  targetHarness.write_list2_tran(targetLib, targetCell.load, targetCell.slope)
  targetHarness.set_list2_eintl(list2_eintl)
  targetHarness.write_list2_eintl(targetLib, targetCell.load, targetCell.slope)
  targetHarness.set_list2_ein(list2_ein)
  targetHarness.write_list2_ein(targetLib, targetCell.load, targetCell.slope)

  targetHarness.set_list2_cin(list2_cin)
  targetHarness.average_list2_cin(targetLib, targetCell.load, targetCell.slope)
  targetHarness.set_list2_pleak(list2_pleak)
  targetHarness.write_list2_pleak(targetLib, targetCell.load, targetCell.slope)
    
def runSpiceCombDelaySingle(pool_sema, targetLib, targetCell, targetHarness, spicef, \
                      tmp_slope, tmp_load, tmp_slope_mag, \
                      results_prop_in_out, results_trans_out,\
                      results_energy_start, results_energy_end,\
                      results_q_in_dyn, results_q_out_dyn, results_q_vdd_dyn, results_q_vss_dyn, \
                      results_i_in_leak, results_i_vdd_leak, results_i_vss_leak):
 
  with pool_sema:
    #targetLib.print_msg("start thread :"+str(threading.current_thread().name))
    #print("start thread ")
 
    cap_line = ".param cap ="+str(tmp_load*targetLib.capacitance_mag)+"\n"
    slew_line = ".param slew ="+str(tmp_slope*tmp_slope_mag*targetLib.time_mag)+"\n"
    temp_line = ".temp "+str(targetLib.temperature)+"\n"
    spicefo  = str(spicef)+"_"+str(tmp_load)+"_"+str(tmp_slope)+".sp"
    spicefoe = str(spicef)+"_"+str(tmp_load)+"_"+str(tmp_slope)+"_energy.sp"
 
    ## 1st trial, extract energy_start and energy_end
    res_prop_in_out, res_trans_out, res_energy_start, res_energy_end, \
      = genFileLogic_trial1(targetLib, targetCell, targetHarness, 0, cap_line, slew_line, temp_line, "none", "none", spicefo)
 
    estart_line = ".param ENERGY_START = "+str(res_energy_start)+"\n"
    eend_line = ".param ENERGY_END = "+str(res_energy_end)+"\n"
 
    ## 2nd trial, extract energy
    res_prop_in_out, res_trans_out, \
      res_q_in_dyn, res_q_out_dyn, res_q_vdd_dyn, res_q_vss_dyn, \
      res_i_in_leak, res_i_vdd_leak, res_i_vss_leak \
      = genFileLogic_trial1(targetLib, targetCell, targetHarness, 1, cap_line, slew_line, temp_line, estart_line, eend_line, spicefoe)
    #targetLib.print_msg(str(res_prop_in_out)+" "+str(res_trans_out)+" "+str(res_energy_start)+" "+str(res_energy_end))
    results_prop_in_out[threading.current_thread().name] = res_prop_in_out
    results_trans_out[threading.current_thread().name]   = res_trans_out
    results_energy_start[threading.current_thread().name]= res_energy_start
    results_energy_end[threading.current_thread().name]  = res_energy_end
    results_q_in_dyn[threading.current_thread().name]    = res_q_in_dyn
    results_q_out_dyn[threading.current_thread().name]   = res_q_out_dyn
    results_q_vdd_dyn[threading.current_thread().name]   = res_q_vdd_dyn
    results_q_vss_dyn[threading.current_thread().name]   = res_q_vss_dyn
    results_i_in_leak[threading.current_thread().name]   = res_i_in_leak
    results_i_vdd_leak[threading.current_thread().name]  = res_i_vdd_leak
    results_i_vss_leak[threading.current_thread().name]  = res_i_vss_leak
 
    #targetLib.print_msg("end thread :"+str(threading.current_thread().name))

def genFileLogic_trial1(targetLib, targetCell, targetHarness, meas_energy, cap_line, slew_line, temp_line, estart_line, eend_line, spicef):
  #print (spicef)
  #print (estart_line)
  #print (eend_line)
  #print (spicef)
  #print ("generate AND2\n")
  #targetLib.print_msg(dir(targetLib))

  spicelis = spicef
  spicelis += ".lis"
  # if file is not exist, create spice file and run spice
  if(os.path.isfile(spicelis)):
    targetLib.print_msg("skip file: "+str(spicef))
  else:
    targetLib.print_msg("generate file: "+str(spicef))
    with open(spicef,'w') as f:
      outlines = []
      outlines.append("*title: delay meas.\n")
      outlines.append(".option brief nopage nomod post=1 ingold=2 autostop\n")
      outlines.append(".inc '../"+targetCell.model+"'\n")
      outlines.append(".inc '../"+targetCell.netlist+"'\n")
      outlines.append(temp_line)
      outlines.append(".param _vdd = "+str(targetLib.vdd_voltage)+"\n")
      outlines.append(".param _vss = "+str(targetLib.vss_voltage)+"\n")
      outlines.append(".param _vnw = "+str(targetLib.nwell_voltage)+"\n")
      outlines.append(".param _vpw = "+str(targetLib.pwell_voltage)+"\n")
      outlines.append(".param cap = 10f \n")
      outlines.append(".param slew = 100p \n")
      outlines.append(".param _tslew = slew\n")
      outlines.append(".param _tstart = slew\n")
      outlines.append(".param _tend = '_tstart + _tslew'\n")
                  #outlines.append(".param _tsimend = '_tslew * 10000' \n")
      #outlines.append(".param _tsimend = '10 * _tslew + 1us' \n")
      outlines.append(".param _tsimend = '25 * _tslew ' \n")
 
      outlines.append(".param _Energy_meas_end_extent = "+str(targetLib.energy_meas_time_extent)+"\n")
      outlines.append(" \n")
      outlines.append("VDD_DYN VDD_DYN 0 DC '_vdd' \n")
      outlines.append("VSS_DYN VSS_DYN 0 DC '_vss' \n")
      outlines.append("VNW_DYN VNW_DYN 0 DC '_vnw' \n")
      outlines.append("VPW_DYN VPW_DYN 0 DC '_vpw' \n")
      outlines.append("* output load calculation\n")
      outlines.append("VOCAP VOUT WOUT DC 0\n")
      #outlines.append("VDD_LEAK VDD_LEAK 0 DC '_vdd' \n")
      #outlines.append("VSS_LEAK VSS_LEAK 0 DC '_vss' \n")
      #outlines.append("VNW_LEAK VNW_LEAK 0 DC '_vnw' \n")
      #outlines.append("VPW_LEAK VPW_LEAK 0 DC '_vpw' \n")
      outlines.append(" \n")
      ## in auto mode, simulation timestep is 1/10 of min. input slew
      ## simulation runs 1000x of input slew time
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
 
      ##
      ## delay measurement 
      outlines.append("** Delay \n")
      outlines.append("* Prop delay \n")
      if(targetHarness.target_inport_val == "01"):
        outlines.append(".measure Tran PROP_IN_OUT trig v(VIN) VAL='"+str(targetLib.logic_low_to_high_threshold_voltage)+"' rise=1 \n")
      elif(targetHarness.target_inport_val == "10"):
        outlines.append(".measure Tran PROP_IN_OUT trig v(VIN) VAL='"+str(targetLib.logic_high_to_low_threshold_voltage)+"' fall=1 \n")
      if(targetHarness.target_outport_val == "10"):
        outlines.append("+ targ v(VOUT) val='"+str(targetLib.logic_high_to_low_threshold_voltage)+"' fall=1 \n")
      elif(targetHarness.target_outport_val == "01"):
        outlines.append("+ targ v(VOUT) val='"+str(targetLib.logic_low_to_high_threshold_voltage)+"' rise=1 \n")
      outlines.append("* Trans delay \n")
 
      if(targetHarness.target_outport_val == "10"):
        outlines.append(".measure Tran TRANS_OUT trig v(VOUT) VAL='"+str(targetLib.logic_threshold_high_voltage)+"' fall=1\n")
        outlines.append("+ targ v(VOUT) val='"+str(targetLib.logic_threshold_low_voltage)+"' fall=1 \n")
      elif(targetHarness.target_outport_val == "01"):
        outlines.append(".measure Tran TRANS_OUT trig v(VOUT) VAL='"+str(targetLib.logic_threshold_low_voltage)+"' rise=1\n")
        outlines.append("+ targ v(VOUT) val='"+str(targetLib.logic_threshold_high_voltage)+"' rise=1 \n")
 
      # get ENERGY_START and ENERGY_END for energy calculation in 2nd round 
      if(meas_energy == 0):
        outlines.append("* For energy calculation \n")
        if(targetHarness.target_inport_val == "01"):
          outlines.append(".measure Tran ENERGY_START when v(VIN)='"+str(targetLib.energy_meas_low_threshold_voltage)+"' rise=1 \n")
        elif(targetHarness.target_inport_val == "10"):
          outlines.append(".measure Tran ENERGY_START when v(VIN)='"+str(targetLib.energy_meas_high_threshold_voltage)+"' fall=1 \n")
        if(targetHarness.target_outport_val == "01"):
          outlines.append(".measure Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_high_threshold_voltage)+"' rise=1 \n")
        elif(targetHarness.target_outport_val == "10"):
          outlines.append(".measure Tran ENERGY_END when v(VOUT)='"+str(targetLib.energy_meas_low_threshold_voltage)+"' fall=1 \n")
 
      ##
      ## energy measurement 
      elif(meas_energy == 1):
        outlines.append(estart_line)
        outlines.append(eend_line)
        outlines.append("* \n")
        outlines.append("** In/Out Q, Capacitance \n")
        outlines.append("* \n")
        outlines.append(".measure Tran Q_IN_DYN integ i(VIN) from='ENERGY_START' to='ENERGY_END'  \n")
        outlines.append(".measure Tran Q_OUT_DYN integ i(VOCAP) from='ENERGY_START' to='ENERGY_END*_Energy_meas_end_extent' \n")
        outlines.append(" \n")
        outlines.append("* \n")
        outlines.append("** Energy \n")
        outlines.append("*  (Total charge, Short-Circuit Charge) \n")
        outlines.append(".measure Tran Q_VDD_DYN integ i(VDD_DYN) from='ENERGY_START' to='ENERGY_END*_Energy_meas_end_extent'  \n")
        outlines.append(".measure Tran Q_VSS_DYN integ i(VSS_DYN) from='ENERGY_START' to='ENERGY_END*_Energy_meas_end_extent'  \n")
        outlines.append(" \n")
        outlines.append("* Leakage current \n")
        outlines.append(".measure Tran I_VDD_LEAK avg i(VDD_DYN) from='_tstart*0.1' to='_tstart'  \n")
        outlines.append(".measure Tran I_VSS_LEAK avg i(VSS_DYN) from='_tstart*0.1' to='_tstart'  \n")
        outlines.append(" \n")
        outlines.append("* Gate leak current \n")
        outlines.append(".measure Tran I_IN_LEAK avg i(VIN) from='_tstart*0.1' to='_tstart'  \n")
      else:
        targetLib.print_msg("Error, meas_energy should 0 (disable) or 1 (enable)")
        my_error()
 
      ## for ngspice batch mode 
      outlines.append("*comment out .control for ngspice batch mode \n")
      outlines.append("*.control \n")
      outlines.append("*run \n")
      outlines.append("*plot V(VIN) V(VOUT) \n")
      outlines.append("*.endc \n")
 
      outlines.append("XINV VIN VOUT VHIGH VLOW VDD_DYN VSS_DYN VNW_DYN VPW_DYN DUT \n")
      outlines.append("C0 WOUT VSS_DYN 'cap'\n")
      outlines.append(" \n")
      outlines.append(".SUBCKT DUT IN OUT HIGH LOW VDD VSS VNW VPW \n")
      # parse subckt definition
      tmp_array = targetCell.instance.split()
      tmp_line = tmp_array[0] # XDUT
      #targetLib.print_msg(tmp_line)
      for w1 in tmp_array:
        # match tmp_array and harness 
        # search target inport
        is_matched = 0
        w2 = targetHarness.target_inport
        if(w1 == w2):
          tmp_line += ' IN'
          is_matched += 1
        # search stable inport
        for w2 in targetHarness.stable_inport:
          if(w1 == w2):
            # this is stable inport
            # search index for this port
            index_val = targetHarness.stable_inport_val[targetHarness.stable_inport.index(w2)]
            if(index_val == '1'):
              tmp_line += ' HIGH'
              is_matched += 1
            elif(index_val == '0'):
              tmp_line += ' LOW'
              is_matched += 1
            else:
              targetLib.print_msg('Illigal input value for stable input')
        # one target outport for one simulation
        w2 = targetHarness.target_outport
        #targetLib.print_msg(w1+" "+w2+"\n")
        if(w1 == w2):
          tmp_line += ' OUT'
          is_matched += 1
        # search non-terget outport
        for w2 in targetHarness.nontarget_outport:
          if(w1 == w2):
            # this is non-terget outport
            # search outdex for this port
            index_val = targetHarness.nontarget_outport_val[targetHarness.nontarget_outport.index(w2)]
            tmp_line += ' WFLOAT'+str(index_val)
            is_matched += 1
        if(w1.upper() == targetLib.vdd_name.upper()):
            # tmp_line += ' '+w1.upper() 
            tmp_line += ' VDD' 
            is_matched += 1
        if(w1.upper() == targetLib.vss_name.upper()):
            # tmp_line += ' '+w1.upper() 
            tmp_line += ' VSS' 
            is_matched += 1
        if(w1.upper() == targetLib.pwell_name.upper()):
            # tmp_line += ' '+w1.upper() 
            tmp_line += ' VPW' 
            is_matched += 1
        if(w1.upper() == targetLib.nwell_name.upper()):
            # tmp_line += ' '+w1.upper() 
            tmp_line += ' VNW' 
            is_matched += 1
        ## show error if this port has not matched
        if(is_matched == 0):
          ## if w1 is wire name, abort
          ## check this is instance tmp_array[0] or circuit name tmp_array[-1]
          if((w1 != tmp_array[0]) and (w1 != tmp_array[-1])): 
            targetLib.print_error("port: "+str(w1)+" has not matched in netlist parse!!")
            
      tmp_line += " "+str(tmp_array[len(tmp_array)-1])+"\n" # CIRCUIT NAME
      outlines.append(tmp_line)
      #targetLib.print_msg(tmp_line)
 
      outlines.append(".ends \n")
      outlines.append(" \n")
      outlines.append(cap_line)
      outlines.append(slew_line)
          
      outlines.append(".end \n") 
      f.writelines(outlines)
    f.close()
 
    spicelis = spicef
    spicelis += ".lis"
    spicerun = spicef
    spicerun += ".run"
    if(re.search("ngspice", targetLib.simulator)):
      cmd = "nice -n "+str(targetLib.sim_nice)+" "+str(targetLib.simulator)+" -b "+str(spicef)+" > "+str(spicelis)+" 2>&1 \n"
    elif(re.search("hspice", targetLib.simulator)):
      cmd = "nice -n "+str(targetLib.sim_nice)+" "+str(targetLib.simulator)+" "+str(spicef)+" -o "+str(spicelis)+" 2> /dev/null \n"
    elif(re.search("Xyce", targetLib.simulator)):
      cmd = "nice -n "+str(targetLib.sim_nice)+" "+str(targetLib.simulator)+" "+str(spicef)+" -hspice-ext all 1> "+str(spicelis)
    with open(spicerun,'w') as f:
      outlines = []
      outlines.append(cmd) 
      f.writelines(outlines)
    f.close()
 
    cmd = ['sh', spicerun]
 
    if(targetLib.runsim == "true"):
      try:
        res = subprocess.check_call(cmd)
      except:
        print ("Failed to lunch spice")

  # read .mt0 for Xyce
  if(re.search("Xyce", targetLib.simulator)):
    spicelis = spicelis[:-3]+"mt0" 

  # read results
  with open(spicelis,'r') as f:
    for inline in f:
      if(re.search("hspice", targetLib.simulator)):
        inline = re.sub('\=',' ',inline)
      #targetLib.print_msg(inline)
      # search measure
      if((re.search("prop_in_out", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
        sparray = re.split(" +", inline) # separate words with spaces (use re.split)
        res_prop_in_out = "{:e}".format(float(sparray[2].strip()))
      elif((re.search("trans_out", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
        sparray = re.split(" +", inline) # separate words with spaces (use re.split)
        res_trans_out = "{:e}".format(float(sparray[2].strip()))
      if(meas_energy == 0):
        if((re.search("energy_start", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
          sparray = re.split(" +", inline) # separate words with spaces (use re.split)
          res_energy_start = "{:e}".format(float(sparray[2].strip()))
        elif((re.search("energy_end", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
          sparray = re.split(" +", inline) # separate words with spaces (use re.split)
          res_energy_end = "{:e}".format(float(sparray[2].strip()))
      if(meas_energy == 1):
        if((re.search("q_in_dyn", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
          sparray = re.split(" +", inline) # separate words with spaces (use re.split)
          res_q_in_dyn = "{:e}".format(float(sparray[2].strip()))
        elif((re.search("q_out_dyn", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
          sparray = re.split(" +", inline) # separate words with spaces (use re.split)
          res_q_out_dyn = "{:e}".format(float(sparray[2].strip()))
        elif((re.search("q_vdd_dyn", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
          sparray = re.split(" +", inline) # separate words with spaces (use re.split)
          res_q_vdd_dyn = "{:e}".format(float(sparray[2].strip()))
        elif((re.search("q_vss_dyn", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
          sparray = re.split(" +", inline) # separate words with spaces (use re.split)
          res_q_vss_dyn = "{:e}".format(float(sparray[2].strip()))
        elif((re.search("i_vdd_leak", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
          sparray = re.split(" +", inline) # separate words with spaces (use re.split)
          res_i_vdd_leak = "{:e}".format(float(sparray[2].strip()))
        elif((re.search("i_vss_leak", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
          sparray = re.split(" +", inline) # separate words with spaces (use re.split)
          res_i_vss_leak = "{:e}".format(float(sparray[2].strip()))
        elif((re.search("i_in_leak", inline, re.IGNORECASE))and not (re.search("failed",inline)) and not (re.search("Error",inline))):
          sparray = re.split(" +", inline) # separate words with spaces (use re.split)
          res_i_in_leak = "{:e}".format(float(sparray[2].strip()))

  f.close()
  #targetLib.print_msg(str(res_prop_in_out)+" "+str(res_trans_out)+" "+str(res_energy_start)+" "+str(res_energy_end))
  # check spice finish successfully
  try:
    res_prop_in_out
  except NameError:
    targetLib.print_msg("Value res_prop_in_out is not defined!!")
    targetLib.print_msg("Check simulation result in work directory")
    sys.exit()
  try:
    res_trans_out
  except NameError:
    targetLib.print_msg("Value res_trans_out is not defined!!")
    targetLib.print_msg("Check simulation result in work directory")
    sys.exit()
  if(meas_energy == 0):
    return float(res_prop_in_out), float(res_trans_out), float(res_energy_start), float(res_energy_end)
  elif(meas_energy == 1):
    return float(res_prop_in_out), float(res_trans_out), \
        float(res_q_in_dyn), float(res_q_out_dyn), float(res_q_vdd_dyn), float(res_q_vss_dyn), \
        float(res_i_in_leak), float(res_i_vdd_leak), float(res_i_vss_leak)
