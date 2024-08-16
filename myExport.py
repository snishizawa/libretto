
import argparse, re, os, shutil, subprocess, sys, inspect, datetime 
from myFunc import my_exit

def exportFiles(targetLib, targetCell, harnessList2):

  ## initialize tmp file
  if(targetLib.isexport == 0):
    initLib(targetLib, targetCell)

  ## generate / update library general settings 
  exportLib(targetLib, targetCell)

  ## export comb. logic
  if((targetLib.isexport == 1) and (targetCell.isexport == 0) and (targetCell.isflop == 0)):
    exportHarness(targetLib, targetCell, harnessList2)
    exportVerilog(targetLib, targetCell)
    compressFiles(targetLib, targetCell)
  ## export seq. logic
  elif((targetLib.isexport == 1) and (targetCell.isexport == 0) and (targetCell.isflop == 1)):
    exportHarnessFlop(targetLib, targetCell, harnessList2)
    exportVerilogFlop(targetLib, targetCell)
    compressFiles(targetLib, targetCell)

## initialize export lib and verilog 
def initLib(targetLib, targetCell):
  
  ## initilize dotlib file
  outlines = []
  with open(targetLib.tmp_file, 'w') as f:
    f.writelines(outlines)
  f.close()
  ## initilize verilog file 
  outlines = []
  with open(targetLib.verilog_name, 'w') as f:
    outlines.append("// Verilog model for "+targetLib.lib_name+"; \n")
    outlines.append("`timescale 1ns/1ns\n")
    f.writelines(outlines)
  f.close()

## export library definition to .lib
def exportLib(targetLib, targetCell):
  with open(targetLib.dotlib_name, 'w') as f:
    outlines = []
    ## general settings
    outlines.append("## dotlib file generated libretto; \n")
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
    outlines.append("  default_leakage_power_density : 0;\n")
    outlines.append("  default_max_fanout : 100;\n")
    outlines.append("  default_output_pin_cap : 0;\n")
    outlines.append("  in_place_swap_mode : match_footprint;\n")
    outlines.append("  input_threshold_pct_fall : "+str(targetLib.logic_high_to_low_threshold*100)+";\n")
    outlines.append("  input_threshold_pct_rise : "+str(targetLib.logic_low_to_high_threshold*100)+";\n")
    outlines.append("  nom_process : 1;\n")
    outlines.append("  nom_temperature : \""+str(targetLib.temperature)+"\";\n")
    outlines.append("  nom_voltage : \""+str(targetLib.vdd_voltage)+"\";\n")
    outlines.append("  output_threshold_pct_fall : "+str(targetLib.logic_high_to_low_threshold*100)+";\n")
    outlines.append("  output_threshold_pct_rise : "+str(targetLib.logic_low_to_high_threshold*100)+";\n")
    outlines.append("  slew_derate_from_library : 1;\n")
    outlines.append("  slew_lower_threshold_pct_fall : "+str(targetLib.logic_threshold_low*100)+";\n")
    outlines.append("  slew_lower_threshold_pct_rise : "+str(targetLib.logic_threshold_low*100)+";\n")
    outlines.append("  slew_upper_threshold_pct_fall : "+str(targetLib.logic_threshold_high*100)+";\n")
    outlines.append("  slew_upper_threshold_pct_rise : "+str(targetLib.logic_threshold_high*100)+";\n")
    ## operating conditions
    outlines.append("  operating_conditions ("+targetLib.operating_conditions+") {\n")
    outlines.append("    process : 1;\n")
    outlines.append("    temperature : "+str(targetLib.temperature)+";\n")
    outlines.append("    voltage : "+str(targetLib.vdd_voltage)+";\n")
    outlines.append("  }\n")
    outlines.append("  default_operating_conditions : "+targetLib.operating_conditions+";\n")
    ## definition of LUT template
    outlines.extend(targetLib.constraint_template_lines)
    outlines.extend(targetLib.delay_template_lines)
    outlines.extend(targetLib.recovery_template_lines)
    outlines.extend(targetLib.removal_template_lines)
    outlines.extend(targetLib.mpw_constraint_template_lines)
    outlines.extend(targetLib.passive_power_template_lines)
    outlines.extend(targetLib.power_template_lines)
    outlines.append("  input_voltage (default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_input) {\n")
    outlines.append("    vil : "+str(targetLib.vss_voltage)+";\n")
    outlines.append("    vih : "+str(targetLib.vdd_voltage)+";\n")
    outlines.append("    vimin : "+str(targetLib.vss_voltage)+";\n")
    outlines.append("    vimax : "+str(targetLib.vdd_voltage)+";\n")
    outlines.append("  }\n")
    outlines.append("  output_voltage (default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_output) {\n")
    outlines.append("    vol : "+str(targetLib.vss_voltage)+";\n")
    outlines.append("    voh : "+str(targetLib.vdd_voltage)+";\n")
    outlines.append("    vomin : "+str(targetLib.vss_voltage)+";\n")
    outlines.append("    vomax : "+str(targetLib.vdd_voltage)+";\n")
    outlines.append("  }\n")
    outlines.extend(targetLib.wireload_lines) 
    f.writelines(outlines)
  f.close()
  targetLib.set_exported()


