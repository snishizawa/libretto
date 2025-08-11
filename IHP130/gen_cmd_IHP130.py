#!/bin/python3
import argparse
import sys
sys.path.append("./script")
from myFunc import my_exit


def main_top(vdd="5.0", temperature="25", process="1.0", op_conditions="TC", name="IHP130",lib_name="IHP130_TC", path_model="./IHP130/MODEL", path_cell="./IHP130/NETLIST"):
  cmd_file = 'cmd/libretto.cmd'
  gen_lib_common(name=name, cmd_file=cmd_file, lib_name=lib_name)
  gen_char_cond(vdd=vdd, cmd_file=cmd_file, temperature=temperature, process=process, op_conditions=op_conditions)
  
  gen_comb(name, cmd_file, "sg13g2_inv_1"    , "INV"   , ['A']                ,['Y'],['Y=!A']                    ,'1', path_cell+"/sg13g2_inv_1.spi"  ,path_model)
  gen_comb(name, cmd_file, "sg13g2_nand2_1"  , "NAND2" , ['A','B']            ,['Y'],['Y=!(A&B)']                ,'1', path_cell+"/sg13g2_nand2_1.spi",path_model)
  gen_comb(name, cmd_file, "sg13g2_nand3_1"  , "NAND3" , ['A','B','C']        ,['Y'],['Y=!(A&B&C)']              ,'1', path_cell+"/sg13g2_nand3_1.spi",path_model)
  gen_comb(name, cmd_file, "sg13g2_nand4_1"  , "NAND4" , ['A','B','C','D']    ,['Y'],['Y=!(A&B&C&D)']            ,'1', path_cell+"/sg13g2_nand4_1.spi",path_model)
  gen_comb(name, cmd_file, "sg13g2_nor2_1"   , "NOR2"  , ['A','B']            ,['Y'],['Y=!(A|B)']                ,'1', path_cell+"/sg13g2_nor2_1.spi" ,path_model)
  gen_comb(name, cmd_file, "sg13g2_nor3_1"   , "NOR3"  , ['A','B','C']        ,['Y'],['Y=!(A|B|C)']              ,'1', path_cell+"/sg13g2_nor3_1.spi" ,path_model)
  gen_comb(name, cmd_file, "sg13g2_nor4_1"   , "NOR4"  , ['A','B','C','D']    ,['Y'],['Y=!(A|B|C|D)']            ,'1', path_cell+"/sg13g2_nor4_1.spi" ,path_model)
  gen_comb(name, cmd_file, "sg13g2_and2_1"   , "AND2"  , ['A','B']            ,['X'] ,['X=(A&B)']                  ,'1', path_cell+"/sg13g2_and2_1.spi" ,path_model)
  gen_comb(name, cmd_file, "sg13g2_and3_1"   , "AND3"  , ['A','B','C']        ,['X'] ,['X=(A&B&C)']                ,'1', path_cell+"/sg13g2_and3_1.spi" ,path_model)
  gen_comb(name, cmd_file, "sg13g2_and4_1"   , "AND4"  , ['A','B','C','D']    ,['X'] ,['X=(A&B&C&D)']              ,'1', path_cell+"/sg13g2_and4_1.spi" ,path_model)
  gen_comb(name, cmd_file, "sg13g2_or2_1"    , "OR2"   , ['A','B']            ,['X'] ,['X=(A|B)']                  ,'1', path_cell+"/sg13g2_or2_1.spi"  ,path_model)
  gen_comb(name, cmd_file, "sg13g2_or3_1"    , "OR3"   , ['A','B','C']        ,['X'] ,['X=(A|B|C)']                ,'1', path_cell+"/sg13g2_or3_1.spi"  ,path_model)
  gen_comb(name, cmd_file, "sg13g2_or4_1"    , "OR4"   , ['A','B','C','D']    ,['X'] ,['X=(A|B|C|D)']              ,'1', path_cell+"/sg13g2_or4_1.spi"  ,path_model)
  gen_comb(name, cmd_file, "sg13g2_a21oi_1"  , "AOI21" , ['A1','A2','B1']     ,['Y'],['Y=!(B|(A1&A2))']          ,'1', path_cell+"/sg13g2_a21oi_1.spi",path_model)
  gen_comb(name, cmd_file, "sg13g2_a22oi_1"  , "AOI22" , ['A1','A2','B1','B2'],['Y'],['Y=!((B1&B2)|(A1&A2))']    ,'1', path_cell+"/sg13g2_a22oi_1.spi",path_model)
  gen_comb(name, cmd_file, "sg13g2_o21ai_1"  , "OAI21" , ['A1','A2','B1']     ,['Y'],['Y=!(B&(A1|A2))']          ,'1', path_cell+"/sg13g2_o21ai_1.spi",path_model)
  gen_comb(name, cmd_file, "sg13g2_a21o_1"   , "AO21"  , ['A1','A2','B1']     ,['X'] ,['X=(B|(A1&A2))']            ,'1', path_cell+"/sg13g2_a21o_1.spi" ,path_model)
  gen_comb(name, cmd_file, "sg13g2_xor2_1"   , "XOR2"  , ['A','B']            ,['X'] ,['X=((A&!B)&(!A&B))']        ,'1', path_cell+"/sg13g2_xor2_1.spi" ,path_model)
  gen_comb(name, cmd_file, "sg13g2_xnor2_1"  , "XNOR2" , ['A','B']            ,['Y'] ,['Y=((!A&!B)&(A&B))']        ,'1', path_cell+"/sg13g2_xnor2_1.spi",path_model)

  gen_seq (name, cmd_file, "sg13g2_dfrbp_1"  , "DFF_PCPU_NR"  , ['D','CLK','RESET_B']       ,['Q' ],['IQ','IQN'] ,['Q=IQ','QN=IQN'], '1', path_cell+"/sg13g2_dfrbp_1.spi"  ,path_model)
  
  exit_libretto(cmd_file)


