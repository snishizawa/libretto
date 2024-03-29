#!/bin/python3

def main_350():
    cmd_file = 'libretto.cmd'
    gen_lib_common("OSU350", cmd_file)
    gen_char_cond("3.3", cmd_file)
#    gen_comb("OSU350", cmd_file, "OA22_1X",  "OA22",  ['A1','A2','B1','B2'],   ['Y'],  ['Y=((B1|B2)&(A1|A2))'],  '1', 'NETLIST/OA22_1X.spi')
#    gen_seq ("OSU350", cmd_file, "DFFAR_1X", "DFF_PCPU_NR", ['DATA','CLK','NRST'], ['Q'], ['IQ','IQN'], ['Q=IQ','QN=IQN'], '1', 'NETLIST/DFFAR_1X.spi')
#    gen_comb("OSU350", cmd_file, "INV_1X",   "INV",   ['A'],             ['YB'], ['YB=!A'],         '1', 'NETLIST/INV_1X.spi')
#    gen_comb("OSU350", cmd_file, "NAND2_1X", "NAND2", ['A','B'],         ['YB'], ['YB=!(A&B)'],     '1', 'NETLIST/NAND2_1X.spi')
#    gen_comb("OSU350", cmd_file, "NAND3_1X", "NAND3", ['A','B','C'],     ['YB'], ['YB=!(A&B&C)'],   '1', 'NETLIST/NAND3_1X.spi')
#    gen_comb("OSU350", cmd_file, "NAND4_1X", "NAND4", ['A','B','C','D'], ['YB'], ['YB=!(A&B&C&D)'], '1', 'NETLIST/NAND4_1X.spi')
#    gen_comb("OSU350", cmd_file, "NOR2_1X",  "NOR2",  ['A','B'],         ['YB'], ['YB=!(A|B)'],     '1', 'NETLIST/NOR2_1X.spi')
#    gen_comb("OSU350", cmd_file, "NOR3_1X",  "NOR3",  ['A','B','C'],     ['YB'], ['YB=!(A|B|C)'],   '1', 'NETLIST/NOR3_1X.spi')
#    gen_comb("OSU350", cmd_file, "NOR4_1X",  "NOR4",  ['A','B','C','D'], ['YB'], ['YB=!(A|B|C|D)'], '1', 'NETLIST/NOR4_1X.spi')
#    gen_comb("OSU350", cmd_file, "AND2_1X",  "AND2",  ['A','B'],         ['Y'],  ['Y=(A&B)'],       '1', 'NETLIST/AND2_1X.spi')
#    gen_comb("OSU350", cmd_file, "AND3_1X",  "AND3",  ['A','B','C'],     ['Y'],  ['Y=(A&B&C)'],     '1', 'NETLIST/AND3_1X.spi')
#    gen_comb("OSU350", cmd_file, "AND4_1X",  "AND4",  ['A','B','C','D'], ['Y'],  ['Y=(A&B&C&D)'],   '1', 'NETLIST/AND4_1X.spi')
#    gen_comb("OSU350", cmd_file, "OR2_1X",   "OR2",   ['A','B'],         ['Y'],  ['Y=(A|B)'],       '1', 'NETLIST/OR2_1X.spi')
#    gen_comb("OSU350", cmd_file, "OR3_1X",   "OR3",   ['A','B','C'],     ['Y'],  ['Y=(A|B|C)'],     '1', 'NETLIST/OR3_1X.spi')
#    gen_comb("OSU350", cmd_file, "OR4_1X",   "OR4",   ['A','B','C','D'], ['Y'],  ['Y=(A|B|C|D)'],   '1', 'NETLIST/OR4_1X.spi')
#    gen_comb("OSU350", cmd_file, "AOI21_1X", "AOI21", ['A1','A2','B'],         ['YB'], ['YB=!(B|(A1&A2))'],      '1', 'NETLIST/AOI21_1X.spi')
#    gen_comb("OSU350", cmd_file, "AOI22_1X", "AOI22", ['A1','A2','B1','B2'],   ['YB'], ['YB=!((B1&B2)|(A1&A2))'],'1', 'NETLIST/AOI22_1X.spi')
#    gen_comb("OSU350", cmd_file, "OAI21_1X", "OAI21", ['A1','A2','B'],         ['YB'], ['YB=!(B&(A1|A2))'],      '1', 'NETLIST/OAI21_1X.spi')
#    gen_comb("OSU350", cmd_file, "OAI22_1X", "OAI22", ['A1','A2','B1','B2'],   ['YB'], ['YB=!((B1|B2)&(A1|A2))'],'1', 'NETLIST/OAI22_1X.spi')
#    gen_comb("OSU350", cmd_file, "AO21_1X",  "AO21",  ['A1','A2','B'],         ['Y'],  ['Y=(B|(A1&A2))'],        '1', 'NETLIST/AO21_1X.spi')
#    gen_comb("OSU350", cmd_file, "AO22_1X",  "AO22",  ['A1','A2','B1','B2'],   ['Y'],  ['Y=((B1&B2)|(A1&A2))'],  '1', 'NETLIST/AO22_1X.spi')
#    gen_comb("OSU350", cmd_file, "OA21_1X",  "OA21",  ['A1','A2','B'],         ['Y'],  ['Y=(B&(A1|A2))'],        '1', 'NETLIST/OA21_1X.spi')
#    gen_comb("OSU350", cmd_file, "XOR2_1X",  "XOR2",  ['A','B'],               ['Y'],  ['Y=((A&!B)&(!A&B))'],    '1', 'NETLIST/XOR2_1X.spi')
#    gen_comb("OSU350", cmd_file, "XNOR2_1X", "XNOR2", ['A','B'],               ['Y'],  ['Y=((!A&!B)&(A&B))'],    '1', 'NETLIST/XNOR2_1X.spi')
#    gen_comb("OSU350", cmd_file, "SEL2_1X",  "SEL2",  ['IN0','IN1','SEL'],     ['Y'],  ['Y=((A&!B)&(!A&B))'],    '1', 'NETLIST/SEL2_1X.spi')
    gen_seq ("OSU350", cmd_file, "DFF_1X", "DFF_PCPU", ['DATA','CLK'], ['Q'], ['Q','QN'], ['Q=IQ','QN=IQN'], '1', 'NETLIST/DFF_1X.spi')