## export harness data to .lib
def exportHarness(targetLib, targetCell, harnessList2):
  with open(targetLib.tmp_file, 'a') as f:
    outlines = []
    outlines.append("  cell ("+targetCell.cell+") {\n") ## cell start
    outlines.append("    area : "+str(targetCell.area)+";\n")
    ##outlines.append("    cell_leakage_power : "+targetCell.pleak+";\n")
    outlines.append("    cell_leakage_power : "+harnessList2[0][0].pleak+";\n") ## use leak of 1st harness
    outlines.append("    pg_pin ("+targetLib.vdd_name+"){\n")
    outlines.append("      pg_type : primary_power;\n")
    outlines.append("      voltage_name : \""+targetLib.vdd_name+"\";\n")
    outlines.append("    }\n")
    outlines.append("    pg_pin ("+targetLib.vss_name+"){\n")
    outlines.append("      pg_type : primary_ground;\n")
    outlines.append("      voltage_name : \""+targetLib.vss_name+"\";\n")
    outlines.append("    }\n")

    ## select one output pin from pinlist(target_outports) 
    for target_outport in targetCell.outports:
      index1 = targetCell.outports.index(target_outport) 
      outlines.append("    pin ("+target_outport+"){\n") ## out pin start
      outlines.append("      direction : output;\n")
      outlines.append("      function : \"("+targetCell.functions[index1]+")\"\n")
      outlines.append("      related_power_pin : \""+targetLib.vdd_name+"\";\n")
      outlines.append("      related_ground_pin : \""+targetLib.vss_name+"\";\n")
      outlines.append("      max_capacitance : \""+str(targetCell.load[-1])+"\";\n") ## use max val. of load table
      outlines.append("      output_voltage : default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_output;\n")
      ## timing
      for target_inport in targetCell.inports:
        outlines.append("      timing () {\n")
        index2 = targetCell.inports.index(target_inport) 
        outlines.append("        related_pin : \""+target_inport+"\";\n")
        outlines.append("        timing_sense : \""+harnessList2[index1][index2*2].timing_sense+"\";\n")
        outlines.append("        timing_type : \""+harnessList2[index1][index2*2].timing_type+"\";\n")
        ## rise
        ## propagation delay
        #outlines.append("        "+harnessList2[index1][index2*2].direction_prop+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2].direction_prop+ " ("+targetCell.delay_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2].lut_prop:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## transition delay
        #outlines.append("        "+harnessList2[index1][index2*2].direction_tran+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2].direction_tran+" ("+targetCell.delay_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2].lut_tran:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## fall
        ## propagation delay
        #outlines.append("        "+harnessList2[index1][index2*2+1].direction_prop+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+1].direction_prop+" ("+targetCell.delay_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2+1].lut_prop:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## transition delay
        #outlines.append("        "+harnessList2[index1][index2*2+1].direction_tran+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+1].direction_tran+" ("+targetCell.delay_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2+1].lut_tran:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        outlines.append("      }\n") ## timing end 
      ## power
      for target_inport in targetCell.inports:
        outlines.append("      internal_power () {\n")
        index2 = targetCell.inports.index(target_inport) 
        outlines.append("        related_pin : \""+target_inport+"\";\n")
        ## rise(fall)
        #outlines.append("        "+harnessList2[index1][index2*2].direction_power+" (power_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2].direction_power+" ("+targetCell.power_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2].lut_eintl:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## fall(rise)
        #outlines.append("        "+harnessList2[index1][index2*2+1].direction_power+" (power_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+1].direction_power+" ("+targetCell.power_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2+1].lut_eintl:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        outlines.append("      }\n") ## power end 
      outlines.append("    }\n") ## out pin end

    ## select one input pin from pinlist(target_inports) 
    for target_inport in targetCell.inports:
      index1 = targetCell.inports.index(target_inport) 
      outlines.append("    pin ("+target_inport+"){\n") ## out pin start
      outlines.append("      direction : input; \n")
      outlines.append("      related_power_pin : "+targetLib.vdd_name+";\n")
      outlines.append("      related_ground_pin : "+targetLib.vss_name+";\n")
      outlines.append("      max_transition : "+str(targetCell.slope[-1])+";\n")
      outlines.append("      capacitance : \""+str(targetCell.cins[index1])+"\";\n")
      outlines.append("      input_voltage : default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_input;\n")
      outlines.append("    }\n") ## in pin end

    outlines.append("  }\n") ## cell end
    f.writelines(outlines)
  f.close()
  targetCell.set_exported()

## export harness data to .lib
def exportHarnessFlop(targetLib, targetCell, harnessList2):
  with open(targetLib.tmp_file, 'a') as f:
    outlines = []
    outlines.append("  cell ("+targetCell.cell+") {\n") #### cell start
    outlines.append("    area : "+str(targetCell.area)+";\n")