def gen_lib_common(name, cmd_file,lib_name="IHP130_TC"):
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
      outlines.append("set_vdd_name VDD\n")
      outlines.append("set_vss_name VSS\n")
      outlines.append("set_pwell_name VPW\n")
      outlines.append("set_nwell_name VNW\n")
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
      outlines.append("set_slope slope3 {4.9 0.7 0.1} \n")
      outlines.append("set_load  load3 {0.49 0.07 0.01} \n")

      outlines.append("# characterizer settings \n")
      outlines.append("set_work_dir work\n")
      outlines.append("set_tmp_dir work\n")
      outlines.append("set_tmp_file _tmp__\n")
      outlines.append("set_simulator ngspice \n")
#      outlines.append("set_simulator /usr/local/bin/ngspice \n")
#      outlines.append("set_simulator /eda/synopsys/hspice/T-2022.06/hspice/linux64/hspice \n")
      outlines.append("set_run_sim true\n")
      outlines.append("set_num_thread 8\n")
      outlines.append("set_sim_nice 19\n")
      outlines.append("set_compress_result false\n")
#      outlines.append("set_supress_message true\n")
#      outlines.append("set_supress_sim_message true\n")
#      outlines.append("set_supress_debug_message true\n")
      outlines.append("set_supress_message false\n")
      outlines.append("set_supress_sim_message false\n")
      outlines.append("set_supress_debug_message true\n")

      outlines.append("# initialize workspace\n")
      outlines.append("initialize\n")
      f.writelines(outlines)
   f.close()

def gen_comb(target, cmd_file, cell_name, logic, inports, outports, funcs, area, netlist, path_model="./IHP130/MODEL"):
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
      outlines.append("add_slope slope1 \n")
      outlines.append("add_load  load1  \n")

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

def gen_seq(target, cmd_file, cell_name, logic, inports, outports, storage, funcs, area, netlist, path_model="./IHP130/MODEL"):
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
  parser.add_argument('--vdd'       , type=float, default='1.5'    , help='VDD')
  parser.add_argument('--temp'      , type=float, default='27'     , help='Temperature')  
  parser.add_argument('--process'   , type=float, default='1.1'    , help='process')  
  parser.add_argument('--condition' , type=str  , default='NCCOM'  , help='OperationgCondition')  
  parser.add_argument('--p_name'    , type=str  , default='IHP' , help='ProcessName')  
  parser.add_argument('--lib_name'  , type=str  , default='IHP_1P5V_27C'      , help='LibraryName')  
  parser.add_argument('--path_model', type=str  , default='./spice_model', help='Path of MOS-model')  
  parser.add_argument('--path_cell' , type=str  , default='./IHP130/NETLIST', help='Path of std-cell')  
  args = parser.parse_args()

  print(args)
  #----------------------------------
  main_top(vdd=args.vdd, temperature=args.temp, process=args.process, \
           op_conditions=args.condition, name=args.p_name,lib_name=args.lib_name, path_model=args.path_model, path_cell=args.path_cell)