#    gen_seq ("OSU350", cmd_file, "DFFARAS_1X", "DFF_PCPU_NRNS", ['DATA','CLK','NSET','NRST'], ['Q'], ['IQ','IQN'], ['Q=IQ','QN=IQN'], '1', 'NETLIST/DFFARAS_1X.spi')
    exit_libretto(cmd_file)

def main_180():
    cmd_file = 'libretto.cmd'
    gen_lib_common("ROHM180", cmd_file)
    gen_char_cond("1.8", cmd_file)
    gen_seq ("ROHM180", cmd_file, "ROHM18DFP010", "DFF_PCPU", ['DATA','CLK'], ['Q'], ['Q','QN'], ['Q=IQ','QN=IQN'], '1', 'rohmlib/ROHM18DFP010.sp')
    #gen_seq ("ROHM180", cmd_file, "ROHM18DFNRP010", "DFF_PCPU_NR", ['DATA','CLK', 'NRST'], ['Q'], ['Q','QN'], ['Q=IQ','QN=IQN'], '1', 'rohmlib/ROHM18DFNRP010.sp')
    #gen_comb("ROHM180", cmd_file, "ROHM18INVP010", "INV", ['A'], ['Y'], ['Y=!A'], '1', 'rohmlib/ROHM18INVP010.sp')
    gen_comb("ROHM180", cmd_file, "ROHM18INVP010", "INV", ['A'], ['Y'], ['Y=!A'], '1', 'rohmlib/ROHM18INVP010.sp')
