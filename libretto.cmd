# common settings for library
set_lib_name         ROHM180
set_dotlib_name      ROHM180.lib
set_verilog_name     ROHM180.v
set_cell_name_suffix ROHM180_
set_cell_name_prefix _V1
set_voltage_unit V
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
set_vdd_voltage 1.8
set_vss_voltage 0
set_pwell_voltage 0
set_nwell_voltage 1.8
set_logic_threshold_high 0.8
set_logic_threshold_low 0.2
set_logic_high_to_low_threshold 0.5
set_logic_low_to_high_threshold 0.5
set_work_dir work
set_simulator /usr/local/bin/ngspice 
set_energy_meas_low_threshold 0.01
set_energy_meas_high_threshold 0.99
set_energy_meas_time_extent 1
set_operating_conditions PVT_3P5V_25C
# initialize workspace
initialize

## add circuit
#	add_cell -n ROHM18INVP010 -l INV -i A -o Y -f Y=!A 
#	add_slope {0.1 0.4 1.6 6.4} 
#	add_load  {0.1 0.4 1.6 6.4} 
#	add_area 1
#	add_netlist rohmlib/ROHM18INVP010.sp
#	add_model rohmlib/model_rohm180.sp
#	add_simulation_timestep auto
#	characterize

## add circuit
add_flop -n ROHM18DFP010 -l DFF_PCPU -i DATA -c CLK -o Q -f Q=IQ QN=IQN 
add_slope {0.1 0.4 1.6 6.4} 
add_load  {0.1 0.4 1.6 6.4} 
add_clock_slope auto 
add_area 1
add_netlist rohmlib/ROHM18DFP010.sp
add_model rohmlib/model_rohm180.sp
add_simulation_timestep auto
add_simulation_setup_auto
add_simulation_hold_auto
characterize
export
