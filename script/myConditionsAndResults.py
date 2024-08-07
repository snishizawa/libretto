import argparse, re, os, shutil, subprocess
import numpy as np

class MyConditionsAndResults:
  def __init__ (self):
    self.instance = None          ## instance name
    self.target_inport = None     ## target inport name
    self.target_outport = None    ## target outport name
    self.stable_inport = []       ## stable imports
    self.stable_inport_val = []   ## stable imports val
    self.nontarget_outport = []   ## nontarget outport
    self.target_clock     = None  ## target clock name
    self.target_clock_val = None  ## target clock value
    self.target_reset     = None  ## target reset name
    self.target_reset_val = None  ## target reset val
    self.target_set     = None    ## target set name
    self.target_set_val = None    ## target set val
  
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
    self.direction_power = "rise_power"

  def set_direction_fall(self):
    self.direction_prop = "cell_fall"
    self.direction_tran = "fall_transition"
    self.direction_power = "fall_power"

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

  ## set timing_sense and timing_type for input/output
  def set_timing_flop_inout(self, inport="tmp", clkport="tmp",outport="tmp"):
    ## inport
    if((inport == 'pos')or(inport == '01')):
      self.timing_sense_setup = "rise_constraint"
      self.timing_sense_hold  = "rise_constraint"
    elif((inport == 'neg')or(inport == '10')):
      self.timing_sense_setup = "fall_constraint"
      self.timing_sense_hold  = "fall_constraint"
    else:
      print("Illegal input: "+inport+", check unate")
    ## outport
    if((outport == 'pos')or(outport == '01')):
      self.timing_type_out = "rising_edge"
    elif((outport == 'neg')or(outport == '10')):
      self.timing_type_out = "falling_edge"
    else:
      print("Illegal input: "+outport+", check unate")
    ## clkport
    self.timing_sense_clock = "non_unate"
    if(clkport == '0101'):
      #self.timing_type_clock = "setup_rising"
      self.timing_type_clock = "rising_edge"
      self.timing_type_setup = "setup_rising"
      self.timing_type_hold  = "hold_rising"
    elif(clkport == '1010'):
      #self.timing_type_clock = "setup_falling"
      self.timing_type_clock = "falling_edge"
      self.timing_type_setup = "setup_falling"
      self.timing_type_hold  = "hold_falling"
    else:
      print("Illegal clkput: "+clkport+", check unate")
  