#    gen_comb(cmd_file, "ROHM18NAND2P010", "NAND2", ['A','B'],         ['Y'], ['Y=!(A&B)'],     '1', 'rohmlib/ROHM18NAND2P010.sp')
#    gen_comb(cmd_file, "ROHM18NAND3P010", "NAND3", ['A','B','C'],     ['Y'], ['Y=!(A&B&C)'],   '1', 'rohmlib/ROHM18NAND3P010.sp')
#    gen_comb(cmd_file, "ROHM18NAND4P010", "NAND4", ['A','B','C','D'], ['Y'], ['Y=!(A&B&C&D)'], '1', 'rohmlib/ROHM18NAND4P010.sp')
#    gen_comb(cmd_file, "ROHM18NOR2P010",  "NOR2",  ['A','B'],         ['Y'], ['Y=!(A|B)'],     '1', 'rohmlib/ROHM18NOR2P010.sp')
#    gen_comb(cmd_file, "ROHM18NOR3P010",  "NOR3",  ['A','B','C'],     ['Y'], ['Y=!(A|B|C)'],   '1', 'rohmlib/ROHM18NOR3P010.sp')
#    gen_comb(cmd_file, "ROHM18NOR4P010",  "NOR4",  ['A','B','C','D'], ['Y'], ['Y=!(A|B|C|D)'], '1', 'rohmlib/ROHM18NOR4P010.sp')
    exit_libretto(cmd_file)

def gen_lib_common(name, cmd_file):
    with open(cmd_file,'w') as f:
        outlines = []
        outlines.append("# common settings for library\n")
        outlines.append("set_lib_name         "+str(name)+"\n")
        outlines.append("set_dotlib_name      "+str(name)+".lib\n")
        outlines.append("set_doc_name      "+str(name)+".md\n")
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

def gen_char_cond(vdd, cmd_file):
    with open(cmd_file,'a') as f:
        outlines = []
        outlines.append("# characterization conditions \n")
        outlines.append("set_process typ\n")
        outlines.append("set_temperature 25\n")
        outlines.append("set_vdd_voltage "+str(vdd)+"\n")
        outlines.append("set_vss_voltage 0\n")
        outlines.append("set_pwell_voltage 0\n")
        outlines.append("set_nwell_voltage "+str(vdd)+"\n")
        outlines.append("set_logic_threshold_high 0.8\n")
        outlines.append("set_logic_threshold_low 0.2\n")
        outlines.append("set_logic_high_to_low_threshold 0.5\n")
        outlines.append("set_logic_low_to_high_threshold 0.5\n")
        outlines.append("set_work_dir work\n")
        outlines.append("set_log_file log.txt\n")
#        outlines.append("set_simulator /usr/local/bin/ngspice \n")
        outlines.append("set_simulator /bin/ngspice \n")
#        outlines.append("set_simulator /cad/synopsys/hspice/P-2019.06-1/hspice/bin/hspice -CC -port 2990wx:25000 -i \n")
        outlines.append("set_run_sim true\n")
#        outlines.append("set_run_sim false\n")
        outlines.append("set_mt_sim true\n")
#        outlines.append("set_mt_sim false\n")
#        outlines.append("set_supress_message false\n")
        outlines.append("set_supress_sim_message false\n")
        outlines.append("set_supress_message true\n")
#        outlines.append("set_supress_sim_message true\n")
        outlines.append("set_supress_debug_message true\n")
        outlines.append("set_energy_meas_low_threshold 0.01\n")
        outlines.append("set_energy_meas_high_threshold 0.99\n")
        outlines.append("set_energy_meas_time_extent 10\n")
        outlines.append("set_operating_conditions PVT_3P5V_25C\n")
        outlines.append("# initialize workspace\n")
        outlines.append("initialize\n")
        f.writelines(outlines)
    f.close()

