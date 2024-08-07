import argparse, re, os, shutil, subprocess, inspect

from myFunc import my_exit

class MyLogicCell:
  def __init__ (self):
    self.cell = None    ## cell name
    self.area = None    ## set area 
    self.functions = [] ## cell function
    self.inports = []   ## inport pins
    self.cins = []      ## inport caps
    self.clock = None   ## clock pin for flop
    self.set = None     ## set pin for flop
    self.reset = None   ## reset pin for flop 
    self.cclks = []    ## clock pin cap. for flop
    self.csets = []    ## set pin cap. for flop
    self.crsts = []    ## reset pin cap. for flop 
    self.outports = []  ## outport pins
    self.flops = []     ## registers 
    self.functions = [] ## logic/flop functions 
    self.slope = []     ## inport slope
    self.cslope = 0     ## inport clock slope
    self.load = []      ## outport load
    self.simulation_timestep = 0      ## simulation timestep 
    self.isexport = 0   ## exported or not
    self.isexport2doc = 0 ## exported to doc or not
    self.isflop = 0     ## DFF or not
    ## setup 
    self.sim_setup_lowest = 0    ## fastest simulation edge (pos. val.) 
    self.sim_setup_highest = 0   ## lowest simulation edge (pos. val.) 
    self.sim_setup_timestep = 0  ## timestep for setup search (pos. val.) 
    ## hold                        
    self.sim_hold_lowest = 0     ## fastest simulation edge (pos. val.) 
    self.sim_hold_highest = 0    ## lowest simulation edge (pos. val.) 
    self.sim_hold_timestep = 0   ## timestep for hold search (pos. val.) 
    ## power
    self.pleak = []        ## cell leak power
    self.inport_pleak = [] ## inport leak power
    self.inport_cap = []   ## inport cap
    ## message
    self.supress_msg = None        ## supress message 

##                                                #
##-- add functions for both comb. and seq. cell --#   
##                                                #
  def add_cell(self, line="tmp"):
    tmp_array = line.split('-')
    ## expected format : add_cell -n(name) AND_X1 
    ##                            -l(logic) AND2 
    ##                             -i(inports) A B 
    ##                             -o(outports) YB
    ##                             -f(function) YB=A*B
    for options in tmp_array:

      ## add_cell command 
      if(re.match("^add_cell", options)):
        continue
      ## -n option
      elif(re.match("^n ", options)):
        tmp_array2 = options.split() 
        self.cell = tmp_array2[1] 
        #print (self.cell)
      ## -l option
      elif(re.match("^l ", options)):
        tmp_array2 = options.split() 
        self.logic = tmp_array2[1] 
        #print (self.logic)
      ## -i option
      elif(re.match("^i ", options)):
        tmp_array2 = options.split() 
        for w in tmp_array2:
          self.inports.append(w)
        self.inports.pop(0) # delete first object("-i")
        #print (self.inports)
      ## -o option
      ## -f option override -o option
      ## currently, -o is not used
      elif(re.match("^o ", options)):
        tmp_array2 = options.split() 
        #for w in tmp_array2:
        # self.outports.append(w)
        #self.outports.pop(0) # delete first object("-o")
        #print (self.outports)
      ## -f option
      elif(re.match("^f ", options)):
        tmp_array2 = options.split() 
        #print (tmp_array2)
        tmp_array2.pop(0) # delete first object("-f")
        for w in tmp_array2:
          tmp_array3 = w.split('=') 
          self.outports.append(tmp_array3[0])
          self.functions.append(tmp_array3[1])