# def set_timing_flop_clock(self, inport="0101", outport="01"):
#   ## inport
#   self.timing_sense_clock  = "non_unate"
#   if(inport == "0101"):
#     self.timing_type_clock = "rising_edge"
#   elif(inport == "1010"):
#     self.timing_type_clock = "falling_edge"
#   else:
#     self.timing_type_clock  = "NONE"
#   if((outport == "01")or(outport.upper() == "RISE")):
#     self.direction_clock_prop = "cell_rise"
#     self.direction_clock_tran = "rise_transition"
#   elif((outport == "10")or(outport.upper() == "FALL")):
#     self.direction_clock_prop = "cell_fall"
#     self.direction_clock_tran = "fall_transition"
#   else:
#     print("Warning: illigal outport type at set_timing_flop_set: "+str(inport))

  def set_timing_flop_set(self, targetCell, inport="01", outport="01", clkport="0101"):
    ## clkport
    if(clkport == '0101'):
      self.timing_type_set_recov = "recovery_rising"
      self.timing_type_set_remov = "removal_rising"
    elif(clkport == '1010'):
      self.timing_type_set_recov = "recovery_falling"
      self.timing_type_set_remov = "removal_falling"
    else:
      print("Illegal clkput: "+clkport+", check unate")

    ## inport
    if((inport == "01")or(inport.upper() == "RISE")):
      self.timing_sense_set = "positive_unate"
      self.timing_when = targetCell.set 
      self.timing_sense_set_recov = "fall_constraint"
      self.timing_sense_set_remov = "fall_constraint"
    elif((inport == "10")or(inport.upper() == "FALL")):
      self.timing_sense_set = "negative_unate"
      self.timing_when = "!"+targetCell.set 
      self.timing_sense_set_recov = "rise_constraint"
      self.timing_sense_set_remov = "rise_constraint"
    else:
      print("Warning: illigal inport type at set_timing_flop_set: "+str(inport))
    ## outport
    if((outport == "01")or(outport.upper() == "RISE")):
      self.timing_type_set = "preset"
      self.direction_set_prop = "cell_rise"
      self.direction_set_tran = "rise_transition"
    elif((outport == "10")or(outport.upper() == "FALL")):
      self.timing_type_set = "clear"
      self.direction_set_prop = "cell_fall"
      self.direction_set_tran = "fall_transition"
    else:
      print("Warning: illigal outport type at set_timing_flop_set: "+str(inport))

  def set_timing_flop_reset(self, targetCell, inport="01", outport="10", clkport="0101"):
    ## clkport
    if(clkport == '0101'):
      self.timing_type_reset_recov = "recovery_rising"
      self.timing_type_reset_remov = "removal_rising"
    elif(clkport == '1010'):
      self.timing_type_reset_recov = "recovery_falling"
      self.timing_type_reset_remov = "removal_falling"
    else:
      print("Illegal clkput: "+clkport+", check unate")
    ## inport
    if((inport == "01")or(inport.upper() == "RISE")):
      self.timing_sense_reset = "negative_unate"
      self.timing_when = targetCell.reset 
      self.timing_sense_reset_recov = "fall_constraint"
      self.timing_sense_reset_remov = "fall_constraint"
    elif((inport == "10")or(inport.upper() == "FALL")):
      self.timing_sense_reset = "positive_unate"
      self.timing_when = "!"+targetCell.reset 
      self.timing_sense_reset_recov = "rise_constraint"
      self.timing_sense_reset_remov = "rise_constraint"
    else:
      print("Warning: illigal inport type at set_timing_flop_reset: "+str(inport))
    ## outport
    if((outport == "01")or(outport.upper() == "RISE")):
      self.timing_type_reset = "preset"
      self.direction_reset_prop = "cell_rise"
      self.direction_reset_tran = "rise_transition"
    elif((outport == "10")or(outport.upper() == "FALL")):
      self.timing_type_reset = "clear"
      self.direction_reset_prop = "cell_fall"
      self.direction_reset_tran = "fall_transition"
    else:
      print("Warning: illigal outport type at set_timing_flop_reset: "+str(inport))

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

  def invert_set_reset_val(self):
    if(self.target_reset_val == '01'):
      self.target_reset_val = '10'
    elif(self.target_reset_val == '10'):
      self.target_reset_val = '01'
    if(self.target_set_val == '01'):
      self.target_set_val = '10'
    elif(self.target_set_val == '10'):
      self.target_set_val = '01'

  def invert_outport_val(self):
    if(self.target_outport_val == '01'):
      self.target_outport_val = '10'
    elif(self.target_outport_val == '10'):
      self.target_outport_val = '01'

  ## propagation delay table
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
    ## index_1
    outline = "index_1(\""
    self.lut_prop = []
    self.lut_prop_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_prop.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_prop.append(outline)
    ## values
    self.lut_prop.append("values ( \\")
    #print(self.list2_prop)
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_prop[i][j])+", "
        #print("i,j"+str(i)+","+str(j))
        #print(len(ilist))
        #print(len(jlist)-1)
        #print(len(self.list2_prop))
        #print([len(v) for v in self.list2_prop])
        #print(self.list2_prop[i][j])
        tmp_line = str("{:5f}".format(self.list2_prop[i][j]/targetLib.time_mag))
        outline += tmp_line+", "
      ## do not add "," for last line
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_prop[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_prop[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_prop[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_prop[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"
      self.lut_prop.append(outline)
    self.lut_prop.append(");")
    
    # store min/center/max for doc
    # min
    #self.lut_prop_mintomax.append(str("{:5f}".format(self.list2_prop[0][0]/targetLib.time_mag)))
    self.lut_prop_mintomax.append(str("{:5f}".format(np.amin(self.list2_prop)/targetLib.time_mag)))
    
    # center
    #self.lut_prop_mintomax.append(str("{:5f}".format(self.list2_prop[int(len(ilist))-1][int(len(jlist))-1]/targetLib.time_mag)))
    self.lut_prop_mintomax.append(str("{:5f}".format(np.median(self.list2_prop)/targetLib.time_mag)))

    # max
    #self.lut_prop_mintomax.append(str("{:5f}".format(self.list2_prop[-1][-1]/targetLib.time_mag)))
    self.lut_prop_mintomax.append(str("{:5f}".format(np.amax(self.list2_prop)/targetLib.time_mag)))
    
  ## transient delay table
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
    ## index_1
    outline = "index_1(\""
    self.lut_tran = []
    self.lut_tran_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_tran.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_tran.append(outline)
    ## values
    self.lut_tran.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_tran[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_tran[i][j]/targetLib.time_mag))
        outline += tmp_line+", "
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_tran[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_tran[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_tran[i][len(jlist)-1])+"\", \\"
        #tmp_line = str("{:5f}".format(self.list2_prop[i][len(jlist)-1]/targetLib.time_mag))
        tmp_line = str("{:5f}".format(self.list2_tran[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"
      self.lut_tran.append(outline)
    self.lut_tran.append(");")
    
    # store min/center/max for doc
    # min
    self.lut_tran_mintomax.append(str("{:5f}".format(np.amin(self.list2_tran)/targetLib.time_mag)))
    # center
    self.lut_tran_mintomax.append(str("{:5f}".format(np.median(self.list2_tran)/targetLib.time_mag)))
    # max
    self.lut_tran_mintomax.append(str("{:5f}".format(np.amax(self.list2_tran)/targetLib.time_mag)))

  ## propagation delay table for set
  def set_list2_prop_set(self, list2_prop_set=[]):
    self.list2_prop_set = list2_prop_set 

  def print_list2_prop_set(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_prop_set[i][j])
  
  def print_lut_prop_set(self):
    for i in range(len(self.lut_prop_set)):
      print(self.lut_prop_set[i])

  def write_list2_prop_set(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_prop_set = []
    self.lut_prop_set_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_prop_set.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_prop_set.append(outline)
    ## values
    self.lut_prop_set.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_prop_set[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_prop_set[i][j]/targetLib.time_mag))
        outline += tmp_line+", "
      ## do not add "," for last line
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_prop_set[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_prop_set[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_prop_set[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_prop_set[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"
      self.lut_prop_set.append(outline)
    self.lut_prop_set.append(");")
    
    # store min/center/max for doc
    # min
    self.lut_prop_set_mintomax.append(str("{:5f}".format(np.amin(self.list2_prop_set)/targetLib.time_mag)))
    # center
    self.lut_prop_set_mintomax.append(str("{:5f}".format(np.median(self.list2_prop_set)/targetLib.time_mag)))
    # max
    self.lut_prop_set_mintomax.append(str("{:5f}".format(np.amax(self.list2_prop_set)/targetLib.time_mag)))

  ## transient delay table for set
  def set_list2_tran_set(self, list2_tran_set=[]):
    self.list2_tran_set = list2_tran_set 

  def print_list2_tran_set(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_tran_set[i][j])
  
  def print_lut_tran_set(self):
    for i in range(len(self.lut_tran_set)):
      print(self.lut_tran_set[i])

  def write_list2_tran_set(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_tran_set = []
    self.lut_tran_set_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_tran_set.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_tran_set.append(outline)
    ## values
    self.lut_tran_set.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_tran_set[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_tran_set[i][j]/targetLib.time_mag))
        outline += tmp_line+", "
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_tran_set[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_tran_set[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_tran_set[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_tran_reset[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"
      self.lut_tran_set.append(outline)
    self.lut_tran_set.append(");")
    
    # store min/center/max for doc
    # min
    self.lut_tran_set_mintomax.append(str("{:5f}".format(np.amin(self.list2_tran_set)/targetLib.time_mag)))
    # center
    self.lut_tran_set_mintomax.append(str("{:5f}".format(np.median(self.list2_tran_set)/targetLib.time_mag)))
    # max
    self.lut_tran_set_mintomax.append(str("{:5f}".format(np.amax(self.list2_tran_set)/targetLib.time_mag)))

  ## propagation delay table for reset
  def set_list2_prop_reset(self, list2_prop_reset=[]):
    self.list2_prop_reset = list2_prop_reset 

  def print_list2_prop_reset(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_prop_reset[i][j])
  
  def print_lut_prop_reset(self):
    for i in range(len(self.lut_prop_reset)):
      print(self.lut_prop_reset[i])

  def write_list2_prop_reset(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_prop_reset = []
    self.lut_prop_reset_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_prop_reset.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_prop_reset.append(outline)
    ## values
    self.lut_prop_reset.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_prop_reset[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_prop_reset[i][j]/targetLib.time_mag))
        outline += tmp_line+", "
      ## do not add "," for last line
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_prop_reset[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_prop_reset[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_prop_reset[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_prop_reset[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"
      self.lut_prop_reset.append(outline)
    self.lut_prop_reset.append(");")
    
    # store min/center/max for doc
    # min
    self.lut_prop_reset_mintomax.append(str("{:5f}".format(np.amin(self.list2_prop_reset)/targetLib.time_mag)))
    # center
    self.lut_prop_reset_mintomax.append(str("{:5f}".format(np.median(self.list2_prop_reset)/targetLib.time_mag)))
    # max
    self.lut_prop_reset_mintomax.append(str("{:5f}".format(np.amax(self.list2_prop_reset)/targetLib.time_mag)))

  ## transient delay table for set
  def set_list2_tran_set(self, list2_tran_set=[]):
    self.list2_tran_set = list2_tran_set 

  def print_list2_tran_set(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_tran_set[i][j])
  
  def print_lut_tran_set(self):
    for i in range(len(self.lut_tran_set)):
      print(self.lut_tran_set[i])

  def write_list2_tran_set(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_tran_set = []
    self.lut_tran_set_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_tran_set.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_tran_set.append(outline)
    ## values
    self.lut_tran_set.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_tran_set[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_tran_set[i][j]/targetLib.time_mag))
        outline += tmp_line+", "
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_tran_set[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_tran_set[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_tran_set[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_tran_reset[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"
      self.lut_tran_set.append(outline)
    self.lut_tran_set.append(");")

    # store min/center/max for doc
    # min
    self.lut_tran_set_mintomax.append(str("{:5f}".format(np.amin(self.list2_tran_set)/targetLib.time_mag)))
    # center
    self.lut_tran_set_mintomax.append(str("{:5f}".format(np.median(self.list2_tran_set)/targetLib.time_mag)))
    # max
    self.lut_tran_set_mintomax.append(str("{:5f}".format(np.amax(self.list2_tran_set)/targetLib.time_mag)))
    
  ## internal power (energy) table 
  def set_list2_eintl(self, list2_eintl=[]):
    self.list2_eintl = list2_eintl 

  def print_list2_eintl(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_eintl[i][j])
  
  def print_lut_eintl(self):
    for i in range(len(self.lut_eintl)):
      print(self.lut_eintl[i])

  def write_list2_eintl(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_eintl = []
    self.lut_eintl_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_eintl.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_eintl.append(outline)
    ## values
    self.lut_eintl.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_eintl[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_eintl[i][j]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+", "
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_eintl[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_eintl[i][len(jlist)-1]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_eintl[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_eintl[i][len(jlist)-1]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+"\" \\"
      self.lut_eintl.append(outline)
    self.lut_eintl.append(");")
    
    # store min/center/max for doc
    # min
    self.lut_eintl_mintomax.append(str("{:5f}".format(np.amin(self.list2_eintl)*targetLib.voltage_mag/targetLib.energy_mag)))
    # center
    self.lut_eintl_mintomax.append(str("{:5f}".format(np.median(self.list2_eintl)*targetLib.voltage_mag/targetLib.energy_mag)))
    # max
    self.lut_eintl_mintomax.append(str("{:5f}".format(np.amax(self.list2_eintl)*targetLib.voltage_mag/targetLib.energy_mag)))

  ## propagation delay table for reset
  def set_list2_prop_reset(self, list2_prop_reset=[]):
    self.list2_prop_reset = list2_prop_reset 

  def print_list2_prop_reset(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_prop_reset[i][j])
  
  def print_lut_prop_reset(self):
    for i in range(len(self.lut_prop_reset)):
      print(self.lut_prop_reset[i])

  def write_list2_prop_reset(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_prop_reset = []
    self.lut_prop_reset_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_prop_reset.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_prop_reset.append(outline)
    ## values
    self.lut_prop_reset.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_prop_reset[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_prop_reset[i][j]/targetLib.time_mag))
        outline += tmp_line+", "
      ## do not add "," for last line
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_prop_reset[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_prop_reset[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_prop_reset[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_prop_reset[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"
      self.lut_prop_reset.append(outline)
    self.lut_prop_reset.append(");")

    # store min/center/max for doc
    # min
    self.lut_prop_reset_mintomax.append(str("{:5f}".format(np.amin(self.list2_prop_reset)/targetLib.time_mag)))
    # center
    self.lut_prop_reset_mintomax.append(str("{:5f}".format(np.median(self.list2_prop_reset)/targetLib.time_mag)))
    # max
    self.lut_prop_reset_mintomax.append(str("{:5f}".format(np.amax(self.list2_prop_reset)/targetLib.time_mag)))

    
  ## transient delay table for reset
  def set_list2_tran_reset(self, list2_tran_reset=[]):
    self.list2_tran_reset = list2_tran_reset 

  def print_list2_tran_reset(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_tran_reset[i][j])
  
  def print_lut_tran_reset(self):
    for i in range(len(self.lut_tran_reset)):
      print(self.lut_tran_reset[i])

  def write_list2_tran_reset(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_tran_reset = []
    self.lut_tran_reset_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_tran_reset.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_tran_reset.append(outline)
    ## values
    self.lut_tran_reset.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_tran_reset[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_tran_reset[i][j]/targetLib.time_mag))
        outline += tmp_line+", "
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_tran_reset[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_tran_reset[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_tran_reset[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_tran_reset[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"
      self.lut_tran_reset.append(outline)
    self.lut_tran_reset.append(");")

    # store min/center/max for doc
    # min
    self.lut_tran_reset_mintomax.append(str("{:5f}".format(np.amin(self.list2_tran_reset)/targetLib.time_mag)))
    # center
    self.lut_tran_reset_mintomax.append(str("{:5f}".format(np.median(self.list2_tran_reset)/targetLib.time_mag)))
    # max
    self.lut_tran_reset_mintomax.append(str("{:5f}".format(np.amax(self.list2_tran_reset)/targetLib.time_mag)))
    
  ## propagation delay table for set
  def set_list2_prop_set(self, list2_prop_set=[]):
    self.list2_prop_set = list2_prop_set 

  def print_list2_prop_set(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_prop_set[i][j])
  
  def print_lut_prop_set(self):
    for i in range(len(self.lut_prop_set)):
      print(self.lut_prop_set[i])

  def write_list2_prop_set(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_prop_set = []
    self.lut_prop_set_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_prop_set.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_prop_set.append(outline)
    ## values
    self.lut_prop_set.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_prop_set[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_prop_set[i][j]/targetLib.time_mag))
        outline += tmp_line+", "
      ## do not add "," for last line
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_prop_set[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_prop_set[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_prop_set[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_prop_set[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"
      self.lut_prop_set.append(outline)
    self.lut_prop_set.append(");")

    # store min/center/max for doc
    # min
    self.lut_prop_set_mintomax.append(str("{:5f}".format(np.amin(self.list2_prop_set)/targetLib.time_mag)))
    # center
    self.lut_prop_set_mintomax.append(str("{:5f}".format(np.median(self.list2_prop_set)/targetLib.time_mag)))
    # max
    self.lut_prop_set_mintomax.append(str("{:5f}".format(np.amax(self.list2_prop_set)/targetLib.time_mag)))
    
  ## transient delay table for set
  def set_list2_tran_set(self, list2_tran_set=[]):
    self.list2_tran_set = list2_tran_set 

  def print_list2_tran_set(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_tran_set[i][j])
  
  def print_lut_tran_set(self):
    for i in range(len(self.lut_tran_set)):
      print(self.lut_tran_set[i])

  def write_list2_tran_set(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_tran_set = []
    self.lut_tran_set_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_tran_set.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_tran_set.append(outline)
    ## values
    self.lut_tran_set.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_tran_set[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_tran_set[i][j]/targetLib.time_mag))
        outline += tmp_line+", "
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_tran_set[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_tran_set[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_tran_set[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_tran_set[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"
      self.lut_tran_set.append(outline)
    self.lut_tran_set.append(");")
    
    # store min/center/max for doc
    # min
    self.lut_tran_set_mintomax.append(str("{:5f}".format(np.amin(self.list2_tran_set)/targetLib.time_mag)))
    # center
    self.lut_tran_set_mintomax.append(str("{:5f}".format(np.median(self.list2_tran_set)/targetLib.time_mag)))
    # max
    self.lut_tran_set_mintomax.append(str("{:5f}".format(np.amax(self.list2_tran_set)/targetLib.time_mag)))


  ## internal power (energy) table 
  def set_list2_eintl(self, list2_eintl=[]):
    self.list2_eintl = list2_eintl 

  def print_list2_eintl(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_eintl[i][j])
  
  def print_lut_eintl(self):
    for i in range(len(self.lut_eintl)):
      print(self.lut_eintl[i])

  def write_list2_eintl(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_eintl = []
    self.lut_eintl_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_eintl.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_eintl.append(outline)
    ## values
    self.lut_eintl.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_eintl[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_eintl[i][j]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+", "
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_eintl[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_eintl[i][len(jlist)-1]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_eintl[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_eintl[i][len(jlist)-1]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+"\" \\"
      self.lut_eintl.append(outline)
    self.lut_eintl.append(");")
    # store min/center/max for doc
    # min
    self.lut_eintl_mintomax.append(str("{:5f}".format(np.amin(self.list2_eintl)*targetLib.voltage_mag/targetLib.energy_mag)))
    # center
    self.lut_eintl_mintomax.append(str("{:5f}".format(np.median(self.list2_eintl)*targetLib.voltage_mag/targetLib.energy_mag)))
    # max
    self.lut_eintl_mintomax.append(str("{:5f}".format(np.amax(self.list2_eintl)*targetLib.voltage_mag/targetLib.energy_mag)))
    
  ## input energy 
  def set_list2_ein(self, list2_ein=[]):
    self.list2_ein = list2_ein 

  def print_list2_ein(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_ein[i][j])
  
  def print_lut_ein(self):
    for i in range(len(self.lut_ein)):
      print(self.lut_ein[i])

  def write_list2_ein(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_ein = []
    self.lut_ein_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_ein.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_ein.append(outline)
    ## values
    self.lut_ein.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_ein[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_ein[i][j]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+", "
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_ein[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_ein[i][len(jlist)-1]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_ein[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_ein[i][len(jlist)-1]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+"\", \\"
      self.lut_ein.append(outline)
    self.lut_ein.append(");")
    # store min/center/max for doc
    # min
    self.lut_ein_mintomax.append(str("{:5f}".format(np.amin(self.list2_ein)*targetLib.voltage_mag/targetLib.energy_mag)))
    # center
    self.lut_ein_mintomax.append(str("{:5f}".format(np.median(self.list2_ein)*targetLib.voltage_mag/targetLib.energy_mag)))
    # max
    self.lut_ein_mintomax.append(str("{:5f}".format(np.amax(self.list2_ein)*targetLib.voltage_mag/targetLib.energy_mag)))

  ## input capacitance 
  def set_list2_cin(self, list2_cin=[]):
    self.list2_cin = list2_cin 

  def print_list2_cin(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_cin[i][j])
  
  def print_lut_cin(self):
    for i in range(len(self.lut_cin)):
      print(self.lut_cin[i])

  def average_list2_cin(self, targetLib, ilist, jlist):
    ## output average of input capacitance
    ## (do not write table)
    self.lut_cin = 0;
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        self.lut_cin += self.list2_cin[i][j]
    #self.cin = str(self.lut_cin / (len(ilist) * len(jlist))/targetLib.capacitance_mag) ## use average
    self.cin = str(self.lut_cin / (len(ilist) * len(jlist))) ## use average
      
    #print("store cin:"+str(self.cin))

  ## clock input energy 
  def set_list2_eclk(self, list2_eclk=[]):
    self.list2_eclk = list2_eclk 

  def print_list2_eclk(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_eclk[i][j])
  
  def print_lut_eclk(self):
    for i in range(len(self.lut_eclk)):
      print(self.lut_eclk[i])

  def write_list2_eclk(self, targetLib, ilist, jlist):
    ## index_1
    outline = "index_1(\""
    self.lut_eclk = []
    self.lut_eclk_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_eclk.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_eclk.append(outline)
    ## values
    self.lut_eclk.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_eclk[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_eclk[i][j]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+", "
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_eclk[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_eclk[i][len(jlist)-1]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_eclk[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_eclk[i][len(jlist)-1]*targetLib.voltage_mag/targetLib.energy_mag))
        outline += tmp_line+"\", \\"
      self.lut_eclk.append(outline)
    self.lut_eclk.append(");")
    # store min/center/max for doc
    # min
    self.lut_eclk_mintomax.append(str("{:5f}".format(np.amin(self.list2_eclk)*targetLib.voltage_mag/targetLib.energy_mag)))
    # center
    self.lut_eclk_mintomax.append(str("{:5f}".format(np.median(self.list2_eclk)*targetLib.voltage_mag/targetLib.energy_mag)))
    # max
    self.lut_eclk_mintomax.append(str("{:5f}".format(np.amax(self.list2_eclk)*targetLib.voltage_mag/targetLib.energy_mag)))

  ## clock input capacitance 
  def set_list2_cclk(self, list2_cclk=[]):
    self.list2_cclk = list2_cclk 

  def print_list2_cclk(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_cclk[i][j])
  
  def print_lut_cclk(self):
    for i in range(len(self.lut_cclk)):
      print(self.lut_cclk[i])

  def average_list2_cclk(self, targetLib, ilist, jlist):
    ## output average of input capacitance
    ## (do not write table)
    self.lut_cclk = 0;
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        self.lut_cclk += self.list2_cclk[i][j]
    #self.cclk = str(self.lut_cclk / (len(ilist) * len(jlist))/targetLib.capacitance_mag) ## use average
    self.cclk = str(self.lut_cclk / (len(ilist) * len(jlist))) ## use average
    #print("store cclk:"+str(self.cclk))

  ## leak power
  def set_list2_pleak(self, list2_pleak=[]):
    self.list2_pleak = list2_pleak 

  def print_list2_pleak(self, ilist, jlist):
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        print(self.list2_pleak[i][j])
  
  def print_lut_pleak(self):
    for i in range(len(self.lut_pleak)):
      print(self.lut_pleak[i])

  def write_list2_pleak(self, targetLib, ilist, jlist):
    ## output average of leak power
    ## (do not write table)
    self.lut_pleak = 0;
    for i in range(len(ilist)):
      for j in range(len(jlist)):
        self.lut_pleak += self.list2_pleak[i][j]
    #self.pleak = str(self.lut_pleak / (len(ilist) * len(jlist))/targetLib.leakage_power_mag) # use average
    self.pleak = str("{:5f}".format(self.lut_pleak / (len(ilist) * len(jlist))/targetLib.leakage_power_mag)) # use average
  
  ## setup (for flop)
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
    ## index_1
    outline = "index_1(\""
    self.lut_setup = []
    self.lut_setup_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_setup.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_setup.append(outline)
    ## values
    self.lut_setup.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_setup[i][j])+", "
#        targetLib.print_msg(str(i)+" "+str(j))
#        targetLib.print_msg(self.list2_setup)
#        targetLib.print_msg(str("{:5f}".format(self.list2_setup[i][j]/targetLib.time_mag)))
        tmp_line = str("{:5f}".format(self.list2_setup[i][j]/targetLib.time_mag))
        outline += tmp_line+", "

      ## do not add "," for last line
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_setup[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_setup[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_setup[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_setup[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"

      self.lut_setup.append(outline)

    self.lut_setup.append(");")
    # store min/center/max for doc
    # min
    self.lut_setup_mintomax.append(str("{:5f}".format(np.amin(self.list2_setup)/targetLib.time_mag)))
    # center
    self.lut_setup_mintomax.append(str("{:5f}".format(np.median(self.list2_setup)/targetLib.time_mag)))
    # max
    self.lut_setup_mintomax.append(str("{:5f}".format(np.amax(self.list2_setup)/targetLib.time_mag)))

  ## hold (for flop)
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
    ## index_1
    outline = "index_1(\""
    self.lut_hold = []
    self.lut_hold_mintomax = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    #print(outline)
    self.lut_hold.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_hold.append(outline)
    ## values
    self.lut_hold.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_hold[i][j])+", "
        tmp_line = str("{:5f}".format(self.list2_hold[i][j]/targetLib.time_mag))
        outline += tmp_line+", "

      ## do not add "," for last line
      if(i == (len(ilist)-1)): 
        #outline += str(self.list2_hold[i][len(jlist)-1])+"\" \\"
        tmp_line = str("{:5f}".format(self.list2_hold[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\" \\"
      ##  add "," for else 
      else: 
        #outline += str(self.list2_hold[i][len(jlist)-1])+"\", \\"
        tmp_line = str("{:5f}".format(self.list2_hold[i][len(jlist)-1]/targetLib.time_mag))
        outline += tmp_line+"\", \\"

      self.lut_hold.append(outline)

    self.lut_hold.append(");")

    # store min/center/max for doc
    # min
    self.lut_hold_mintomax.append(str("{:5f}".format(np.amin(self.list2_hold)/targetLib.time_mag)))
    # center
    self.lut_hold_mintomax.append(str("{:5f}".format(np.median(self.list2_hold)/targetLib.time_mag)))
    # max
    self.lut_hold_mintomax.append(str("{:5f}".format(np.amax(self.list2_hold)/targetLib.time_mag)))