def gen_comb(target, cmd_file, cell_name, logic, inports, outports, funcs, area, netlist):
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
#        outlines.append("add_slope {0.1 0.4 1.6 6.4} \n")
#        outlines.append("add_load  {0.01 0.04 0.16 0.64} \n")
        if(target == "ROHM180"):
            outlines.append("add_slope  {0.1 0.7 4.9} \n")
            outlines.append("add_load  {0.01 0.1 1.0} \n")
            #outlines.append("add_slope slope1 {0.1 0.7 4.9} \n")
            #outlines.append("add_load  load1 {0.01 0.1 1.0} \n")
            #outlines.append("add_slope slope2 {0.1 4.9} \n")
            #outlines.append("add_load  load2 {0.01 } \n")
        elif(target == "OSU350"):
            outlines.append("add_slope {0.1 10} \n")
            outlines.append("add_load  {0.01 1.00} \n")
            outlines.append("add_slope {0.1 0.7 4.9} \n")
            outlines.append("add_load  {0.01 0.07 0.49} \n")
            #outlines.append("add_slope slope2 {0.1 0.2 0.4} \n")
            #outlines.append("add_load  load2 {0.01 0.02 0.04} \n")
        else:
            print("target is not registered!\n")
        line_add_area = 'add_area '+str(area)+'\n'
        outlines.append(line_add_area)
        line_add_netlist = 'add_netlist '+str(netlist)+'\n'
        outlines.append(line_add_netlist)
        if(target == "ROHM180"):
            outlines.append("add_model rohmlib/model_rohm180.sp\n")
        elif(target == "OSU350"):
            outlines.append("add_model NETLIST/model.sp\n")
        else:
            print("target is not registered!\n")
        outlines.append("add_simulation_timestep auto\n")
        outlines.append("characterize\n")
#        outlines.append("compress\n")
        outlines.append("export\n")
        outlines.append("\n")
        f.writelines(outlines)
    f.close()

def gen_seq(target, cmd_file, cell_name, logic, inports, outports, storage, funcs, area, netlist):
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
        if(target == "ROHM180"):
            outlines.append("add_slope {0.1 0.7 4.9} \n")
            outlines.append("add_load  {0.01 0.1 1.0} \n")
            #outlines.append("add_slope {0.1 4.9} \n")
            #outlines.append("add_load  {0.01 } \n")
        elif(target == "OSU350"):
            outlines.append("add_slope {0.1 10} \n")
            outlines.append("add_load  {0.01 1.00} \n")
            #outlines.append("add_slope {0.1 0.7 4.9} \n")
            #outlines.append("add_load  {0.01 0.07 0.49} \n")
            #outlines.append("add_slope {0.1 0.2 0.4} \n")
            #outlines.append("add_load  {0.01 0.02 0.04} \n")
        else:
            print("target is not registered!\n")
        outlines.append("add_clock_slope auto \n")
        line_add_area = 'add_area '+str(area)+'\n'
        outlines.append(line_add_area)
        line_add_netlist = 'add_netlist '+str(netlist)+'\n'
        outlines.append(line_add_netlist)
        if(target == "ROHM180"):
            outlines.append("add_model rohmlib/model_rohm180.sp\n")
        elif(target == "OSU350"):
            outlines.append("add_model NETLIST/model.sp\n")
        else:
            print("target is not registered!\n")
        outlines.append("add_simulation_timestep auto\n")
        outlines.append("add_simulation_setup_auto\n")
        outlines.append("add_simulation_hold_auto\n")
        #outlines.append("add_simulation_setup 0.1\n")
        #outlines.append("add_simulation_hold 0.1\n")
        outlines.append("characterize\n")
        outlines.append("export\n")
#        outlines.append("compress\n")
        f.writelines(outlines)
    f.close()

def exit_libretto(cmd_file):
    with open(cmd_file,'a') as f:
        outlines = []
        outlines.append("exit\n")
        f.writelines(outlines)
    f.close()

if __name__ == '__main__':
    #main_350()
    main_180()

