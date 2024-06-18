#!/bin/python3
import argparse
import sys
sys.path.append("./script")
from myFunc import my_exit


def main_top(vdd="5.0", temperature="25", process="1.0", op_conditions="TC", name="SKY130",lib_name="SKY130_TC", path_model="./SKY130/MODEL", path_cell="./SKY130/NETLIST"):
  cmd_file = 'cmd/libretto.cmd'
  gen_lib_common(name=name, cmd_file=cmd_file, lib_name=lib_name)
  gen_char_cond(vdd=vdd, cmd_file=cmd_file, temperature=temperature, process=process, op_conditions=op_conditions)
  
  gen_comb(name, cmd_file, "sky130_fd_sc_hd__inv_1"    , "INV"   , ['A']              ,['Y'],['Y=!A']          ,'1', path_cell+"/sky130_fd_sc_hd__inv_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__nand2_1"  , "NAND2" , ['A','B']          ,['Y'],['Y=!(A&B)']      ,'1', path_cell+"/sky130_fd_sc_hd__nand2_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__nand3_1"  , "NAND3" , ['A','B','C']      ,['Y'],['Y=!(A&B&C)']    ,'1', path_cell+"/sky130_fd_sc_hd__nand3_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__nand4_1"  , "NAND4" , ['A','B','C','D']  ,['Y'],['Y=!(A&BC&D&)']  ,'1', path_cell+"/sky130_fd_sc_hd__nand4_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__nor2_1"   , "NOR2" ,  ['A','B']          ,['Y'],['Y=!(A|B)']      ,'1', path_cell+"/sky130_fd_sc_hd__nor2_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__nor3_1"   , "NOR3" ,  ['A','B','C']      ,['Y'],['Y=!(A|B|C)']    ,'1', path_cell+"/sky130_fd_sc_hd__nor3_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__nor4_1"   , "NOR4" ,  ['A','B','C','D']  ,['Y'],['Y=!(A|BC|D|)']  ,'1', path_cell+"/sky130_fd_sc_hd__nor4_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__and2_1"   , "AND2" ,  ['A','B']          ,['X'],['X=(A&B)']      ,'1', path_cell+"/sky130_fd_sc_hd__and2_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__and3_1"   , "AND3" ,  ['A','B','C']      ,['X'],['X=(A&B&C)']    ,'1', path_cell+"/sky130_fd_sc_hd__and3_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__and4_1"   , "AND4" ,  ['A','B','C','D']  ,['X'],['X=(A&BC&D)']   ,'1', path_cell+"/sky130_fd_sc_hd__and4_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__or2_1"    , "OR2" ,   ['A','B']          ,['X'],['X=(A|B)']      ,'1', path_cell+"/sky130_fd_sc_hd__or2_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__or3_1"    , "OR3" ,   ['A','B','C']      ,['X'],['X=(A|B|C)']    ,'1', path_cell+"/sky130_fd_sc_hd__or3_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__or4_1"    , "OR4" ,   ['A','B','C','D']  ,['X'],['X=(A|B|C|D)']  ,'1', path_cell+"/sky130_fd_sc_hd__or4_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__a21oi_1"  , "AOI21" ,   ['A1','A2','B1']        ,['Y'],['Y=!(B1|(A1&A2))']        ,'1', path_cell+"/sky130_fd_sc_hd__a21oi_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__a22oi_1"  , "AOI22" ,   ['A1','A2','B1','B2']  ,['Y'],['Y=!((B1&B2)|(A1&A2))']  ,'1', path_cell+"/sky130_fd_sc_hd__a22oi_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__o21ai_1"  , "OAI21" ,   ['A1','A2','B1']        ,['Y'],['Y=!(B1&(A1|A2))']        ,'1', path_cell+"/sky130_fd_sc_hd__o21ai_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__o22ai_1"  , "OAI22" ,   ['A1','A2','B1','B2']  ,['Y'],['Y=!((B1|B2)&(A1|A2))']  ,'1', path_cell+"/sky130_fd_sc_hd__o22ai_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__xor2_1"   , "XOR2" ,    ['A','B']  ,['X'],['X=((A&!B)&(!A&B))']  ,'1', path_cell+"/sky130_fd_sc_hd__xor2_1.spice"  ,path_model)