#       print ("func:"+str(self.functions))
#       print ("outp:"+str(self.outports))
#       print (self.functions)
#       print (self.outports)
      ## undefined option 
      else:
        print("ERROR: undefined option:"+options) 
        my_exit()
    # do not use print_msg 
    print ("finish add_cell")

  def set_supress_message(self, targetLib):
    self.supress_msg = targetLib.supress_msg 

  def print_msg(self, message=""):
    if((self.supress_msg.lower() == "false")or(self.supress_msg.lower() == "f")):
      print(message)

  # self.slope is 2D array
  # [[1, 2, 3, "slope1"],[2, 3, 4, "slope2"]]
  def add_slope(self, line="tmp"):
    line = re.sub('\{','',line)
    line = re.sub('\}','',line)
    line = re.sub('^add_slope ','',line)
    tmp_array = line.split()
    tmp_name = tmp_array.pop(0) # pop out slope name
    tmp_slope = [] 
    for w in tmp_array:
      #self.slope.append(float(w))
      tmp_slope.append(float(w))
    tmp_slope.append(tmp_name)
    self.slope.append(tmp_slope)
    #print (self.slope)

  # self.load is 2D array
  # [[1, 2, 3, "load1"],[2, 3, 4, "load2"]]
  def add_load(self, line="tmp"):
    line = re.sub('\{','',line)
    line = re.sub('\}','',line)
    line = re.sub('^add_load ','',line)
    tmp_array = line.split()
    tmp_name = tmp_array.pop(0) # pop out load name
    tmp_load = [] 
    for w in tmp_array:
      #self.load.append(float(w))
      tmp_load.append(float(w))
    tmp_load.append(tmp_name)
    self.load.append(tmp_load)
    #print (self.load)

  def return_slope(self, line="slope_name"):
    flag_match = 0
    jlist = []
    # search slope name from 2D slope array
    for jlist in self.slope:
        if (jlist[-1] != line):
          continue
        else:
          flag_match = 1
          break
    if (flag_match == 0): # exit loop w/o match
      print("cannot find slope:"+str(line))
      my_exit()
    jlist.pop(-1) # delete slope name
    outline = "(\""
    self.lut_prop = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    return outline

  def return_load(self):
    jlist = self.load
    flag_match = 0
    jlist = []
    # search load name from 2D load array
    for jlist in self.load:
        if (jlist[-1] != line):
          continue
        else:
          flag_match = 1
          break
    if (flag_match == 0): # exit loop w/o match
      print("cannot find load:"+str(line))
      my_exit()
    jlist.pop(-1) # delete load name
    outline = "(\""
    self.lut_prop = []
    for j in range(len(jlist)-1):
      outline += str(jlist[j])+", " 
    outline += str(jlist[len(jlist)-1])+"\");" 
    return outline

  def add_area(self, line="tmp"):
    tmp_array = line.split()
    self.area = float(tmp_array[1]) 

  def add_netlist(self, line="tmp"):
    tmp_array = line.split()
    self.netlist = tmp_array[1]
    self.definition = None 
    self.instance = None 
    lines = open(self.netlist, "r")
    ## search cell name in the netlist
    for line in lines:
      #print("self.cell.lower:"+str(self.cell.lower()))
      #print("line.lower:"+str(line.lower()))
      if((self.cell.lower() in line.lower()) and (".subckt" in line.lower())):
        print("Cell definition found!")
        #print(line)
        self.definition = line
        ## generate circuit call
        line = re.sub('\$.*$','',line)
        tmp_array2 = line.split()
        #print (tmp_array2)
        tmp_array2.pop(0) ## delete .subckt
        #print (tmp_array2)
        tmp_str = tmp_array2.pop(0)
        #print (tmp_array2)
        tmp_array2.append(tmp_str) ## move circuit name to last
        #print (tmp_array2)
        tmp_array2.insert(0,"XDUT") ## insert instance name 
        #print (tmp_array2)
        self.instance = ' '.join(tmp_array2) ## convert array into string
        
        
    ## if cell name is not found, show error
    if(self.definition == None):
      print("Cell definition not found. Please use add_cell command to add your cell")
      my_exit()

  def add_model(self, line="tmp"):
    tmp_array = line.split()
    self.model = tmp_array[1] 

  def add_simulation_timestep(self, line="tmp"):
    tmp_array = line.split()
    ## if auto, use 1/10 of min slope
    if (tmp_array[1] == 'auto'):
      #self.simulation_timestep = float(self.slope[0])/10 
      self.simulation_timestep = self.search_min_slope(line) / 10 
      self.print_msg ("auto set simulation timestep: "+str(self.simulation_timestep))
    else:
      self.simulation_timestep = float(tmp_array[1])

  def set_exported(self):
    self.isexport = 1 

  def set_exported2doc(self):
    self.isexport2doc = 1
        
  def set_inport_cap_pleak(self, index, harness):
    ## average leak power of all harness
    self.pleak += harness.pleak 

