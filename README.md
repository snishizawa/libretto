# libretto
## Introduction
An open cell library characterizer.
Current version support timing characterization and power characterization of combinational cells and sequential cells.
Multithread supported. All of the indexes are simulated in parallel.

## More better one?
Maybe LibreCell is better than libretto for characterization (lctime). LibreCell also support layout generation (lclayout). I have not tried yet.
https://codeberg.org/librecell

Maybe CharLib is better than libretto for characterization. Why we can find some similarities in the code and data structure...
https://github.com/stineje/CharLib/tree/main

## Back to libretto. Requirements
(1) Simulator. We assume ngspice
(2) Pandox, if you convert datasheet to PDF

## How to use
Use Makefile to speficy the target.
```Makefile
PROCESS_NAME := OSU350
```
Use make command to run libretto and pandoc. GEN_CMD in Makefile generate .cmd file and run libretto.
```sh libretto_make.sh
make
```

We can manually prepare .cmd file. Then type 
```sh libretto.sh
python3 libretto.py -b [.cmd file]
```

## How to prepare .cmd file
.cmd file composes three blocks.
(1) common settings for library
(2) common settings for cell
(3) individual settings for cell

### common settings for library
Define common settings for target library.
(called **set command**)
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| set_lib_name | OSU035 | library name |
| set_dotlib_name | OSU035.lib | .lib file name |
| set_verilog_name | OSU035.v | .v file name |
| set_cell_name_suffix | OSU035_ | cell name suffix (option) |
| set_cell_name_prefix | \_V1 | cell name prefix (option) |
| set_voltage_unit | V | voltage unit |
| set_capacitance_unit | pF | capacitance unit |
| set_resistance_unit | Ohm | resistance unit |
| set_current_unit | mA | current unit |
| set_leakage_power_unit | pW | power unit | 
| set_time_unit | ns | time unit |
| set_vdd_name | VDD | vdd name, used to detect vdd |
| set_vss_name | VSS | vss name, used to detect vss |
| set_pwell_name | VPW | pwell name, used to detect pwell (option)|
| set_nwell_name | VNW | nwell name, used to detect nwell (option)|

### common characterization conditions
Define common settings for logic cells.
(called **set command**)
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| set_process | typ | define process condition (written into .lib) | 
| set_temperature | 25 | simulation temperature  (written into .lib) |
| set_vdd_voltage | 3.5 | simulation vdd voltage (unit in set_voltage_unit)|
| set_vss_voltage | 0 |  simulation vss voltage (unit in set_voltage_unit) |
| set_pwell_voltage | 0 |  simulation pwell voltage (unit in set_voltage_unit) |
| set_nwell_voltage | 3.5 |  simulation nwell voltage (unit in set_voltage_unit) |
| set_logic_threshold_high | 0.8 | logic threshold for slew table (ratio: 0~1) |
| set_logic_threshold_low | 0.2 | logic threshold for slew table (ratio: 0~1) |
| set_logic_high_to_low_threshold | 0.5 | logic threshold for delay table (ratio: 0~1) |
| set_logic_low_to_high_threshold | 0.5 | logic threshold for delay table (ratio: 0~1) |
| set_energy_meas_low_threshold | 0.01 | threshold to define voltage low for energy calculation (ratio:0~1) |
| set_energy_meas_high_threshold | 0.99 | threshold to define voltage high for energy calculation (ratio:0~1) |
| set_energy_meas_time_extent | 4 | simulation time extension for energy calculation target large output slew (real val.) |
| set_operating_conditions | PVT_3P5V_25C | define operation condition (written into .lib) |
| set_slope | slope_name {0.01 0.02 ...} | set of slope_name and its index (unit in set_time_unit) |
| set_load | load_name {0.01 0.02 ...} | set of load_name and its index (unit in set_capacitance_unit)|

### common characterization setting
Define common settings for logic cells.
(called **set command**)
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| set_work_dir | work | simulation working directory |
| set_tmp_dir | _temp_dir_ | temporal dir for dotlib generation |
| set_tmp_file | _temp_file_ | temporal file for dotlib generation |
| set_simulator | /usr/local/bin/ngspice | binary for ngspice | 
| set_run_sim | true | true: clean working directory and run simulation (default), false: reuse previous simulation result for .lib creation|
| set_mt_sim | true | true: multithread simulation, all of the indexes are parallely simulated. false: single thread simulation | 
| set_sim_nice | value | specify nice value for simulator | 
| set_compress_result | true | true: compress simulator log | 
| set_supress_message | true | true: supress message. false: print message | 
| set_supress_sim_message | true | true: supress simulation message. false: print message | 
| set_supress_debug_message | true | true: supress debug message. false: print debug message | 