#  gen_comb(name, cmd_file, "sky130_fd_sc_hd__xnor2_1"  , "XNOR2" ,   ['A','B']  ,['Y'],['Y=((A&!B)&(!A&B))']  ,'1', path_cell+"/sky130_fd_sc_hd__xnor2_1.spice"  ,path_model)
  gen_seq(name, cmd_file, "sky130_fd_sc_hd__dfxtp_1"  , "DFF_PCPU" ,   ['D','CLK']  ,['Q'], ['IQ','IQN'], ['Q=IQ','QN=IQN']  ,'1', path_cell+"/sky130_fd_sc_hd__dfxtp_1.spice"  ,path_model)

#  gen_comb(name, cmd_file, "SEL2_1X"   , "SEL2"  , ['IN0','IN1','SEL']  ,['Y'] ,['Y=((IN0&!SEL)&(IN1&SEL))'] ,'1', path_cell+"/SEL2_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "NAND2_1X"  , "NAND2" , ['A','B']            ,['YB'],['YB=!(A&B)']                ,'1', path_cell+"/NAND2_1X.spi",path_model)
#  gen_comb(name, cmd_file, "NAND3_1X"  , "NAND3" , ['A','B','C']        ,['YB'],['YB=!(A&B&C)']              ,'1', path_cell+"/NAND3_1X.spi",path_model)
#  gen_comb(name, cmd_file, "NAND4_1X"  , "NAND4" , ['A','B','C','D']    ,['YB'],['YB=!(A&B&C&D)']            ,'1', path_cell+"/NAND4_1X.spi",path_model)
#  gen_comb(name, cmd_file, "NOR2_1X"   , "NOR2"  , ['A','B']            ,['YB'],['YB=!(A|B)']                ,'1', path_cell+"/NOR2_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "NOR3_1X"   , "NOR3"  , ['A','B','C']        ,['YB'],['YB=!(A|B|C)']              ,'1', path_cell+"/NOR3_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "NOR4_1X"   , "NOR4"  , ['A','B','C','D']    ,['YB'],['YB=!(A|B|C|D)']            ,'1', path_cell+"/NOR4_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "AND2_1X"   , "AND2"  , ['A','B']            ,['Y'] ,['Y=(A&B)']                  ,'1', path_cell+"/AND2_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "AND3_1X"   , "AND3"  , ['A','B','C']        ,['Y'] ,['Y=(A&B&C)']                ,'1', path_cell+"/AND3_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "AND4_1X"   , "AND4"  , ['A','B','C','D']    ,['Y'] ,['Y=(A&B&C&D)']              ,'1', path_cell+"/AND4_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "OR2_1X"    , "OR2"   , ['A','B']            ,['Y'] ,['Y=(A|B)']                  ,'1', path_cell+"/OR2_1X.spi"  ,path_model)
#  gen_comb(name, cmd_file, "OR3_1X"    , "OR3"   , ['A','B','C']        ,['Y'] ,['Y=(A|B|C)']                ,'1', path_cell+"/OR3_1X.spi"  ,path_model)
#  gen_comb(name, cmd_file, "OR4_1X"    , "OR4"   , ['A','B','C','D']    ,['Y'] ,['Y=(A|B|C|D)']              ,'1', path_cell+"/OR4_1X.spi"  ,path_model)
#  gen_comb(name, cmd_file, "AOI21_1X"  , "AOI21" , ['A1','A2','B']      ,['YB'],['YB=!(B|(A1&A2))']          ,'1', path_cell+"/AOI21_1X.spi",path_model)
#  gen_comb(name, cmd_file, "AOI22_1X"  , "AOI22" , ['A1','A2','B1','B2'],['YB'],['YB=!((B1&B2)|(A1&A2))']    ,'1', path_cell+"/AOI22_1X.spi",path_model)
#  gen_comb(name, cmd_file, "OAI21_1X"  , "OAI21" , ['A1','A2','B']      ,['YB'],['YB=!(B&(A1|A2))']          ,'1', path_cell+"/OAI21_1X.spi",path_model)
#  gen_comb(name, cmd_file, "OAI22_1X"  , "OAI22" , ['A1','A2','B1','B2'],['YB'],['YB=!((B1|B2)&(A1|A2))']    ,'1', path_cell+"/OAI22_1X.spi",path_model)
#  gen_comb(name, cmd_file, "AO21_1X"   , "AO21"  , ['A1','A2','B']      ,['Y'] ,['Y=(B|(A1&A2))']            ,'1', path_cell+"/AO21_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "AO22_1X"   , "AO22"  , ['A1','A2','B1','B2'],['Y'] ,['Y=((B1&B2)|(A1&A2))']      ,'1', path_cell+"/AO22_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "OA21_1X"   , "OA21"  , ['A1','A2','B']      ,['Y'] ,['Y=(B&(A1|A2))']            ,'1', path_cell+"/OA21_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "OA22_1X"   , "OA22"  , ['A1','A2','B1','B2'],['Y'] ,['Y=((B1|B2)&(A1|A2))']      ,'1', path_cell+"/OA22_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "XOR2_1X"   , "XOR2"  , ['A','B']            ,['Y'] ,['Y=((A&!B)&(!A&B))']        ,'1', path_cell+"/XOR2_1X.spi" ,path_model)
#  gen_comb(name, cmd_file, "XNOR2_1X"  , "XNOR2" , ['A','B']            ,['Y'] ,['Y=((!A&!B)&(A&B))']        ,'1', path_cell+"/XNOR2_1X.spi",path_model)
#
#  gen_seq (name, cmd_file, "DFFAS_1X"  , "DFF_PCPU_NS"  , ['DATA','CLK','NSET']       ,['Q' ],['IQ','IQN'] ,['Q=IQ','QN=IQN'], '1', path_cell+"/DFFAS_1X.spi"  ,path_model)
#  gen_seq (name, cmd_file, "DFFAR_1X"  , "DFF_PCPU_NR"  , ['DATA','CLK','NRST']       ,['Q' ],['IQ','IQN'] ,['Q=IQ','QN=IQN'], '1', path_cell+"/DFFAR_1X.spi"  ,path_model)
#  gen_seq (name, cmd_file, "DFF_1X"    , "DFF_PCPU"     , ['DATA','CLK']              ,['Q'] ,['Q','QN']   ,['Q=IQ','QN=IQN'], '1', path_cell+"/DFF_1X.spi"    ,path_model)
#  gen_seq (name, cmd_file, "DFFARAS_1X", "DFF_PCPU_NRNS", ['DATA','CLK','NSET','NRST'],['Q'] ,['IQ','IQN'] ,['Q=IQ','QN=IQN'], '1', path_cell+"/DFFARAS_1X.spi",path_model)
  
  exit_libretto(cmd_file)


