import argparse, re, os, shutil, subprocess

class MyLibrarySetting:
	def __init__ (self):
		self.isexport = 0
		self.delay_model = "table_lookup"

	def set_lib_name(self, line="tmp"):
		tmp_array = line.split()
		self.lib_name = tmp_array[1] 
		print(tmp_array[1])
		
	def set_dotlib_name(self, line="tmp"):
		tmp_array = line.split()
		self.dotlib_name = tmp_array[1] 
		print(tmp_array[1])
		
	def set_verilog_name(self, line="tmp"):
		tmp_array = line.split()
		self.verilog_name = tmp_array[1] 
		print(tmp_array[1])
		
	def set_cell_name_suffix(self, line="tmp"):
		tmp_array = line.split()
		self.cell_name_suffix = tmp_array[1] 
		print(tmp_array[1])

	def set_cell_name_prefix(self, line="tmp"):
		tmp_array = line.split()
		self.cell_name_prefix = tmp_array[1] 
		print(tmp_array[1])

	def set_voltage_unit(self, line="tmp"):
		tmp_array = line.split()
		print(tmp_array[1])
		if(tmp_array[1].upper() == 'V'):
			self.voltage_unit = "V"	
			self.voltage_mag = 1	
		elif(tmp_array[1].upper() == 'MV'):
			self.voltage_unit = "mV"	
			self.voltage_mag = 1e-3	
		else:
			my_error("illegal unit for set_voltage_unit")

	def set_capacitance_unit(self, line="tmp"):
		tmp_array = line.split()
		print(tmp_array[1])
		if(tmp_array[1].upper() == 'PF'):
			self.capacitance_unit = "pF"	
			self.capacitance_mag = 1e-15	
		elif(tmp_array[1].upper() == 'NF'):
			self.capacitance_unit = "nF"	
			self.capacitance_mag = 1e-12	
		else:
			my_error("illegal unit for set_capacitance_unit")

	def set_resistance_unit(self, line="tmp"):
		tmp_array = line.split()
		print(tmp_array[1])
		if(tmp_array[1].upper() == 'OHM'):
			self.resistance_unit = "Ohm"	
			self.resistance_mag = 1	
		elif(tmp_array[1].upper() == 'KOHM'):
			self.resistance_unit = "kOhm"	
			self.resistance_mag = 1e3	
		else:
			my_error("illegal unit for set_resistance_unit")

	def set_time_unit(self, line="tmp"):
		tmp_array = line.split()
		print(tmp_array[1])
		if(tmp_array[1].upper() == 'PS'):
			self.time_unit = "ps"	
			self.time_mag = 1e-12	
		elif(tmp_array[1].upper() == 'NS'):
			self.time_unit = "ns"	
			self.time_mag = 1e-9	
		else:
			my_error("illegal unit for set_time_unit")

	def set_current_unit(self, line="tmp"):
		tmp_array = line.split()
		print(tmp_array[1])
		if(tmp_array[1].upper() == 'A'):
			self.current_unit = "A"	
			self.current_mag = 1	
		elif(tmp_array[1].upper() == 'MA'):
			self.current_unit = "mA"	
			self.current_mag = 1e-3	
		elif(tmp_array[1].upper() == 'UA'):
			self.current_unit = "uA"	
			self.current_mag = 1e-6	
		else:
			my_error("illegal unit for set_current_unit")

	def set_leakage_power_unit(self, line="tmp"):
		tmp_array = line.split()
		print(tmp_array[1])
		if(tmp_array[1].upper() == 'PW'):
			self.leakage_power_unit = "pW"	
			self.leakage_power_mag = 1e-12	
		elif(tmp_array[1].upper() == 'NW'):
			self.leakage_power_unit = "nW"	
			self.leakage_power_mag = 1e-9	
		else:
			my_error("illegal unit for set_leakage_power_unit")

	def set_vdd_name(self, line="tmp"):
		tmp_array = line.split()
		self.vdd_name = tmp_array[1] 
		print(tmp_array[1])

	def set_vss_name(self, line="tmp"):
		tmp_array = line.split()
		self.vss_name = tmp_array[1] 
		print(tmp_array[1])

	def set_pwell_name(self, line="tmp"):
		tmp_array = line.split()
		self.pwell_name = tmp_array[1] 
		print(tmp_array[1])

	def set_nwell_name(self, line="tmp"):
		tmp_array = line.split()
		self.nwell_name = tmp_array[1] 
		print(tmp_array[1])

	def set_process(self, line="tmp"):
		tmp_array = line.split()
		self.process = tmp_array[1] 
		print(tmp_array[1])

	def set_temperature(self, line="tmp"):
		tmp_array = line.split()
		self.temperature = tmp_array[1] 
		print(tmp_array[1])

	def set_vdd_voltage(self, line="tmp"):
		tmp_array = line.split()
		self.vdd_voltage = tmp_array[1] 
		print(self.vdd_voltage)

	def set_vss_voltage(self, line="tmp"):
		tmp_array = line.split()
		self.vss_voltage = tmp_array[1] 
		print(tmp_array[1])

	def set_nwell_voltage(self, line="tmp"):
		tmp_array = line.split()
		self.nwell_voltage = tmp_array[1] 
		print(tmp_array[1])

	def set_pwell_voltage(self, line="tmp"):
		tmp_array = line.split()
		self.pwell_voltage = tmp_array[1] 
		print(tmp_array[1])

	def set_logic_threshold_high(self, line="tmp"):
		tmp_array = line.split()
		self.logic_threshold_high = tmp_array[1] 
		print(tmp_array[1])

	def set_logic_threshold_low(self, line="tmp"):
		tmp_array = line.split()
		self.logic_threshold_low = tmp_array[1] 
		print(tmp_array[1])

	def set_logic_high_to_low_threshold(self, line="tmp"):
		tmp_array = line.split()
		self.logic_high_to_low_threshold = tmp_array[1] 
		print(tmp_array[1])

	def set_logic_low_to_high_threshold(self, line="tmp"):
		tmp_array = line.split()
		self.logic_low_to_high_threshold = tmp_array[1] 
		print(tmp_array[1])

	def set_work_dir(self, line="tmp"):
		tmp_array = line.split()
		self.work_dir = tmp_array[1] 
		print(tmp_array[1])

	def set_simulator(self, line="tmp"):
		tmp_array = line.split()
		self.simulator = tmp_array[1] 
		print(tmp_array[1])

	def set_energy_meas_low_threshold(self, line="tmp"):
		tmp_array = line.split()
		self.energy_meas_low_threshold = tmp_array[1] 
		print(tmp_array[1])

	def set_energy_meas_high_threshold(self, line="tmp"):
		tmp_array = line.split()
		self.energy_meas_high_threshold = tmp_array[1] 
		print(tmp_array[1])

	def set_energy_meas_time_extent(self, line="tmp"):
		tmp_array = line.split()
		self.energy_meas_time_extent = tmp_array[1] 
		print(tmp_array[1])
	
	def set_operating_conditions(self, line="tmp"):
		tmp_array = line.split()
		self.operating_conditions = tmp_array[1] 
		print(tmp_array[1])
	
	def set_exported(self):
		self.isexport = 1 
