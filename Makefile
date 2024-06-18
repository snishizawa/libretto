#===========================================================
# setting/gen_cmd_<PROCESS_NAME>.py is command generator for libretto.py
#
#   input:  setting/gen_cmd_<PROCESS_NAME>.py  <-- set process & spice model .
#   output: cmd/libretto.cmd
#
# libretto.py is spice simulator with ngspice/hspice.
# 
#   input:  cmd/libretto.cmd
#           NETLIST/NETLIST_<PROCESS_NAME>/*.spi model.sp
#   output: <PROCESS_NAME>.lib <PROCESS_NAME>.v <PROCESS_NAME>.md/pdf
# 
#===========================================================
# 00: prepare std-cell (option)
#     --> create & edit MOS model in NETLIST/replace_with_<PROCESS_NAME>.sh
#     --> generate spi file from NETLIST/NETLIST_BASE to NETLIST/NETLIST_<PROCESS_NAME> by NETLIST/replace_with_<PROCESS_NAME>.sh
#
# 01: select std-cell, spice model,,,,
#     --> create & edit setting/gen_cmd_<PROCESS_NAME>.py
#     --> prapare MOS model in spice_model/model_<PROCESS_NAME>_<TEMP>.sp
#     --> generate cmd/libretto.cmd by setting/gen_cmd_<PROCESS_NAME>.py
#
# 02: characterization
#     --> make PROCESS_NAME=<PROCESS_NAME> CONDITION=<CONDITION>
#     --> output <PROCESS_NAME>.v .lib .md .pdf
#===========================================================

.SUFFIXES:
.SUFFIXES: .cmd .md .sp

PROCESS_NAME := OSU350
#PROCESS_NAME := SKY130
#PROCESS_NAME := ROHM180
#PROCESS_NAME := GF180
PROCESS      := 1.0
CONDITION    := TCCOM

LIBRETTO	= script/libretto.py
GEN_CMD		= $(PROCESS_NAME)/gen_cmd_$(PROCESS_NAME).py

CMD_FILE	= cmd/libretto.cmd



#------------------------------------------------
ifeq ($(PROCESS_NAME),OSU350)
  ifeq ($(CONDITION),BCCOM)
  	VDD  = 5.5
  	SPEED= FF
    TEMP =-40
  endif
  ifeq ($(CONDITION),TCCOM)
    VDD  = 5.0
  	SPEED= TT
    TEMP = 25
  endif
  ifeq ($(CONDITION),WCCOM)
    VDD  = 4.5
  	SPEED= SS
    TEMP =125
  endif
endif
ifeq ($(PROCESS_NAME),SKY130)
  ifeq ($(CONDITION),TCCOM)
  	VDD  = 1.5
  	SPEED= TT
    TEMP = 25
  endif
endif
ifeq ($(PROCESS_NAME),ROHM180)
  ifeq ($(CONDITION),TCCOM)
  	VDD  = 1.8
  	SPEED= TT
    TEMP = 25
  endif
endif


VDD_STR      := $(subst .,P,$(VDD))V
TEMP_STR     := $(subst -,M,$(TEMP))C


LIB_NAME    := $(PROCESS_NAME)_$(VDD_STR)_$(TEMP_STR)
PATH_MODEL  := $(PROCESS_NAME)/MODEL/model_$(PROCESS_NAME)_$(TEMP_STR)_$(SPEED).sp
PATH_CELL   := $(PROCESS_NAME)/NETLIST
LIB         := $(LIB_NAME).lib 
MD          := $(LIB_NAME).md
PDF         := $(LIB_NAME).pdf

#========================================================================
.PHONY: all

all:$(LIB) $(PDF)
	mv $(LIB_NAME).* $(PROCESS_NAME).v $(PROCESS_NAME)/

#all:
#	make prep
#	python3 $(GEN_CMD) --vdd $(VDD) --temp  $(TEMP) --process $(PROCESS) --condition $(CONDITION) \
#		--p_name $(PROCESS_NAME) --lib_name $(LIB_NAME)  \
#		--path_model $(PATH_MODEL) --path_cell $(PATH_CELL);
#	time python3 $(LIBRETTO) -b $(CMD_FILE);


$(PDF):$(LIB) $(MD) 
	/bin/pandoc $(MD) -o $@ -V documentclass=ltjarticle --pdf-engine=lualatex -V geometry:margin=1in -N --toc -V secnumdepth=4;

$(LIB):prep $(MODEL) 
	python3 $(GEN_CMD) --vdd $(VDD) --temp  $(TEMP) --process $(PROCESS) --condition $(CONDITION) \
		--p_name $(PROCESS_NAME) --lib_name $(LIB_NAME)  \
		--path_model $(PATH_MODEL) --path_cell $(PATH_CELL);

	time python3 $(LIBRETTO) -b $(CMD_FILE);


%.pdf:%.md

prep:
	\rm -rf work cmd/*;\
	mkdir work;
	mkdir -p cmd;
	mkdir -p lib;

lc:
	lc_shell -f tcl/run_lc.tcl 

clean:
	\rm -rf work log.txt  cmd/* script/__pycache__  *.db *.lib *.v *.log *.md *.pdf lib

test:
	echo "OK"