If common characterization commands are done, use **initialize command**
to initialize characterizor.
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| initialize | n/a | initialize characteizer | 

### individual characterization commands
Define individual settings for cells.
(called **add command**)
Except **add_cell** command, other **add command** requires one argument.
**add_cell** command requires several arguments with option.

**add command** block should be start from **add_cell** command,
**characterize**and **export** commands finalize the 
simulation output into .lib and .v.
If another **add command** is applied before running
the **characterize** and **export** commands, latest 
**add command** overwrite the previous setting.

Combinational cells and sequential cells requires different 
**add command**. 

(1) **add command** for combinational cells

**add_cell** for combinational cells
(**add_cell** command should be one-line)
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| add_cell |  | add cell for characterize | 
| -n cell_name | -n NAND2_1X | cell name in netlist|
| -l logic_def. | -l NAND2 | logic of target cell (\*) |
| -i inport | -i A B | inport list |
| -o outport | -o YB | outport list |
| -f verilog_func| YB = !(A\|B) | verilog function | 

Supported logic functions (\*) are listed as follow,
(Dec. 2021)
| logic def |  Description |
|:-----------|:------------|
| INV | 1-input 1-output inverter | 
| BUF | 1-input 1-output inverter | 
| AND2 | 2-input 1-output AND | 
| AND3 | 3-input 1-output AND | 
| AND4 | 4-input 1-output AND | 
| OR2 | 2-input 1-output OR | 
| OR3 | 3-input 1-output OR | 
| OR4 | 4-input 1-output OR | 
| NAND2 | 2-input 1-output NAND | 
| NAND3 | 3-input 1-output NAND | 
| NAND4 | 4-input 1-output NAND | 
| NOR2 | 2-input 1-output NOR | 
| NOR3 | 3-input 1-output NOR | 
| NOR4 | 4-input 1-output NOR | 
| XOR2 | 2-input 1-output XOR | 
| XNOR2 | 2-input 1-output XNOR | 
| SEL2 | 2-input 1-select 1-output selector | 

Other **add command**(s) for combinational cells
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| add_slope | slope_name | specify one slope_name defined by set_slope | 
| add_load  | load_name  | specify one load_name defined by set_load | 
| add_area  | 1 | area (real val, no unit) | 
| add_netlist | NETLIST/INV_1X.spi | location of netlist | 
| add_model | NETLIST/model.sp | location of model file (include simulation options) | 
| add_simulation_timestep | real val/auto | simulation timestep. If **auto slope_name** is selected then simulator automatically define timestep from min. slope | 

**characterize** and **export** commands
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| characterize | n/a | run characterization |
| export| n/a | export data into .lib and .v| 

(2) **add command** for sequential cells
**add_cell** for sequential cells
(**add_cell** command shoul be one-line)
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| add_cell |  | add cell for characterize | 
| -n cell_name | -n DFF_ARAS_1X | cell name in netlist|
| -l logic_def. | -l DFF_PCPU_NRNS | logic of target cell (\*) |
| -i inport | -i DATA | inport |
| -c clock port | -c CLK | clock port |
| -s set inport | -s NSET | set port (optional) |
| -r reset inport | -r NRST | reset port (optional) |
| -o outport | -o Q | outport |
| -q storage | -q IQ IQN | storage elements |
| -f func| Q=IQ QN=IQN | operation function | 

Supported sequential functions (\*) are listed as follow,
(Dec. 2021)
| logic def |  Description |
|:-----------|:------------|
| DFF_PCPU | D-Flip-Flop with pos-edge clock and positive unate output | 
| DFF_PCNU | D-Flip-Flop with pos-edge clock and negative unate output | 
| DFF_NCPU | D-Flip-Flop with neg-edge clock and positive unate output | 
| DFF_NCNU | D-Flip-Flop with neg-edge clock and negative unate output | 
| DFF_PCPU_NR | D-Flip-Flop with pos-edge clock, positive unate output, async. neg-edge reset | 
| DFF_PCPU_NRNS | D-Flip-Flop with pos-edge clock, positive unate output, async. neg-edge reset, async. neg-edge set | 