##                                 #
##-- add functions for seq. cell --#    
##                                 #
  def add_flop(self, line="tmp"):
    tmp_array = line.split('-')
    ## expected format : add_floop -n(name) DFFRS_X1 /
    ##                             -l(logic)    DFFARAS : DFF w async RST and async SET
    ##                              -i(inports)  DATA 
    ##                              -c(clock)    CLK 
    ##                              -s(set)      SET   (if used) 
    ##                              -r(reset)    RESET (if used)
    ##                              -o(outports) Q QN
    ##                              -q(flops)    IQ IQN
    ##                              -f(function) Q=IQ QN=IQN
    self.isflop = 1  ## set as flop
    for options in tmp_array:

      ## add_flop command 
      if(re.match("^add_flop", options)):
        continue
      ## -n option (subckt name)
      elif(re.match("^n ", options)):
        tmp_array2 = options.split() 
        self.cell = tmp_array2[1] 
        #print (self.cell)
      ## -l option (logic type)
      elif(re.match("^l ", options)):
        tmp_array2 = options.split() 
        self.logic = tmp_array2[1] 
        #print (self.logic)
      ## -i option (input name)
      elif(re.match("^i ", options)):
        tmp_array2 = options.split() 
        for w in tmp_array2:
          self.inports.append(w)
        self.inports.pop(0) # delete first object("-i")
        #print (self.inports)
      ## -c option (clock name)
      elif(re.match("^c ", options)):
        tmp_array2 = options.split() 
        self.clock = tmp_array2[1] 
        #print (self.clock)
      ## -s option (set name)
      elif(re.match("^s ", options)):
        tmp_array2 = options.split() 
        self.set = tmp_array2[1] 
        #print (self.set)
      ## -r option (reset name)
      elif(re.match("^r ", options)):
        tmp_array2 = options.split() 
        self.reset = tmp_array2[1] 
        print (self.reset)
      ## -o option (output name)
      elif(re.match("^o ", options)):
        tmp_array2 = options.split() 
        for w in tmp_array2:
          self.outports.append(w)
        self.outports.pop(0) ## delete first object("-o")
        #print (self.outports)
      ## -q option (storage name)
      elif(re.match("^q ", options)):
        tmp_array2 = options.split() 
        for w in tmp_array2:
          self.flops.append(w)
        self.flops.pop(0) ## delete first object("-q")
        #print (self.flops)
      ## -f option (function name)
      elif(re.match("^f ", options)):
        tmp_array2 = options.split() 
        #print (tmp_array2)
        tmp_array2.pop(0) ## delete first object("-f")
        for w in tmp_array2:
          tmp_array3 = w.split('=') 
          for o in self.outports:
            if(o == tmp_array3[0]):
              self.functions.append(tmp_array3[1])
        #print (self.functions)
      ## undefined option 
      else:
        print("ERROR: undefined option:"+options+"\n")  
        my_exit() 
    # do not use print_msg 
    print ("finish add_flop")

  def search_min_slope(self, line="tmp"):
    tmp_array = line.split()
    flag_match = 0
    jlist = []
    # search slope name from 2D slope array
    for jlist in self.slope:
        if (jlist[-1] != tmp_array[2]):
          continue
        else:
          flag_match = 1
          break
    if (flag_match == 0): # exit loop w/o match
      print("cannot find slope:"+str(line))
      my_exit()
    return float(jlist[0]) 
    
  def search_max_slope(self, line="tmp"):
    tmp_array = line.split()
    flag_match = 0
    jlist = []
    # search slope name from 2D slope array
    for jlist in self.slope:
        if (jlist[-1] != tmp_array[2]):
          continue
        else:
          flag_match = 1
          break
    if (flag_match == 0): # exit loop w/o match
      print("cannot find slope:"+str(line))
      my_exit()
    return float(jlist[-2]) 
    

  def add_clock_slope(self, line="tmp"):
    tmp_array = line.split()
    ## if auto, and slope is defined, use mininum slope
    if (tmp_array[1] == 'auto'):
      self.cslope = self.search_min_slope(line)
      self.print_msg ("auto set clock slope "+str(self.cslope)+" from slope "+str(tmp_array[2])+" of mininum slope.")
 
    else:
      self.cslope = float(tmp_array[1]) 

  ## this defines lowest limit of setup edge
  def add_simulation_setup_lowest(self, line="tmp"):
    tmp_array = line.split()
    ## if auto, use 10x of max slope 
    ## "10" should be the same value of tstart1 and tclk5 in spice 
    if (tmp_array[1] == 'auto'):
      self.sim_setup_lowest = self.search_max_slope(line) * -10 
      self.print_msg ("auto set setup simulation time lowest limit: "+str(self.sim_setup_lowest))
    else:
      self.sim_setup_lowest = float(tmp_array[1]) 
      
  ## this defines highest limit of setup edge
  def add_simulation_setup_highest(self, line="tmp"):
    tmp_array = line.split()
    ## if auto, use 10x of max slope 
    if (tmp_array[1] == 'auto'):
      self.sim_setup_lowest = self.search_max_slope(line) * 10 
      self.print_msg ("auto set setup simulation time highest limit: "+str(self.sim_setup_highest))
    else:
      self.sim_setup_highest = float(tmp_array[1])
      
  def add_simulation_setup_timestep(self, line="tmp"):
    tmp_array = line.split()
    ## if auto, use 1/10x min slope
    if (tmp_array[1] == 'auto'):
      self.sim_setup_timestep = self.search_min_slope(line) / 10 
      self.print_msg ("auto set setup simulation timestep: "+str(self.sim_setup_highest))
    else:
      self.sim_setup_timestep = float(tmp_array[1])
      
  ## this defines lowest limit of hold edge
  def add_simulation_hold_lowest(self, line="tmp"):
    tmp_array = line.split()
    ## if auto, use very small val. 
    #remove# if hold is less than zero, pwl time point does not be incremental
    #remove# and simulation failed
    if (tmp_array[1] == 'auto'):
      #self.sim_hold_lowest = float(self.slope[-1]) * -5 
      #self.sim_hold_lowest = float(self.slope[-1]) * -10 
      #self.sim_hold_lowest = float(self.slope[-1]) * 0.001 
      self.sim_hold_lowest = self.search_min_slope(line) * -10 
      self.print_msg ("auto set hold simulation time lowest limit: "+str(self.sim_hold_lowest))
    else:
      self.sim_hold_lowest = float(tmp_array[1])
      
  ## this defines highest limit of hold edge
  def add_simulation_hold_highest(self, line="tmp"):
    tmp_array = line.split()
    ## if auto,  use 5x of max slope 
    ## value should be smaller than "tmp_max_val_loop" in holdSearchFlop
    if (tmp_array[1] == 'auto'):
      #self.sim_hold_highest = float(self.slope[-1]) * 5 
      #self.sim_hold_highest = float(self.slope[-1]) * 10 
      self.sim_hold_highest = self.search_max_slope(line) * 10 
      self.print_msg ("auto set hold simulation time highest limit: "+str(self.sim_hold_highest))
    else:
      self.sim_hold_highest = float(tmp_array[1])
      
  def add_simulation_hold_timestep(self, line="tmp"):
    tmp_array = line.split()
    ## if auto,  use 1/10x min slope
    if (tmp_array[1] == 'auto'):
      #self.sim_hold_timestep = float(self.slope[0])/10 
      self.sim_hold_timestep = self.search_min_slope(line) / 10 
      self.print_msg ("auto set hold simulation timestep: "+str(self.sim_hold_timestep))
    else:
      self.sim_hold_timestep = float(tmp_array[1])

  ## calculate ave of cin for each inports
  ## cin is measured two times and stored into 
  ## neighborhood harness, so cin of (2n)th and 
  ## (2n+1)th harness are averaged out
  def set_cin_avg(self, targetLib, harnessList, port="data"):
    tmp_cin = 0;
    tmp_index = 0;
    for targetHarness in harnessList:
      if((port.lower() == 'clock')or(port.lower() == 'clk')):
        tmp_cin += float(targetHarness.cclk)
        ## if this is (2n+1) then store averaged 
        ## cin into targetCell.cins
        if((tmp_index % 2) == 1):
          #self.cclks.append(str((tmp_cin / 2)/targetLib.capacitance_mag))
          self.cclks.append(str("{:5f}".format((tmp_cin / 2)/targetLib.capacitance_mag)))
          tmp_cin = 0
        tmp_index += 1
        self.print_msg("stored cins:"+str(tmp_index)+" for clk")
      elif((port.lower() == 'reset')or(port.lower() == 'rst')):
        tmp_cin += float(targetHarness.cin) # .cin stores rst cap. 
        ## if this is (2n+1) then store averaged 
        ## cin into targetCell.cins
        if((tmp_index % 2) == 1):
          #self.crsts.append(str((tmp_cin / 2)/targetLib.capacitance_mag))
          self.crsts.append(str("{:5f}".format((tmp_cin / 2)/targetLib.capacitance_mag)))
          tmp_cin = 0
        tmp_index += 1
        self.print_msg("stored cins:"+str(tmp_index)+" for rst")
      elif(port.lower() == 'set'):
        tmp_cin += float(targetHarness.cin) # .cin stores set cap.
        ## if this is (2n+1) then store averaged 
        ## cin into targetCell.cins
        if((tmp_index % 2) == 1):
          #self.csets.append(str((tmp_cin / 2)/targetLib.capacitance_mag))
          self.csets.append(str("{:5f}".format((tmp_cin / 2)/targetLib.capacitance_mag)))
          tmp_cin = 0
        tmp_index += 1
        self.print_msg("stored cins:"+str(tmp_index)+" for set")
      else: 
        tmp_cin += float(targetHarness.cin) # else, .cin stores inport cap.
        ## if this is (2n+1) then store averaged 
        ## cin into targetCell.cins
        if((tmp_index % 2) == 1):
          #self.cins.append(str((tmp_cin / 2)/targetLib.capacitance_mag))
          self.cins.append(str("{:5f}".format((tmp_cin / 2)/targetLib.capacitance_mag)))
          tmp_cin = 0
        tmp_index += 1
        self.print_msg("stored cins:"+str(tmp_index)+" for data")
      self.print_msg("stored cins:"+str(tmp_index))