##    outlines.append("    cell_leakage_power : "+targetCell.leak+";\n")
    outlines.append("    pg_pin ("+targetLib.vdd_name+"){\n")
    outlines.append("      pg_type : primary_power;\n")
    outlines.append("      voltage_name : \""+targetLib.vdd_name+"\";\n")
    outlines.append("    }\n")
    outlines.append("    pg_pin ("+targetLib.vss_name+"){\n")
    outlines.append("      pg_type : primary_ground;\n")
    outlines.append("      voltage_name : \""+targetLib.vss_name+"\";\n")
    outlines.append("    }\n")

    ## define flop
    outlines.append("    ff ("+str(targetCell.flops[0])+","+str(targetCell.flops[1])+"){\n") 
    outlines.append("    clocked_on : \""+targetCell.clock+"\";\n") 
    for target_inport in targetCell.inports:
      outlines.append("    next_state : \""+target_inport+"\";\n") 
    if targetCell.reset is not None:
      if(re.search('PR', targetCell.reset)):  ## posedge async. reset
        outlines.append("    clear : \""+targetCell.reset+"\";\n")   
      else:
        outlines.append("    clear : \"!"+targetCell.reset+"\";\n") 
    if targetCell.set is not None:
      if(re.search('PS', targetCell.set)):  ## posedge async. set
        outlines.append("    preset : \""+targetCell.set+"\";\n") 
      else:
        outlines.append("    preset : \"!"+targetCell.set+"\";\n") 
      if targetCell.reset is not None:
        ## value when set and reset both activate
        ## tool does not support this simulation, so hard coded to low
        outlines.append("    clear_preset_var1 : L ;\n") 
        outlines.append("    clear_preset_var2 : L ;\n") 
    outlines.append("    }\n") 
    ##
    ## (1) clock
    ##
    if targetCell.clock is not None:
      # index1 = targetCell.clock.index(target_clock) 
      index1 = 0 
      target_inport = targetCell.clock
      outlines.append("    pin ("+target_inport+"){\n") ## clock pin start 
      outlines.append("      direction : input;\n")
      outlines.append("      related_power_pin : \""+targetLib.vdd_name+"\";\n")
      outlines.append("      related_ground_pin : \""+targetLib.vss_name+"\";\n")
      outlines.append("      max_transition : "+str(targetCell.slope[-1])+";\n")
      #targetLib.print_msg(targetCell.cclks)
      outlines.append("      capacitance : \""+str(targetCell.cclks[index1])+"\";\n")
      outlines.append("      input_voltage : default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_input;\n")
      outlines.append("      clock : true;\n") 
  #   internal_power() {
  #     rise_power(passive_energy_template_7x1) {
  #       index_1 ("0.01669, 0.030212, 0.094214, 0.230514, 0.461228, 0.919101, 2.29957");
  #       values ("0.040923, 0.0374, 0.044187, 0.046943, 0.045139, 0.051569, 0.080466");
  #     }
  #     fall_power(passive_energy_template_7x1) {
  #       index_1 ("0.016236, 0.030811, 0.094437, 0.232485, 0.461801, 0.919137, 2.29958");
  #       values ("0.038868, 0.03793, 0.033501, 0.043008, 0.042432, 0.048973, 0.08357");
  #     }
  #   }
  #   min_pulse_width_high : 0.145244;
  #   min_pulse_width_low : 0.226781;
      outlines.append("    }\n") ## clock pin end



    ##
    ## (2) prop/tran/setup/hold for input pins 
    ##
    for target_inport in targetCell.inports:
      for target_outport in targetCell.outports:
        ## select inport with setup/hold informatioin
        index2 = targetCell.inports.index(target_inport) 
        index1 = targetCell.outports.index(target_outport) 
        #print(harnessList2[index1][index2*2].timing_type_setup)
        if((harnessList2[index1][index2*2].timing_type_setup == "setup_rising") or (harnessList2[index1][index2*2].timing_type_setup == "setup_falling")):
          outlines.append("    pin ("+target_inport+"){\n") #### inport pin start 
          outlines.append("      direction : input;\n")
          outlines.append("      related_power_pin : \""+targetLib.vdd_name+"\";\n")
          outlines.append("      related_ground_pin : \""+targetLib.vss_name+"\";\n")
          outlines.append("      max_transition : "+str(targetCell.slope[-1])+";\n")
