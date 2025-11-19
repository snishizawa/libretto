import argparse, re, os, shutil, subprocess
import numpy as np
from myFunc import my_exit

class MyConditionsAndResults:
  def __init__ (self):
    self.instance = None              ## instance name
    self.target_inport = None         ## target inport name
    self.target_outport = None        ## target outport name
    self.stable_inport = []           ## stable imports
    self.stable_inport_val = []       ## stable imports val
    self.nontarget_outport = []       ## nontarget outport
    self.target_clock     = None      ## target clock name
    self.target_clock_val = None      ## target clock value
    self.target_reset     = None      ## target reset name
    self.target_reset_val = None      ## target reset val
    self.target_set     = None        ## target set name
    self.target_set_val = None        ## target set val
    self.target_load = None           ## target output load capacitance 
    self.target_slope = None          ## target input slope
    self.target_tsetup = None         ## target test setup time (for seq cell)
    self.target_thold = None          ## target test hold time (for seq cell)
    self.tsimendmag = None            ## simulation end time magnitude 
    self.tranmag = None               ## simulation transient time magnitude
    self.timestep_mag = None          ## simulation timestep  magnitude 
    self.target_estart = None         ## target energy meas. clock start 
    self.target_eend = None           ## target energy meas. clock end 
    self.target_eclkstart = None      ## target energy meas. start 
    self.target_eclkend = None        ## target energy meas. end 
    self.iternum = None               ## simulation iteration num for seq. cell 
    self.spicef = None                ## spice file (part)
    self.spicefo = None               ## spice file (full)
    self.is_delay_energy = "None"     ## "delay or energy" 
    self.mode = "None"                ## "setup" "hold" "recov" "remov" 
    self.pwlmode = "None"             ## set pwlmode for DATA/CLK/RST/SET. default is "default"

  def set_target_load(self, load = None):
    self.target_load = load 

  def set_target_slope(self, slope = None):
    self.target_slope = slope 

  def set_target_tsetup(self, tsetup = None):
    self.target_tsetup = tsetup 

  def set_target_thold(self, thold = None):
    self.target_thold = thold 

  def set_tsimendmag(self, tsimendmag = None):
    self.tsimendmag = tsimendmag 
 
  def set_tranmag(self, tranmag = None):
    self.tranmag = tranmag 

  def set_timestep_mag(self, timestep_mag = None):
    self.timestep_mag = timestep_mag 

  def set_target_estart(self, estart = None):
    self.target_estart = estart 

  def set_target_eend(self, eend = None):
    self.target_eend = eend 

  def set_target_eclkstart(self, eclkstart = None):
    self.target_eclkstart = eclkstart 

  def set_target_eclkend(self, eclkend = None):
    self.target_eclkend = eclkend 

  def set_slope_mag(self, targetLib):
    self.slope_mag = 1 
    # self.slope_mag = 1 / (targetLib.logic_threshold_high - targetLib.logic_threshold_low)
 
  def get_spice_lines_common(self, targetLib, targetCell):
    outlines = []
    outlines.append(".param load ="+str(self.target_load)+str(targetLib.capacitance_unit)+"\n")
    outlines.append(".param slope ="+str(self.target_slope * self.slope_mag)+str(targetLib.time_unit)+"\n")
    outlines.append(".temp "+str(targetLib.temperature)+"\n" )
    return outlines
  
  def get_spice_lines_comb(self, targetLib, targetCell):
    outlines = []
    outlines.append(".param tunit ="+str(targetCell.slope[-1])+str(targetLib.time_unit)+"\n" )
    outlines.append(".param _tsimend ='20 * tunit\n" )
    outlines.append(".tran "+str(targetCell.simulation_timestep)+str(targetLib.time_unit)+" '_tsimend'\n")
    return outlines
  
  def get_spice_lines_comb_energy(self, targetLib, targetCell):
    outlines = []
    outlines.append(".param ENERGY_START = "+str(self.target_estart)+"\n")
    outlines.append(".param ENERGY_END = "+str(self.target_eend)+"\n")
    return outlines
  
  def get_spice_lines_seq(self, targetLib, targetCell):
    outlines = []
    outlines.append(".param tsimendmag ="+str(self.tsimendmag)+" tranmag ="+str(self.tranmag)+"\n")
    outlines.append(".param cslope ="+str(targetCell.cslope)+str(targetLib.time_unit)+"\n" )
    outlines.append(".param tsetup ="+str(self.target_tsetup)+str(targetLib.time_unit)+"\n" )
    outlines.append(".param thold ="+str(self.target_thold)+str(targetLib.time_unit)+"\n" )
    outlines.append(".tran "+str(targetCell.simulation_timestep * self.timestep_mag)+str(targetLib.time_unit)+" '_tsimend'\n")
    return outlines

  def get_spice_lines_seq_energy(self, targetLib, targetCell):
    outlines = []
    outlines.append(".param ENERGY_START = "+str(self.target_estart)+"\n")
    outlines.append(".param ENERGY_END = "+str(self.target_eend)+"\n")
    outlines.append(".param ENERGY_CLK_START = "+str(self.target_eclkstart)+"\n")
    outlines.append(".param ENERGY_CLK_END = "+str(self.target_eclkend)+"\n")
    return outlines
  
  def check_time_order(self, tmp_min_time=0.00001, str_fwd="0", str_adv="0", val_fwd=0, val_adv=0):
    if(val_adv > val_fwd):
      print("Warning!! Order "+str(str_adv)+" ("+str(f'{val_adv:.4f}')+") -> "+str(str_fwd)+" ("+str(f'{val_fwd:.4f}')+") is not correct!")
      #print("spice file: "+str(self.spicefo))
      #val_fwd = val_adv + tmp_min_time 
      return -1
    
    return 0

  def round_down_pwltime(self, targetCell, pwltime):
    return (int(pwltime/targetCell.simulation_timestep)) * targetCell.simulation_timestep

  def get_spice_lines_pwltime(self, targetLib, targetCell, pwlmode="default"):
    tmp_min_time = targetCell.simulation_timestep
    tmp_tunit = targetCell.slope[-1]  
    tmp_cslope = targetCell.cslope
    tmp_slope = self.target_slope   
    tmp_tsetup = self.target_tsetup 
    tmp_thold = self.target_thold   
    error_sum = 0

    ## define time for pwl
    if(pwlmode == "default"):
      tmp_tclk1 =  tmp_slope                                 # ^ first clock
      tmp_tclk2 =  tmp_tclk1 + tmp_cslope                    # | 
      tmp_tclk3 =  tmp_tclk2 + tmp_tunit                     # | 
      tmp_tclk4 =  tmp_tclk3 + tmp_cslope                    # v ^ Recovery 
      tmp_tclk5 =  tmp_tclk4 + tmp_tunit                     #   V Removal    
      tmp_tstart1 = tmp_tclk5 + tmp_tunit * 10 + tmp_tsetup  # ^ data input start (variable) 
      tmp_tstart2 = tmp_tstart1 + tmp_slope                  # v varied w/ dedge
      tmp_tend1 =  tmp_tstart2 + tmp_thold                   # ^ data input end (variable)
      tmp_tend2 =  tmp_tend1 + tmp_slope                     # v varied w/ dedge
      tmp_tclk6 =  tmp_tclk4 + tmp_tunit * 10                # ^ second clock
      tmp_tclk7 =  tmp_tclk6 + tmp_cslope                    # v 
      tmp_tsimend = tmp_tend2 + tmp_tunit * 50 * self.tsimendmag
    elif(pwlmode == "LR_mode1"):
      print("this pwlmode is not supported")
                        ##-- LR mode1
      #outlines.append(".param _tclk1 = 100n \n")                # ^ first clock
      #outlines.append(".param _tclk2 = '_tclk1 + cslope '\n")    # | 
      #outlines.append(".param _tclk3 = '_tclk2 + 100n '\n")    # | 
      #outlines.append(".param _tclk4 = '_tclk3 + cslope '\n")    # v ^ Recovery 
      #outlines.append(".param _tclk5 = '_tclk4 + tunit '\n")    #   V Removal    
      #outlines.append(".param _tstart1 = '_tclk6 + 0.5*cslope - 0.5*slope + tsetup'\n")    # ^ data input start 
      #outlines.append(".param _tstart2 = '_tstart1 + slope'\n")                 # v varied w/ dedge
      #outlines.append(".param _tend1 = '_tstart2 + thold'\n")   # ^ data input end
      #outlines.append(".param _tend2 = '_tend1 + slope'\n")      # v varied w/ dedge
      #outlines.append(".param _tclk6 = '_tclk4 + tunit * 10'\n")       # ^ second clock
      #outlines.append(".param _tclk7 = '_tclk6 + cslope '\n")           # v 
      #outlines.append(".param _tsimend = '_tend2 + 200n' \n")

    elif(pwlmode == "LR_mode2"):
      print("this pwlmode is not supported")
      #                  #-- LR mode2
      #outlines.append(".param _tclk1 = 50n \n")                # ^ first clock
      #outlines.append(".param _tclk2 = '_tclk1 + cslope '\n")    # | 
      #outlines.append(".param _tclk3 = '_tclk2 + 50n '\n")    # | 
      #outlines.append(".param _tclk4 = '_tclk3 + cslope '\n")    # v ^ Recovery 
      #outlines.append(".param _tclk5 = '_tclk4 + 50n '\n")    #   V Removal    
      #outlines.append(".param _tstart1 = '_tclk6 + 0.5*cslope - 0.5*slope + tsetup'\n")    # ^ data input start 
      #outlines.append(".param _tstart2 = '_tstart1 + slope'\n")                 # v varied w/ dedge
      #outlines.append(".param _tend1 = '_tclk6 + 0.5*cslope - 0.5*slope + thold'\n")   # ^ data input end
      #outlines.append(".param _tend2 = '_tend1 + slope'\n")      # v varied w/ dedge
      #outlines.append(".param _tclk6 = '_tclk5 + tunit * 10'\n")       # ^ second clock
      #outlines.append(".param _tclk7 = '_tclk6 + cslope '\n")           # v 
      #outlines.append(".param _tsimend = '_tclk7 + 50n' \n")

    elif(pwlmode == "LR_mode3"):
      print("this pwlmode is not supported")

                        #-- LR mode3
