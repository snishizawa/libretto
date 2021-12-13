# libretto
## Introduction
An open cell library characterization.
Current version support timing characterization of combinational cells and sequential cells.

Support for power characterization is TBA.

## How to use
Prepare .cmd file 
Type 
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
| set_resistance_unit | Ohm | resitannce unit |
| set_current_unit | mA | current unit |
| set_leakage_power_unit | pW | power unit | 
| set_time_unit | ns | time unit |
| set_vdd_name | VDD | vdd name, used to detect vdd |
| set_vss_name | VSS | vss name, used to detect vss |
| set_pwell_name | VPW | pwell name (option), used to detect pwell |
| set_nwell_name | VNW |  (option), used to detect nwell |


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
| set_work_dir | work | simulation working directory |
| set_simulator | /usr/local/bin/ngspice | binary for ngspice | 
| set_energy_meas_low_threshold | 0.01 | threshold to define voltage low for energy calculation (ratio:0~1) |
| set_energy_meas_high_threshold | 0.99 | threshold to define voltage high for energy calculation (ratio:0~1) |
| set_energy_meas_time_extent | 4 | simulation time extension for energy calculation target large output slew (real val.) |
| set_operating_conditions | PVT_3P5V_25C | define operation condition (written into .lib) |

If common characterization commands are done, use **initialize command**
to initialize characterizor.
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| initialize | n/a | initialize characteizer | 

### individual characterization commands
Define individual settings for cells.
(called **add command**)
Except **add_cell** command, **add_command** requires one argument.
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
(**add_cell** command shoul be one-line)
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| add_cell |  | add cell for characterize | 
| -n cell_name | -n NAND2_1X | cell name in netlist|
| -l logic_def. | -l NAND2 | logic of target cell (\*) |
| -i inport | -i A B | inport list |
| -o outport | -o YB | outport list |
| -f verilog_func| YB = !(A\|B) | verilog function | 

Supported logic cells (\*) are listed as follow,
| logic def |  Description |
|:-----------|:------------|
| INV | 1-input 1-output inverter | 
| NAND2 | 2-input 1-output NAND | 
| NAND3 | 3-input 1-output NAND | 
| NAND4 | 4-input 1-output NAND | 
| NOR2 | 2-input 1-output NOR | 
| NOR3 | 3-input 1-output NOR | 
| NOR4 | 4-input 1-output NOR | 
| XOR2 | 2-input 1-output XOR | 
| XNOR2 | 2-input 1-output XNOR | 
| SEL2 | 2-input 1-select 1-output selector | 

Other **add cell** for combinational cells
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| add_slope | {1 4 16 64} | slope index (unit in set_time_unit) | 
| add_load  | {1 4 16 64}  | slope index (unit in set_capacitance_unit) | 
| add_netlist | NETLIST/INV_1X.spi | location of netlist | 
| add_model | NETLIST/model.sp | location of model file (include simulation options) | 
| add_simulation_timestep | real val/auto | simulation timestep. If **auto** is selected then simulator automatically define timestep from min. slope | 

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

Supported logic cells (\*) are listed as follow,
| logic def |  Description |
|:-----------|:------------|
| DFF_PCPU | D-Flip-Flop with pos-edge clock and positive unate output | 
| DFF_PCPN | D-Flip-Flop with pos-edge clock and negative unate output | 
| DFF_NCPU | D-Flip-Flop with neg-edge clock and positive unate output | 
| DFF_NCPN | D-Flip-Flop with neg-edge clock and negative unate output | 
| DFF_PCPU_NR | D-Flip-Flop with pos-edge clock, positive unate output, async. neg-edge reset | 
| DFF_PCPU_NRNS | D-Flip-Flop with pos-edge clock, positive unate output, async. neg-edge reset, neg-edge set | 

Other **add command** for sequential cells
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| add_slope | {1 4 16 64} | slope index (unit in set_time_unit) | 
| add_load  | {1 4 16 64}  | slope index (unit in set_capacitance_unit) | 
| add_netlist | NETLIST/DFF_ARAS_1X.spi | location of netlist | 
| add_model | NETLIST/model.sp | location of model file (include simulation options) | 
| add_simulation_timestep | real val/auto | simulation timestep. If **auto** is selected then simulator automatically define timestep from min. slope | 
| add_simulation_setup_auto | n/a | automatically set setup simulation time (lowest, highest, timestep) |
| add_simulation_setup_lowest | -10 | manually set lowest time for setup simulation (real val, unit in set_time_unit) |
| add_simulation_setup_highest | 16 | manually set highst time for setup simulation (real val, unit in set_time_unit) |
| add_simulation_setup_timestep | 5 | manually set timestep for setup simulation (real val, unit in set_time_unit) |
| add_simulation_hold_auto | n/a | automatically set setup simulation time (lowest, highest, timestep) |
| add_simulation_hold_lowest | -10 | manually set lowest time for hold simulation (real val, unit in set_time_unit) |
| add_simulation_hold_highest | 16 | manually set highst time for hold simulation (real val, unit in set_time_unit) |
| add_simulation_hold_timestep | 5 | manually set timestep for hold simulation (real val, unit in set_time_unit) |

**characterize** and **export** commands
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| characterize | n/a | run characterization |
| export| n/a | export data into .lib and .v| 

### exit
use **exit** command to return into shell.
| Command | Argument example | Description |
|:-----------|------------:|:------------|
| exit | n/a | exit |