#          targetLib.print_msg(targetCell.cins)
#          targetLib.print_msg(targetCell)
#          targetLib.print_msg(targetCell.inports)
#          targetLib.print_msg(targetCell.outports)
#          targetLib.print_msg(target_outport)
          outlines.append("      capacitance : \""+str(targetCell.cins[index1])+"\";\n")
          outlines.append("      input_voltage : default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_input;\n")
          ## (2-1) setup
          outlines.append("      timing () {\n")
          outlines.append("        related_pin : \""+targetCell.clock+"\";\n")
          outlines.append("        timing_type : \""+harnessList2[index1][index2*2].timing_type_setup+"\";\n")
          ## setup rise
          #outlines.append("        "+harnessList2[index1][index2*2].timing_sense_setup+" (constraint_template) {\n")
          outlines.append("        "+harnessList2[index1][index2*2].timing_sense_setup+" ("+targetCell.constraint_template_name+") {\n")
          for lut_line in harnessList2[index1][index2*2].lut_setup:
            outlines.append("          "+lut_line+"\n")
          outlines.append("        }\n") 
          ## setup fall
          #outlines.append("        "+harnessList2[index1][index2*2+1].timing_sense_setup+" (constraint_template) {\n")
          outlines.append("        "+harnessList2[index1][index2*2+1].timing_sense_setup+" ("+targetCell.constraint_template_name+") {\n")
          for lut_line in harnessList2[index1][index2*2+1].lut_setup:
            outlines.append("          "+lut_line+"\n")
          outlines.append("        }\n")
                                        
          outlines.append("      }\n") 
          ## (2-2) hold
          outlines.append("      timing () {\n")
          index1 = targetCell.outports.index(target_outport) 
          outlines.append("        related_pin : \""+targetCell.clock+"\";\n")
          outlines.append("        timing_type : \""+harnessList2[index1][index2*2].timing_type_hold+"\";\n")
          ## hold rise
          #outlines.append("        "+harnessList2[index1][index2*2].timing_sense_hold+" (constraint_template) {\n")
          outlines.append("        "+harnessList2[index1][index2*2].timing_sense_hold+" ("+targetCell.constraint_template_name+") {\n")
          for lut_line in harnessList2[index1][index2*2].lut_hold:
            outlines.append("          "+lut_line+"\n")
          outlines.append("        }\n") 
          ## hold fall
          #outlines.append("        "+harnessList2[index1][index2*2+1].timing_sense_hold+" (constraint_template) {\n")
          outlines.append("        "+harnessList2[index1][index2*2+1].timing_sense_hold+" ("+targetCell.constraint_template_name+") {\n")
          for lut_line in harnessList2[index1][index2*2+1].lut_hold:
            outlines.append("          "+lut_line+"\n")
          outlines.append("        }\n") 
          outlines.append("      }\n") 
    outlines.append("    }\n") ## inport pin end

    ##
    ## (3) outport 
    ##
    for target_outport in targetCell.outports:
      index1 = targetCell.outports.index(target_outport) 
      outlines.append("    pin ("+target_outport+"){\n") #### out pin start
      outlines.append("      direction : output;\n")
      outlines.append("      function : \"("+targetCell.functions[index1]+")\"\n")
      outlines.append("      related_power_pin : \""+targetLib.vdd_name+"\";\n")
      outlines.append("      related_ground_pin : \""+targetLib.vss_name+"\";\n")
      outlines.append("      max_capacitance : \""+str(targetCell.load[-1])+"\";\n") ## use max val. of load table
      outlines.append("      output_voltage : default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_output;\n")
      ## (3-1) clock
      if targetCell.clock is not None:
        ## index2 is a base pointer for harness search
        ## index2_offset and index2_offset_max are used to 
        ## search harness from harnessList2 which contain "timing_type_set"
        index2 = targetCell.outports.index(target_outport) 
        index2_offset = 0
        index2_offset_max = 10
        while(index2_offset < index2_offset_max):
          if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_setup"):
            break
          index2_offset += 1
        if(index2_offset == 10):
          print("Error: index2_offset exceed max. search number\n")
          my_exit()

        ##target_inport = targetCell.clock
        outlines.append("      timing () {\n")
        outlines.append("        related_pin : \""+targetCell.clock+"\";\n")
        outlines.append("        timing_type : \""+harnessList2[index1][index2*2+index2_offset].timing_type_clock+"\";\n")
        outlines.append("        timing_sense : \""+harnessList2[index1][index2*2+index2_offset].timing_sense_clock+"\";\n")
        #### (3-1-1) rise
        ## propagation delay
        #outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_prop+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_prop+" ("+targetCell.delay_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2+index2_offset].lut_prop:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## transition delay
        #outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_tran+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_tran+" ("+targetCell.delay_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2+index2_offset].lut_tran:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        #### (3-1-2) fall
        ## propagation delay
        #outlines.append("        "+harnessList2[index1][index2*2+index2_offset+1].direction_prop+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+index2_offset+1].direction_prop+" ("+targetCell.delay_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2+index2_offset+1].lut_prop:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## transition delay
        #outlines.append("        "+harnessList2[index1][index2*2+index2_offset+1].direction_tran+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+index2_offset+1].direction_tran+" ("+targetCell.delay_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2+index2_offset+1].lut_tran:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        outlines.append("      }\n") ## timing end 
      ##outlines.append("    }\n") ## out pin end -> continue for reset

      ## (3-2) reset (one directrion)
      if targetCell.reset is not None:
        ##target_inport = targetCell.reset
        outlines.append("      timing () {\n")

        ## Harness search for reset
        ## index2 is an base pointer for harness search
        ## index2_offset and index2_offset_max are used to 
        ## search harness from harnessList2 which contain "timing_type_set"
        index2 = targetCell.outports.index(target_outport) 
        index2_offset = 0
        index2_offset_max = 10
        while(index2_offset < index2_offset_max):
          #print(harnessList2[index1][index2*2+index2_offset])
          if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_reset"):
            break
          index2_offset += 1
        if(index2_offset == 10):
          print("Error: index2_offset exceed max. search number\n")
          my_exit()

        outlines.append("        related_pin : \""+targetCell.reset+"\";\n")
        outlines.append("        timing_sense : \""+harnessList2[index1][index2*2+index2_offset].timing_sense_reset+"\";\n")
        outlines.append("        timing_type : \""+harnessList2[index1][index2*2+index2_offset].timing_type_reset+"\";\n")
        ## (3-2-1) propagation delay
        #outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_reset_prop+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_reset_prop+" ("+targetCell.delay_template_name+") {\n")
        #for lut_line in harnessList2[index1][index2*2+index2_offset].lut_prop:
        for lut_line in harnessList2[index1][index2*2+index2_offset].lut_prop_reset:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## (3-2-2) transition delay
        #outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_reset_tran+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_reset_tran+" ("+targetCell.delay_template_name+") {\n")
        #for lut_line in harnessList2[index1][index2*2+index2_offset].lut_tran:
        for lut_line in harnessList2[index1][index2*2+index2_offset].lut_tran_reset:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        outlines.append("      }\n") 
      ##outlines.append("    }\n") #### out pin end -> continue for set

      ## (3-3) set (one directrion)
      if targetCell.set is not None:
        ##target_inport = targetCell.set
        outlines.append("      timing () {\n")
        ## Harness search for set
        ## index2 is an base pointer for harness search
        ## index2_offset and index2_offset_max are used to 
        ## search harness from harnessList2 which contain "timing_type_set"
        index2 = targetCell.outports.index(target_outport) 
        index2_offset = 0
        index2_offset_max = 10
        while(index2_offset < index2_offset_max):
          if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_set"):
            break
          index2_offset += 1
        if(index2_offset == 10):
          print("Error: index2_offset exceed max. search number\n")
          my_exit()

        outlines.append("        related_pin : \""+targetCell.set+"\";\n")
        outlines.append("        timing_sense : \""+harnessList2[index1][index2*2+index2_offset].timing_sense_set+"\";\n")
        outlines.append("        timing_type : \""+harnessList2[index1][index2*2+index2_offset].timing_type_set+"\";\n")
        ## (3-3-1) propagation delay
        #outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_set_prop+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_set_prop+" ("+targetCell.delay_template_name+") {\n")
        #for lut_line in harnessList2[index1][index2*2+index2_offset].lut_prop:
        for lut_line in harnessList2[index1][index2*2+index2_offset].lut_prop_set:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## (3-3-2) transition delay
        #outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_set_tran+" (delay_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+index2_offset].direction_set_tran+" ("+targetCell.delay_template_name+") {\n")
        #for lut_line in harnessList2[index1][index2*2+index2_offset].lut_tran:
        for lut_line in harnessList2[index1][index2*2+index2_offset].lut_tran_set:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        outlines.append("      }\n") 
      ##outlines.append("    }\n") #### out pin end
      
      ## (3-4) clock power
      if targetCell.clock is not None:
        ## index2 is a base pointer for harness search
        ## index2_offset and index2_offset_max are used to 
        ## search harness from harnessList2 which contain "timing_type_set"
        index2 = targetCell.outports.index(target_outport) 
        index2_offset = 0
        index2_offset_max = 10
        while(index2_offset < index2_offset_max):
          if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_setup"):
            break
          index2_offset += 1
        if(index2_offset == 10):
          print("Error: index2_offset exceed max. search number\n")
          my_exit()

        outlines.append("      internal_power () {\n")
        index2 = targetCell.inports.index(target_inport) 
        outlines.append("        related_pin : \""+targetCell.clock+"\";\n")
        ## rise(fall)
        #outlines.append("        "+harnessList2[index1][index2*2].direction_power+" (power_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2].direction_power+" ("+targetCell.power_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2].lut_eintl:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## fall(rise)
        #outlines.append("        "+harnessList2[index1][index2*2+1].direction_power+" (power_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+1].direction_power+" ("+targetCell.power_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2+1].lut_eintl:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        outlines.append("      }\n") ## power end 

      ## (3-5) reset power 
      if targetCell.reset is not None:

        ## Harness search for reset
        ## index2 is an base pointer for harness search
        ## index2_offset and index2_offset_max are used to 
        ## search harness from harnessList2 which contain "timing_type_set"
        index2 = targetCell.outports.index(target_outport) 
        index2_offset = 0
        index2_offset_max = 10
        while(index2_offset < index2_offset_max):
          #print(harnessList2[index1][index2*2+index2_offset])
          if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_reset"):
            break
          index2_offset += 1
        if(index2_offset == 10):
          print("Error: index2_offset exceed max. search number\n")
          my_exit()

        outlines.append("      internal_power () {\n")
        index2 = targetCell.inports.index(target_inport) 
        outlines.append("        related_pin : \""+targetCell.reset+"\";\n")
        ## rise(fall)
        #outlines.append("        "+harnessList2[index1][index2*2].direction_power+" (power_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2].direction_power+" ("+targetCell.power_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2].lut_eintl:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## fall(rise)
        #outlines.append("        "+harnessList2[index1][index2*2+1].direction_power+" (power_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+1].direction_power+" ("+targetCell.power_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2+1].lut_eintl:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        outlines.append("      }\n") ## power end 

      ## (3-6) set power 
      if targetCell.set is not None:

        ## Harness search for set
        ## index2 is an base pointer for harness search
        ## index2_offset and index2_offset_max are used to 
        ## search harness from harnessList2 which contain "timing_type_set"
        index2 = targetCell.outports.index(target_outport) 
        index2_offset = 0
        index2_offset_max = 10
        while(index2_offset < index2_offset_max):
          #print(harnessList2[index1][index2*2+index2_offset])
          if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_set"):
            break
          index2_offset += 1
        if(index2_offset == 10):
          print("Error: index2_offset exceed max. search number\n")
          my_exit()

        outlines.append("      internal_power () {\n")
        index2 = targetCell.inports.index(target_inport) 
        outlines.append("        related_pin : \""+targetCell.set+"\";\n")
        ## rise(fall)
        #outlines.append("        "+harnessList2[index1][index2*2].direction_power+" (power_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2].direction_power+" ("+targetCell.power_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2].lut_eintl:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        ## fall(rise)
        #outlines.append("        "+harnessList2[index1][index2*2+1].direction_power+" (power_template) {\n")
        outlines.append("        "+harnessList2[index1][index2*2+1].direction_power+" ("+targetCell.power_template_name+") {\n")
        for lut_line in harnessList2[index1][index2*2+1].lut_eintl:
          outlines.append("          "+lut_line+"\n")
        outlines.append("        }\n") 
        outlines.append("      }\n") ## power end 
      ##outlines.append("    }\n") #### out pin end
    outlines.append("    }\n") ## out pin end

    ## (4) Reset
    if targetCell.reset is not None:
      # for target_reset in targetCell.reset:
      target_reset = targetCell.reset
      index1 = targetCell.reset.index(target_reset) 
      outlines.append("    pin ("+target_reset+"){\n") #### out pin start
      outlines.append("      direction : input;\n")
      #outlines.append("      function : \"("+targetCell.functions[index1]+")\"\n")
      outlines.append("      related_power_pin : \""+targetLib.vdd_name+"\";\n")
      outlines.append("      related_ground_pin : \""+targetLib.vss_name+"\";\n")
      outlines.append("      max_transition : "+str(targetCell.slope[-1])+";\n")
      #targetLib.print_msg(targetCell.crsts)
      ##outlines.append("      capacitance : \""+str(targetCell.crsts[index1])+"\";\n")
      outlines.append("      capacitance : \""+str(targetCell.crsts[0])+"\";\n") # use 0 as representative
      outlines.append("      input_voltage : default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_input;\n")
      ##target_inport = targetCell.reset
  
      ## Harness search for reset
      ## index2 is an base pointer for harness search
      ## index2_offset and index2_offset_max are used to 
      ## search harness from harnessList2 which contain "timing_type_set"
      index2 = targetCell.outports.index(target_outport) 
      index2_offset = 0
      index2_offset_max = 10
      while(index2_offset < index2_offset_max):
        #print(harnessList2[index1][index2*2+index2_offset])
        if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_reset"):
          break
        index2_offset += 1
      if(index2_offset == 10):
        print("Error: index2_offset exceed max. search number\n")
        my_exit()
      #for a in inspect.getmembers(harnessList2[index1][index2*2+index2_offset]):
      #  print (a) 
      ## (4-1) recovery
      outlines.append("      timing () {\n")
      outlines.append("        related_pin : \""+targetCell.clock+"\";\n")
      outlines.append("        timing_type : \""+harnessList2[index1][index2*2+index2_offset].timing_type_reset_recov+"\";\n")
      if (1 != len(targetCell.inports)):
        print ("Error: number of targetCell.inports is "+str(len(targetCell.inports))+", not one! die" )
        my_exit()
      #for target_inport in targetCell.inports: ## only one target_inport should be available
      #  outlines.append("        when : \""+harnessList2[index1][index2*2+index2_offset].timing_type_reset+"\";\n")
      #outlines.append("        "+harnessList2[index1][index2*2+index2_offset].timing_sense_reset_recov+" (recovery_template) {\n")
      outlines.append("        "+harnessList2[index1][index2*2+index2_offset].timing_sense_reset_recov+" ("+targetCell.recovery_template_name+") {\n")
      for lut_line in harnessList2[index1][index2*2+index2_offset].lut_setup:
        outlines.append("          "+lut_line+"\n")
      outlines.append("        }\n") 
      outlines.append("      }\n") 
      ## (4-2)removal 
      outlines.append("      timing () {\n")
      outlines.append("        related_pin : \""+targetCell.clock+"\";\n")
      outlines.append("        timing_type : \""+harnessList2[index1][index2*2+index2_offset].timing_type_reset_remov+"\";\n")
      if (1 != len(targetCell.inports)):
        print ("Error: number of targetCell.inports is "+str(len(targetCell.inports))+", not one! die" )
        my_exit()
      #for target_inport in targetCell.inports: ## only one target_inport should be available
      #  outlines.append("        when : \""+harnessList2[index1][index2*2+index2_offset].timing_type_reset+"\";\n")
      #outlines.append("        "+harnessList2[index1][index2*2+index2_offset].timing_sense_reset_remov+" (removal_template) {\n")
      outlines.append("        "+harnessList2[index1][index2*2+index2_offset].timing_sense_reset_remov+" ("+targetCell.removal_template_name+") {\n")
      for lut_line in harnessList2[index1][index2*2+index2_offset].lut_hold:
        outlines.append("          "+lut_line+"\n")
      outlines.append("        }\n") 
      outlines.append("      }\n")
                        
    if targetCell.reset is not None:
            outlines.append("    }\n") #### out pin end -> continue for set

    ## (5) set
    if targetCell.set is not None:
      #for target_set in targetCell.set:
      target_set = targetCell.set
      index1 = targetCell.set.index(target_set) 
      outlines.append("    pin ("+target_set+"){\n") #### out pin start
      outlines.append("      direction : input;\n")
      #outlines.append("      function : \"("+targetCell.functions[index1]+")\"\n")
      outlines.append("      related_power_pin : \""+targetLib.vdd_name+"\";\n")
      outlines.append("      related_ground_pin : \""+targetLib.vss_name+"\";\n")
      outlines.append("      max_transition : "+str(targetCell.slope[-1])+";\n")
      #targetLib.print_msg(targetCell.csets)
      #outlines.append("      capacitance : \""+str(targetCell.csets[index1])+"\";\n")
      outlines.append("      capacitance : \""+str(targetCell.csets[0])+"\";\n") # use 0 as representative val
      outlines.append("      input_voltage : default_"+targetLib.vdd_name+"_"+targetLib.vss_name+"_input;\n")
      ##target_inport = targetCell.set
  
      ## Harness search for set
      ## index2 is an base pointer for harness search
      ## index2_offset and index2_offset_max are used to 
      ## search harness from harnessList2 which contain "timing_type_set"
      index2 = targetCell.outports.index(target_outport) 
      index2_offset = 0
      index2_offset_max = 10
      while(index2_offset < index2_offset_max):
        #print(harnessList2[index1][index2*2+index2_offset])
        if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_set"):
          break
        index2_offset += 1
      if(index2_offset == 10):
        print("Error: index2_offset exceed max. search number\n")
        my_exit()
  
      ## (5-1) recovery
      outlines.append("      timing () {\n")
      outlines.append("        related_pin : \""+targetCell.clock+"\";\n")
      outlines.append("        timing_type : \""+harnessList2[index1][index2*2+index2_offset].timing_type_set_recov+"\";\n")
      if (1 != len(targetCell.inports)):
        print ("Error: number of targetCell.inports is "+str(len(targetCell.inports))+", not one! die" )
        my_exit()
      #for target_inport in targetCell.inports: ## only one target_inport should be available
      #  outlines.append("        when : \""+harnessList2[index1][index2*2+index2_offset].timing_type_set+"\";\n")
      #outlines.append("        "+harnessList2[index1][index2*2+index2_offset].timing_sense_set_recov+" (recovery_template) {\n")
      outlines.append("        "+harnessList2[index1][index2*2+index2_offset].timing_sense_set_recov+" ("+targetCell.recovery_template_name+") {\n")
      for lut_line in harnessList2[index1][index2*2+index2_offset].lut_setup:
        outlines.append("          "+lut_line+"\n")
      outlines.append("        }\n") 
      outlines.append("      }\n") 
  
      ## (5-2)removal 
      outlines.append("      timing () {\n")
      outlines.append("        related_pin : \""+targetCell.clock+"\";\n")
      outlines.append("        timing_type : \""+harnessList2[index1][index2*2+index2_offset].timing_type_set_remov+"\";\n")
      if (1 != len(targetCell.inports)):
        print ("Error: number of targetCell.inports is "+str(len(targetCell.inports))+", not one! die" )
        my_exit()
      #for target_inport in targetCell.inports: ## only one target_inport should be available
      #  outlines.append("        when : \""+harnessList2[index1][index2*2+index2_offset].timing_type_set+"\";\n")
      #outlines.append("        "+harnessList2[index1][index2*2+index2_offset].timing_sense_set_remov+" (removal_template) {\n")
      outlines.append("        "+harnessList2[index1][index2*2+index2_offset].timing_sense_set_remov+" ("+targetCell.removal_template_name+") {\n")
      for lut_line in harnessList2[index1][index2*2+index2_offset].lut_hold:
        outlines.append("          "+lut_line+"\n")
      outlines.append("        }\n") 
      outlines.append("      }\n")
                        
    if targetCell.set is not None:
            outlines.append("    }\n") #### out pin end -> continue for set

    outlines.append("  }\n") #### cell end
    f.writelines(outlines)
  f.close()
  targetCell.set_exported()