def gen_lib_common(name, cmd_file,lib_name="SKY130_TC"):
   with open(cmd_file,'w') as f:
      outlines = []
      outlines.append("# common settings for library\n")
      outlines.append("set_lib_name         "+str(lib_name)+"\n")
      outlines.append("set_dotlib_name      "+str(lib_name)+".lib\n")
      outlines.append("set_doc_name      "+str(lib_name)+".md\n")
      outlines.append("set_verilog_name     "+str(name)+".v\n")
      outlines.append("set_cell_name_suffix "+str(name)+"_\n")
      outlines.append("set_cell_name_prefix _V1\n")
      outlines.append("set_voltage_unit V\n")
      outlines.append("set_capacitance_unit pF\n")
      outlines.append("set_resistance_unit Ohm\n")
      outlines.append("set_current_unit mA\n")
      outlines.append("set_leakage_power_unit pW \n")
      outlines.append("set_energy_unit fJ \n")
      outlines.append("set_time_unit ns\n")
      outlines.append("set_vdd_name VPWR\n")
      outlines.append("set_vss_name VGND\n")
      outlines.append("set_pwell_name VNB\n")
      outlines.append("set_nwell_name VPB\n")
      f.writelines(outlines)
   f.close()

def gen_char_cond(vdd, cmd_file, temperature="25", process="1.0", op_conditions="TCCOM"):
   with open(cmd_file,'a') as f:
      outlines = []
      outlines.append("# characterization conditions \n")
      outlines.append("set_process "+str(process)+"\n")
      outlines.append("set_temperature "+str(temperature)+"\n")
      outlines.append("set_vdd_voltage "+str(vdd)+"\n")
      outlines.append("set_vss_voltage 0\n")
      outlines.append("set_pwell_voltage 0\n")
      outlines.append("set_nwell_voltage "+str(vdd)+"\n")
      outlines.append("set_logic_threshold_high 0.8\n")
      outlines.append("set_logic_threshold_low 0.2\n")
      outlines.append("set_logic_high_to_low_threshold 0.5\n")
      outlines.append("set_logic_low_to_high_threshold 0.5\n")
      outlines.append("set_energy_meas_low_threshold 0.01\n")
      outlines.append("set_energy_meas_high_threshold 0.99\n")
      outlines.append("set_energy_meas_time_extent 10\n")
      outlines.append("set_operating_conditions "+str(op_conditions)+"\n")
      outlines.append("set_slope slope1 {0.1 0.7} \n")
      outlines.append("set_load  load1 {0.01 0.07} \n")
      outlines.append("set_slope slope2 {0.1 0.7 4.9} \n")
      outlines.append("set_load  load2 {0.01 0.07 0.49} \n")

      outlines.append("# characterizer setting \n")
      outlines.append("set_work_dir work\n")
      outlines.append("set_tmp_dir work\n")
      outlines.append("set_tmp_file _tmp__\n")
      outlines.append("set_simulator ngspice \n")
