# common settings for library
set_lib_name OSU035
set_dotlib_name OSU035.lib
set_verilog_name OSU035.v
set_cell_name_suffix OSU035_
set_cell_name_prefix _V1
set_voltage_unit mV
set_capacitance_unit pF
set_resistance_unit Ohm
set_current_unit mA
set_leakage_power_unit pW 
set_time_unit ns
set_vdd_name VDD
set_vss_name VSS
set_pwell_name VPW
set_nwell_name VNW

# characterization conditions 
set_process typ
set_temperature 25
set_vdd_voltage 3.5
set_vss_voltage 0
set_pwell_voltage 0
set_nwell_voltage 3.5
set_logic_threshold_high 0.8
set_logic_threshold_low 0.2
set_logic_high_to_low_threshold 0.5
set_logic_low_to_high_threshold 0.5
set_work_dir work
set_simulator /usr/local/bin/ngspice 
set_energy_meas_low_threshold 0.01
set_energy_meas_high_threshold 0.99
set_energy_meas_time_extent 4
set_operating_conditions PVT_3P5V_25C

# initialize workspace
initialize

## add circuit
#add_cell -n INV_1X -l INV -i A -o Y -f Y=!A 
#add_slope {1 4 16 64} 
#add_load  {1 4 16 64} 
#add_netlist NETLIST/INV_1X.spi
#add_model NETLIST/model.sp
#add_simulation_timestep auto
#
## characterize
#characterize
#export
#
##add_cell -n AND2_1X -l AND2 -i A B -o Y -f Y=A*B 
##add_slope {1 4 16 64} 
##add_load  {1 4 16 64} 
##add_netlist NETLIST/AND2_1X.spi
##add_model NETLIST/model.sp
##add_simulation_timestep auto
##
### characterize
##characterize
##export
##
#add_cell -n NAND2_1X -l NAND2 -i A B -o Y -f Y=!(A*B) 
#add_slope {1 4 16 64} 
#add_load  {1 4 16 64} 
#add_netlist NETLIST/NAND2_1X.spi
#add_model NETLIST/model.sp
#add_simulation_timestep auto
#
## characterize
#characterize
#export
#
#add_cell -n NAND3_1X -l NAND3 -i A B C -o Y -f Y=!(A*B*C) 
#add_slope {1 4 16 64} 
#add_load  {1 4 16 64} 
#add_netlist NETLIST/NAND3_1X.spi
#add_model NETLIST/model.sp
#add_simulation_timestep auto
#
## characterize
#characterize
#export
#
#add_cell -n NAND4_1X -l NAND4 -i A B C D -o Y -f Y=!(A*B*C*D) 
#add_slope {1 4 16 64} 
#add_load  {1 4 16 64} 
#add_netlist NETLIST/NAND4_1X.spi
#add_model NETLIST/model.sp
#add_simulation_timestep auto
#
## characterize
#characterize
#export
#
#add_cell -n NOR2_1X -l NOR2 -i A B -o Y -f Y=!(A|B) 
#add_slope {1 4 16 64} 
#add_load  {1 4 16 64} 
#add_netlist NETLIST/NOR2_1X.spi
#add_model NETLIST/model.sp
#add_simulation_timestep auto
#
## characterize
#characterize
#export
#
add_cell -n NOR3_1X -l NOR3 -i A B C -o YB -f YB=!(A|B|C) 
add_slope {1 4 16 64} 
add_load  {1 4 16 64} 
add_netlist NETLIST/NOR3_1X.spi
add_model NETLIST/model.sp
add_simulation_timestep auto
#
## characterize
characterize
export
#
#add_cell -n NOR4_1X -l NOR4 -i A B C D -o Y -f Y=!(A|B|C|D) 
#add_slope {1 4 16 64} 
#add_load  {1 4 16 64} 
#add_netlist NETLIST/NOR4_1X.spi
#add_model NETLIST/model.sp
#add_simulation_timestep auto
#
## characterize
#characterize
#export
#
#add_cell -n XOR2_1X -l XOR2 -i A B -o Y -f Y=((A&(!B))|((!A)&B))
#add_slope {1 4 16 64} 
#add_load  {1 4 16 64} 
#add_netlist NETLIST/XOR2_1X.spi
#add_model NETLIST/model.sp
#add_simulation_timestep auto
#
## characterize
#characterize
#export
#
#add_cell -n XNOR2_1X -l XNOR2 -i A B -o Y -f Y=!((A&(!B))|((!A)&B))
#add_slope {1 4 16 64} 
#add_load  {1 4 16 64} 
#add_netlist NETLIST/XNOR2_1X.spi
#add_model NETLIST/model.sp
#add_simulation_timestep auto
#
## characterize
#characterize
#export
#
#add_cell -n SEL2_1X -l SEL2 -i IN0 IN1 SEL -o Y -f Y=!((IN0&(!SEL))|((IN1)&SEL))
#add_slope {1 4 16 64} 
#add_load  {1 4 16 64} 
#add_netlist NETLIST/SEL2_1X.spi
#add_model NETLIST/model.sp
#add_simulation_timestep auto
#
## characterize
#characterize
#export

## add circuit
## DFF, positive clock positive unate, async neg-reset, async neg-set
add_flop -n DFF_ARAS_1X -l DFF_PCPU_NRNS -i DATA -c CLK -s NSET -r NRST -o Q -q IQ IQN -f Q=IQ QN=IQN 
## DFF, positive clock negtive unate, async reset, async set
##add_flop -n DFFRS_1X -l DFF_PCNU_ARAS -i DATA -c CLK -s SET -r RST -o QN -q IQ IQN -f Q=IQ QN=IQN 
## DFF, positive clock positive unate, async reset
##add_flop -n DFFRS_1X -l DFF_PCBU_AR -i DATA -c CLK -r RST -o Q -q IQ IQN -f Q=IQ QN=IQN 
## DFF, positive clock positive unate
##add_flop -n DFFRS_1X -l DFF_PCPU -i DATA -c CLK -o Q -q IQ IQN -f Q=IQ QN=IQN 
add_slope {1 4 16 64} 
add_load  {1 4 16 64} 
add_clock_slope auto 
add_netlist NETLIST/DFF_ARAS_1X.spi
add_model NETLIST/model.sp
add_simulation_timestep auto
## --
add_simulation_setup_auto
## or 
#add_simulation_setup_lowest -10
#add_simulation_setup_highest 16
#add_simulation_setup_timestep 5
## --
add_simulation_hold_auto
## or 
##add_simulation_hold_lowest auto
##add_simulation_hold_highest auto
##add_simulation_hold_timestep auto
##
### characterize
characterize
export

exit