## export library definition to .lib
def exportVerilog(targetLib, targetCell):
  with open(targetLib.verilog_name, 'a') as f:
    outlines = []

    ## list ports in one line 
    portlist = "("
    numport = 0
    for target_outport in targetCell.outports:
      if(numport != 0):
        portlist = portlist+", "
      portlist = portlist+target_outport
      numport += 1
    for target_inport in targetCell.inports:
      portlist = portlist+","+target_inport
      numport += 1
    portlist = portlist+");"

    outlines.append("module "+targetCell.cell+portlist+"\n")

    ## input/output statement
    for target_outport in targetCell.outports:
      outlines.append("output "+target_outport+";\n")
    for target_inport in targetCell.inports:
      outlines.append("input "+target_inport+";\n")

    ## branch for sequencial cell
    if(targetCell.logic == "DFFARAS"):
      print ("This cell "+targetCell.logic+" is not supported for verilog out\n")
      my_exit()  

    ## branch for combinational cell
    else:
    ## assign statement
      for target_outport in targetCell.outports:
        index1 = targetCell.outports.index(target_outport) 
        outlines.append("assign "+target_outport+" = "+targetCell.functions[index1]+";\n")

    outlines.append("endmodule\n\n")
    f.writelines(outlines)
  f.close()

## export library definition to .lib
def exportVerilogFlop(targetLib, targetCell):
  with open(targetLib.verilog_name, 'a') as f:
    outlines = []

    ## list ports in one line 
    portlist = "("
    numport = 0
    for target_outport in targetCell.outports:
      if(numport != 0):
        portlist = portlist+", "
      portlist = portlist+target_outport
      numport += 1
    for target_inport in targetCell.inports:
      portlist = portlist+","+target_inport
      numport += 1
    if targetCell.clock is not None:
      portlist = portlist+","+targetCell.clock
      numport += 1
    if targetCell.reset is not None:
      portlist = portlist+","+targetCell.reset
      numport += 1
    if targetCell.set is not None:
      portlist = portlist+","+targetCell.set
      numport += 1
    portlist = portlist+");"

    outlines.append("module "+targetCell.cell+portlist+"\n")

    ## input/output statement
    for target_outport in targetCell.outports:
      #outlines.append("output "+target_outport+";\n")
      outlines.append("output reg "+target_outport+";\n")
    for target_inport in targetCell.inports:
      outlines.append("input "+target_inport+";\n")
    if targetCell.clock is not None:
      outlines.append("input "+targetCell.clock+";\n")
    if targetCell.reset is not None:
      outlines.append("input "+targetCell.reset+";\n")
    if targetCell.set is not None:
      outlines.append("input "+targetCell.set+";\n")

    ## assign statement
    for target_outport in targetCell.outports:
      for target_inport in targetCell.inports:
        line = 'always@('
        resetlines = []
        setlines = []
        #print(str(targetCell.logic))
        ## clock
        if(re.search('PC', targetCell.logic)):  ## posedge clock
          line=line+"posedge "+targetCell.clock
        elif(re.search('NC', targetCell.logic)):  ## negedge clock
          line=line+"negedge "+targetCell.clock
        else:
          print("Error! failed to generate DFF verilog!")
          my_exit()

        ## reset (option)
        if(targetCell.reset != None):  ## reset
          if(re.search('PR', targetCell.logic)):  ## posedge async. reset
            line=line+" or posedge "+targetCell.reset
            resetlines.append('if('+targetCell.reset+') begin\n')
            resetlines.append('  '+target_outport+'<=0;\n')
            resetlines.append('end else begin\n')
          elif(re.search('NR', targetCell.logic)):  ## negedge async. reset
            line=str(line)+" or negedge "+targetCell.reset
            resetlines.append('if(!'+targetCell.reset+') begin\n')
            resetlines.append('  '+target_outport+'<=0;\n')
            resetlines.append('end else begin\n')
        ## set (option)
        if(targetCell.set != None):  ## reset
          if(re.search('PS', targetCell.logic)):  ## posedge async. set 
            line=line+" or posedge "+targetCell.set
            setlines.append('if('+targetCell.set+') begin\n')
            setlines.append('  '+target_outport+'<=1;\n')
            setlines.append('end else begin\n')
          elif(re.search('NS', targetCell.logic)):  ## negedge async. set 
            line=line+" or negedge "+targetCell.set
            setlines.append('if(!'+targetCell.set+') begin\n')
            setlines.append('  '+target_outport+'<=1;\n')
            setlines.append('end else begin\n')
        line=line+")begin\n"
        outlines.append(line)
        if targetCell.set is not None:  
          outlines.append(setlines[0])
          outlines.append(setlines[1])
          outlines.append(setlines[2])
        if targetCell.reset is not None:  
          outlines.append(resetlines[0])
          outlines.append(resetlines[1])
          outlines.append(resetlines[2])
        outlines.append(target_outport+'<='+target_inport+';')
        outlines.append('\nend\n')
        outlines.append('end\n')
      ## for target_inport
    ## for target_outport
    outlines.append("endmodule\n\n")
    f.writelines(outlines)
  f.close()