#      outlines.append("set_simulator /usr/local/bin/ngspice \n")
#      outlines.append("set_simulator /eda/synopsys/hspice/T-2022.06/hspice/linux64/hspice \n")
      outlines.append("set_run_sim true\n")
      outlines.append("set_mt_sim true\n")
#      outlines.append("set_mt_sim false\n")
      outlines.append("set_sim_nice 19\n")
      outlines.append("set_compress_result False\n")
#      outlines.append("set_supress_message true\n")
#      outlines.append("set_supress_sim_message true\n")
#      outlines.append("set_supress_debug_message true\n")
      outlines.append("set_supress_message false\n")
      outlines.append("set_supress_sim_message false\n")
      outlines.append("set_supress_debug_message false\n")

      outlines.append("# initialize workspace\n")
      outlines.append("initialize\n")
      f.writelines(outlines)
   f.close()

def gen_comb(target, cmd_file, cell_name, logic, inports, outports, funcs, area, netlist, path_model="./SKY130/MODEL"):
   with open(cmd_file,'a') as f:
      outlines = []
      outlines.append("\n")
      outlines.append("## add circuit\n")
      line_add_cell = 'add_cell -n '+str(cell_name)+' -l '+str(logic)+' -i '
      for w1 in inports:
         line_add_cell += str(w1)+' '
      line_add_cell += '-o '
      for w1 in outports:
         line_add_cell += str(w1)+' '
      line_add_cell += '-f '
      for w1 in funcs:
         line_add_cell += str(w1)+' '
      line_add_cell += '\n'
      outlines.append(line_add_cell)
      outlines.append("add_slope slope2 \n")
      outlines.append("add_load  load2  \n")

      line_add_area = 'add_area '+str(area)+'\n'
      outlines.append(line_add_area)
      line_add_netlist = 'add_netlist '+str(netlist)+'\n'
      outlines.append(line_add_netlist)

      outlines.append("add_model "+str(path_model)+"\n")
      outlines.append("add_simulation_timestep auto slope1\n")
      outlines.append("characterize\n")
      outlines.append("export\n")
      outlines.append("\n")
      f.writelines(outlines)
   f.close()