Other **add command**(s) for sequential cells
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| add_slope | slope_name | specify one slope_name defined by set_slope | 
| add_load  | load_name  | specify one load_name defined by set_load | 
| add_area  | 1  | area (real val, no unit) | 
| add_netlist | NETLIST/DFF_ARAS_1X.spi | location of netlist | 
| add_model | NETLIST/model.sp | location of model file (include simulation options) | 
| add_clock_slope | real val/auto | slope for clock. If **auto slope_name** is selected then simulator automatically select min. slope of slope_name |
| add_simulation_timestep | real val/auto | simulation timestep. If **auto slope_name** is selected then simulator automatically define timestep from min. slope of slope_name | 
| add_simulation_setup_auto | n/a | automatically set setup simulation time (lowest, highest, timestep) |
| add_simulation_setup_lowest | -10 | manually set lowest time for setup simulation (real val, unit in set_time_unit) |
| add_simulation_setup_highest | 16 | manually set highst time for setup simulation (real val, unit in set_time_unit) |
| add_simulation_setup_timestep | 5 | manually set timestep for setup simulation (real val, unit in set_time_unit) |
| add_simulation_hold_auto | n/a | automatically set hold simulation time (lowest, highest, timestep) |
| add_simulation_hold_lowest | -10 | manually set lowest time for hold simulation (real val, unit in set_time_unit) |
| add_simulation_hold_highest | 16 | manually set highst time for hold simulation (real val, unit in set_time_unit) |
| add_simulation_hold_timestep | 5 | manually set timestep for hold simulation (real val, unit in set_time_unit) |

**characterize**, **export** and **compress** commands
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| characterize | n/a | run characterization |
| export | n/a | export data into .lib and .v| 
| compress | n/a | compress generated spice file into tgz (note: not reused for set_run_sim option)| 

### exit
use **exit** command to return into shell.
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| exit | n/a | exit |

### sample
```txt libretto.cmd
# common settings for library
set_lib_name         OSU350_5P0V_25C
set_dotlib_name      OSU350_5P0V_25C.lib
set_doc_name      OSU350_5P0V_25C.md
set_verilog_name     OSU350.v
set_cell_name_suffix OSU350_
set_cell_name_prefix _V1
set_voltage_unit V
set_capacitance_unit pF
set_resistance_unit Ohm
set_current_unit mA
set_leakage_power_unit pW 
set_energy_unit fJ 
set_time_unit ns
set_vdd_name VDD
set_vss_name VSS
set_pwell_name VPW
set_nwell_name VNW

# characterization conditions 
set_process 1.0
set_temperature 25.0
set_vdd_voltage 5.0
set_vss_voltage 0
set_pwell_voltage 0
set_nwell_voltage 5.0
set_logic_threshold_high 0.8
set_logic_threshold_low 0.2
set_logic_high_to_low_threshold 0.5
set_logic_low_to_high_threshold 0.5
set_work_dir work
set_tmp_file __tmp__
set_simulator ngspice 
set_run_sim true
set_mt_sim true
set_supress_message true
set_supress_sim_message true
set_supress_debug_message true
set_energy_meas_low_threshold 0.01
set_energy_meas_high_threshold 0.99
set_energy_meas_time_extent 10
set_operating_conditions TCCOM
set_slope slope1 {0.1 0.7} 
set_load  load1 {0.01 0.07} 
set_slope slope2 {0.1 0.7 4.9} 
set_load  load2 {0.01 0.07 0.49} 
# initialize workspace
initialize

## add circuit
add_cell -n INV_1X -l INV -i A -o YB -f YB=!A 
add_slope slope2 
add_load  load2  
add_area 1
add_netlist NETLIST/NETLIST_OSU350/INV_1X.spi
add_model spice_model/model_OSU350_25C_TT.sp
add_simulation_timestep auto slope2
characterize
export

## add circuit
add_flop -n DFF_1X -l DFF_PCPU -i DATA -c CLK -o Q -q Q QN -f Q=IQ QN=IQN 
add_slope slope1 
add_load  load1  
add_clock_slope auto slope1
add_area 1
add_netlist NETLIST/NETLIST_OSU350/DFF_1X.spi
add_model spice_model/model_OSU350_25C_TT.sp
add_simulation_timestep auto slope1
add_simulation_setup_auto slope1
add_simulation_hold_auto slope1
characterize
export
exit

exit
```

## Known issues (future works)
1. Support more logics
* Combinationals: multi-output cells
* Sequentials: latches, scans
2. Verilog generation for timing simulation
3. Tristates
4. Multiple voltage for IOs and level shifters

## Done
1. Speed up: Use multithreads (23Jun)
2. Documentation support (23Jun)
3. Support multiple loads slopes (24May)