#      outlines.append(".param _tclk1 = 50n \n")                # ^ first clock
#      outlines.append(".param _tclk2 = '_tclk1 + cslope '\n")    # | 
#      outlines.append(".param _tclk3 = '_tclk2 + 50n '\n")    # | 
#      outlines.append(".param _tclk4 = '_tclk3 + cslope '\n")    # v ^ Recovery 
#      outlines.append(".param _tclk5 = '_tclk4 + 50n '\n")    #   V Removal    
#      outlines.append(".param _tstart1 = '_tclk6 + 0.5*cslope - 0.5*slope + tsetup'\n")    # ^ data input start 
#      outlines.append(".param _tstart2 = '_tstart1 + slope'\n")                 # v varied w/ dedge
#      outlines.append(".param _tend1 = '_tclk6 + 0.5*cslope - 0.5*slope + thold'\n")   # ^ data input end
#      outlines.append(".param _tend2 = '_tend1 + slope'\n")      # v varied w/ dedge
#      outlines.append(".param _tclk6 = '_tclk5 + _tclk6_wait'\n")       # ^ second clock
#      outlines.append(".param _tclk7 = '_tclk6 + cslope '\n")           # v 
#      outlines.append(".param _tsimend = '_tclk7 + 50n' \n")
    else:
      my_exit("Non-registered pwlmode:"+str(pwlmode)+"\n")

    ## check time order
    ## DATA 
    if((self.target_inport_val == "01") or (self.target_inport_val == "10")):
      error_sum += self.check_time_order (tmp_min_time, "tmp_tstart2", "tmp_tstart1"   , tmp_tstart2, tmp_tstart1)
      
      ## activate this check only for setup or recovery simulation 
      ## hold (and removal) simulation try to find simulation failure -> let simulation fail 
      if((self.mode == "setup") or (self.mode == "recov")):
        error_sum +=   self.check_time_order (tmp_min_time, "tmp_tend1",   "tmp_tstart2"   , tmp_tend1, tmp_tstart2)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tend2",   "tmp_tend1"     , tmp_tend2, tmp_tend1)
      error_sum += self.check_time_order (tmp_min_time, "tmp_tsimend", "tmp_tend2"     , tmp_tsimend, tmp_tend2)

      error_sum += self.check_time_order (tmp_min_time, "tmp_tstart1", "tmp_tclk4"     , tmp_tstart1, tmp_tclk4)
      error_sum += self.check_time_order (tmp_min_time, "tmp_tend1", "tmp_tstart2"     , tmp_tend1, tmp_tstart2)
    ## CLOCK                                           
    if((self.target_clock_val == "0101") or (self.target_clock_val == "0101")):
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tclk2",   "tmp_tclk1"     , tmp_tclk2, tmp_tclk1)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tclk3",   "tmp_tclk2"     , tmp_tclk3, tmp_tclk2)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tclk4",   "tmp_tclk3"     , tmp_tclk4, tmp_tclk3)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tclk6",   "tmp_tclk4"     , tmp_tclk6, tmp_tclk4)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tclk7",   "tmp_tclk6"     , tmp_tclk7, tmp_tclk6)
    if((self.target_clock_val == "010") or (self.target_clock_val == "101")):
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tclk2",   "tmp_tclk1"     , tmp_tclk2, tmp_tclk1)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tclk3",   "tmp_tclk2"     , tmp_tclk3, tmp_tclk2)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tclk4",   "tmp_tclk3"     , tmp_tclk4, tmp_tclk3)
    ## RST                                             
    if((self.target_reset_val == "01") or (self.target_reset_val == "10")):
      error_sum += self.check_time_order (tmp_min_time, "tmp_tstart2", "tmp_tstart1"   , tmp_tstart2, tmp_tstart1)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tend1",   "tmp_tstart2"   , tmp_tend1, tmp_tstart2)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tend2",   "tmp_tend1"     , tmp_tend2, tmp_tend1)
    ## SET                                             
    if((self.target_set_val == "01") or (self.target_set_val == "10")):
      error_sum += self.check_time_order (tmp_min_time, "tmp_tstart2", "tmp_tstart1"   , tmp_tstart2, tmp_tstart1)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tend1",   "tmp_tstart2"   , tmp_tend1, tmp_tstart2)
      error_sum +=   self.check_time_order (tmp_min_time, "tmp_tend2",   "tmp_tend1"     , tmp_tend2, tmp_tend1)

    ## round-down pwltime to prevent "min-time-step" error in ngspice
    tmp_tclk1 =  self.round_down_pwltime(targetCell, tmp_tclk1) 
    tmp_tclk2 =  self.round_down_pwltime(targetCell, tmp_tclk2) 
    tmp_tclk3 =  self.round_down_pwltime(targetCell, tmp_tclk3) 
    tmp_tclk4 =  self.round_down_pwltime(targetCell, tmp_tclk4) 
    tmp_tclk5 =  self.round_down_pwltime(targetCell, tmp_tclk5) 
    tmp_tstart1 =self.round_down_pwltime(targetCell, tmp_tstart1) 
    tmp_tstart2 =self.round_down_pwltime(targetCell, tmp_tstart2)
    tmp_tend1 =  self.round_down_pwltime(targetCell, tmp_tend1) 
    tmp_tend2 =  self.round_down_pwltime(targetCell, tmp_tend2) 
    tmp_tclk6 =  self.round_down_pwltime(targetCell, tmp_tclk6) 
    tmp_tclk7 =  self.round_down_pwltime(targetCell, tmp_tclk7) 
    tmp_tsimend =self.round_down_pwltime(targetCell, tmp_tsimend)

    # abort simulation if time order is not as expected
    if(error_sum < 0):
      tmp_tsimend = 0

    ## generate spice lines
    outlines = []
    outlines.append(".param _tclk1 =   "+str(f'{tmp_tclk1:.3f}')+str(targetLib.time_unit)+" \n")                         
    outlines.append(".param _tclk2 =   "+str(f'{tmp_tclk2:.3f}')+str(targetLib.time_unit)+" \n")                         
    outlines.append(".param _tclk3 =   "+str(f'{tmp_tclk3:.3f}')+str(targetLib.time_unit)+" \n")                         
    outlines.append(".param _tclk4 =   "+str(f'{tmp_tclk4:.3f}')+str(targetLib.time_unit)+" \n")                         
    outlines.append(".param _tclk5 =   "+str(f'{tmp_tclk5:.3f}')+str(targetLib.time_unit)+" \n")                         
    outlines.append(".param _tstart1 = "+str(f'{tmp_tstart1:.3f}')+str(targetLib.time_unit)+" \n")                    
    outlines.append(".param _tstart2 = "+str(f'{tmp_tstart2:.3f}')+str(targetLib.time_unit)+" \n")                    
    outlines.append(".param _tend1 =   "+str(f'{tmp_tend1:.3f}')+str(targetLib.time_unit)+" \n")                        
    outlines.append(".param _tend2 =   "+str(f'{tmp_tend2:.3f}')+str(targetLib.time_unit)+" \n")                        
    outlines.append(".param _tclk6 =   "+str(f'{tmp_tclk6:.3f}')+str(targetLib.time_unit)+" \n")                        
    outlines.append(".param _tclk7 =   "+str(f'{tmp_tclk7:.3f}')+str(targetLib.time_unit)+" \n")                        
    outlines.append(".param _tsimend = "+str(f'{tmp_tsimend:.3f}')+str(targetLib.time_unit)+" \n")                    
    return outlines
  
  def set_spicef(self, spicef = "not_set"):
    self.spicef = spicef
 
  def set_iternum(self, iternum = None):
    self.iternum = iternum

  def set_delay_energy(self, is_delay_energy = "None"):
    if(is_delay_energy == "delay"):
      self.is_delay_energy = "delay" 
    elif(is_delay_energy == "energy"):
      self.is_delay_energy = "energy"
    else:
      my_exit("is_delay_energy is not ether delay nor ennergy:"+str(is_delay_energy)) 

  def set_sim_mode_seq(self, mode = "None"):
    if(mode == "setup"):
      self.mode = "setup" 
    elif(mode == "hold"):
      self.mode = "hold"
    elif(mode == "recovery"):
      self.mode = "recov"
    elif(mode == "removal"):
      self.mode = "remov"
    else:
      my_exit("mode is not ether  nor ennergy:"+str(mode)) 

  def get_spicefo_seq(self):
    if(self.is_delay_energy == "delay"):
      self.spicefo = str(self.spicef)+"_j"+str(self.iternum)+"_"+str(self.target_load)+"_"+str(self.target_slope)+"_setup"+str(f'{self.target_tsetup:,.4f}')+"_hold"+str(f'{self.target_thold:,.4f}')+"_d.sp"
    elif(self.is_delay_energy == "energy"):
      self.spicefo = str(self.spicef)+"_j"+str(self.iternum)+"_"+str(self.target_load)+"_"+str(self.target_slope)+"_setup"+str(f'{self.target_tsetup:,.4f}')+"_hold"+str(f'{self.target_thold:,.4f}')+"_e.sp"
    else:
      print("self.is_delay_energy is not matched with delay/energy: "+str(self.is_delay_energy))
    return self.spicefo