def gen_seq(target, cmd_file, cell_name, logic, inports, outports, storage, funcs, area, netlist, path_model="./SKY130/MODEL"):
   with open(cmd_file,'a') as f:
      outlines = []
      outlines.append("## add circuit\n")
      line_add_flop = 'add_flop -n '+str(cell_name)+' -l '+str(logic)
      if((logic == 'DFF_PCPU_NRNS')or(logic == 'DFF_PCNU_NRNS')or(logic == 'DFF_NCPU_NRNS')or(logic == 'DFF_NCNU_NRNS')):
         line_add_flop += ' -i '+str(inports[0])+' -c '+str(inports[1])+' -s '+str(inports[2])+' -r '+str(inports[3]) 
      elif((logic == 'DFF_PCPU_NR')or(logic == 'DFF_PCNU_NR')or(logic == 'DFF_NCPU_NR')or(logic == 'DFF_NCNU_NR')):
         line_add_flop += ' -i '+str(inports[0])+' -c '+str(inports[1])+' -r '+str(inports[2]) 
      elif((logic == 'DFF_PCPU_NS')or(logic == 'DFF_PCNU_NS')or(logic == 'DFF_NCPU_NS')or(logic == 'DFF_NCNU_NS')):
         line_add_flop += ' -i '+str(inports[0])+' -c '+str(inports[1])+' -s '+str(inports[2])
      elif((logic == 'DFF_PCPU')or(logic == 'DFF_PCNU')or(logic == 'DFF_NCPU')or(logic == 'DFF_NCNU')):
         line_add_flop += ' -i '+str(inports[0])+' -c '+str(inports[1])
      else:
         print("function not matched!\n")
      line_add_flop += ' -o '
      for w1 in outports:
         line_add_flop += str(w1)+' '
      line_add_flop += '-q '
      for w1 in storage:
         line_add_flop += str(w1)+' '
      line_add_flop += '-f '
      for w1 in funcs:
         line_add_flop += str(w1)+' '
      line_add_flop += '\n'
      outlines.append(line_add_flop)

      #-- len(slope)>=2 & len(load)>=0, need max(slope)>2ns 
      #outlines.append("add_slope {0.1 0.7 4.9} \n")
      #outlines.append("add_load  {0.01 0.07 0.49} \n")
      #outlines.append("add_slope {0.1 0.7 4.9} \n")
      #outlines.append("add_slope {0.1 0.3 0.7 2.1 4.9} \n")
      #outlines.append("add_load  {0.01 0.03 0.09 0.27 0.49} \n")
      #outlines.append("add_slope {4.9} \n")
      #outlines.append("add_load  {0.49} \n")
      outlines.append("add_slope slope1 \n")
      outlines.append("add_load  load1  \n")

      #outlines.append("add_clock_slope auto \n")
      outlines.append("add_clock_slope auto slope1\n")
      line_add_area = 'add_area '+str(area)+'\n'
      outlines.append(line_add_area)
      line_add_netlist = 'add_netlist '+str(netlist)+'\n'
      outlines.append(line_add_netlist)

      outlines.append("add_model "+str(path_model)+"\n")

      outlines.append("add_simulation_timestep auto slope1\n")
      outlines.append("add_simulation_setup_auto slope1\n")
      outlines.append("add_simulation_hold_auto slope1\n")
      outlines.append("characterize\n")
      outlines.append("compress\n")
      outlines.append("export\n")
      f.writelines(outlines)
   f.close()

def exit_libretto(cmd_file):
   with open(cmd_file,'a') as f:
      outlines = []
      outlines.append("exit\n")
      f.writelines(outlines)
   f.close()

if __name__ == '__main__':

  #----------------------------------
  parser = argparse.ArgumentParser(description='generate cmd/libretto.cmd')
  parser.add_argument('--vdd'       , type=float, default='5.1'    , help='VDD')
  parser.add_argument('--temp'      , type=float, default='26'     , help='Temperature')  
  parser.add_argument('--process'   , type=float, default='1.1'    , help='process')  
  parser.add_argument('--condition' , type=str  , default='NCCOM'  , help='OperationgCondition')  
  parser.add_argument('--p_name'    , type=str  , default='OSU' , help='ProcessName')  
  parser.add_argument('--lib_name'  , type=str  , default='OSU_5P1V_26C'      , help='LibraryName')  
  parser.add_argument('--path_model', type=str  , default='./spice_model', help='Path of MOS-model')  
  parser.add_argument('--path_cell' , type=str  , default='./SKY130/NETLIST', help='Path of std-cell')  
  args = parser.parse_args()

  print(args)
  #----------------------------------
  main_top(vdd=args.vdd, temperature=args.temp, process=args.process, \
           op_conditions=args.condition, name=args.p_name,lib_name=args.lib_name, path_model=args.path_model, path_cell=args.path_cell)