## compress (Cristiano, 20240514)
def compressFiles(targetLib, targetCell):
  if(targetLib.compress == "true"):
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    targetLib.print_msg(dt_string+" creating "+targetCell.cell+" directory")
    cmd_str = "mkdir "+targetLib.work_dir+"/"+targetCell.cell 
    subprocess.run(cmd_str, shell=True)  
    targetLib.print_msg(dt_string+" compress "+targetCell.cell+" characterization result")
    cmd_str = "mv "+targetLib.work_dir+"/vt*"+targetCell.cell+"* "+targetLib.work_dir+"/"+targetCell.cell 
    subprocess.run(cmd_str, shell=True)  
    cmd_str = "tar -zcvf "+targetLib.work_dir+"/"+targetCell.cell+".tgz "+targetLib.work_dir+"/"+targetCell.cell 
    subprocess.run(cmd_str, shell=True)  

## export harness data to .lib
def exitFiles(targetLib, num_gen_file):
  cat_cmd = "cat "+str(targetLib.tmp_file)+" >> "+str(targetLib.dotlib_name)+" \n"
  with open("cat_run.sh",'w') as f:
    outlines = []
    outlines.append(cat_cmd) 
    f.writelines(outlines)
  f.close()
  cmd = ['sh', 'cat_run.sh']
  try:
    res = subprocess.check_call(cmd)
  except:
    print ("Failed to cat dotlib file")
  with open(targetLib.dotlib_name, 'a') as f:
    outlines = []
    outlines.append("}\n")
    f.writelines(outlines)
  f.close()
  print("\n-- dotlib file generation completed!!  ")
  print("--  "+str(num_gen_file)+" cells generated!!  \n")