#  def get_spicefo_seq_energy(self, stage=None):
#    self.spicefo = str(self.spicef)+"_j"+str(self.iternum)+"_"+str(self.target_load)+"_"+str(self.target_slope)+"_setup"+str(f'{self.target_tsetup:,.4f}')+"_hold"+str(f'{self.target_thold:,.4f}')+"_e.sp"
#    return self.spicefo

  def get_spicefo_comb(self, stage=None):
    self.spicefo =  str(self.spicef)+"_"+str(self.target_load)+"_"+str(self.target_slope)+"_d.sp"
    return self.spicefo

  def get_spicefo_comb_energy(self, stage=None):
    self.spicefo = str(self.spicef)+"_"+str(self.target_load)+"_"+str(self.target_slope)+"_e.sp"
    return self.spicefo

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

  def set_target_outport(self, outport="tmp", function="tmp", val="01"):
    self.target_outport = outport
    self.target_function = function
    self.target_outport_val = val

  def set_stable_inport(self, inport="tmp", val="1"):
    self.stable_inport.append(inport)
    self.stable_inport_val.append(val)

  def set_nontarget_outport(self, outport="tmp"):
    self.stable_nontarget.append(outport)

  def set_target_clock(self, inport="tmp", val="01"):
    self.target_clock = inport
    self.target_clock_val = val

  def set_target_reset(self, inport="tmp", val="01"):
    self.target_reset = inport
    self.target_reset_val = val

  def set_target_set(self, inport="tmp", val="01"):
    self.target_set = inport
    self.target_set_val = val

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
    self.lut_prop.append(outline)
    ## index_2
    outline = "index_2(\""
    for i in range(len(ilist)-1):
      outline += str(ilist[i])+", " 
    outline += str(ilist[len(ilist)-1])+"\");" 
    self.lut_prop.append(outline)
    ## values
    self.lut_prop.append("values ( \\")
    for i in range(len(ilist)):
      outline = "\""
      for j in range(len(jlist)-1):
        #outline += str(self.list2_prop[i][j])+", "
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

  def print_setuphold_msg(self, targetLib, targetCell, stage=None, tstep_mag=None):
    if(stage == 1):
      msg = "1st stage sparse "+str(self.mode)+" search, timestep: "
    elif(stage == 2):
      msg = "2nd stage sparse "+str(self.mode)+" search, timestep: "
    elif(stage == 3):
      msg = "3rd stage sparse "+str(self.mode)+" search, timestep: "
    elif(stage == 4):
      msg = "4th stage precise "+str(self.mode)+" search, timestep: "
    else:
      print("argument stage: "+str(stage)+" is not matched with 1/2/3/4, die\n")
      my_exit()

    if(self.mode == "setup" or self.mode == "recov"):
      targetLib.print_msg_sim("(slope/load=" +str(self.target_slope)+ "/" +str(self.target_load)+") " \
        + str(msg)+ str(targetCell.sim_setup_timestep * tstep_mag))
    elif(self.mode == "hold" or self.mode == "remov"):
      targetLib.print_msg_sim("(slope/load=" +str(self.target_slope)+ "/" +str(self.target_load)+") " \
        + str(msg)+ str(targetCell.sim_hold_timestep * tstep_mag))
    else:
      print("argument self.mode: "+str(self.mode)+" is not matched with setup/hold/recov/remov, die\n")
      my_exit()
      
  def print_setuphold_intl_msg(self, targetLib, targetCell, stage=None):
      targetLib.print_msg_sim("["+str(self.mode)+" (slope/load=" +str(self.target_slope)+ "/" +str(self.target_load)
        +")] tsetup_search: "+str(f'{self.target_tsetup:,.4f}')+str(targetLib.time_unit)
        +" thold_search: "+str(f'{self.target_thold:,.4f}')+str(targetLib.time_unit)+" stg:"+str(stage)) #+" sp: "+str(self.spicefo))
      
