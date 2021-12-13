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
### common settings for library
Define common settings for target library.
(called **set command**)
| Command | Argument example | Description |
|:-----------|------------:|:------------:|
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
|:-----------|------------:|:------------:|
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
