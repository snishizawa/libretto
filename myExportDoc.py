import argparse, re, os, shutil, subprocess, sys, inspect 
from myFunc import my_exit

def exportDoc(targetLib, targetCell, harnessList2):
    if(targetLib.isexport2doc == 0):
        exportLib2doc(targetLib, targetCell)

    ## export comb. logic
    if((targetLib.isexport2doc == 1) and (targetCell.isexport2doc == 0) and (targetCell.isflop == 0)):
        exportHarness2doc(targetLib, targetCell, harnessList2)
    ## export seq. logic
    elif((targetLib.isexport2doc == 1) and (targetCell.isexport2doc == 0) and (targetCell.isflop == 1)):
        exportHarnessFlop2doc(targetLib, targetCell, harnessList2)

## export library definition to .lib
def exportLib2doc(targetLib, targetCell):
    print(targetLib.doc_name)
    with open(targetLib.doc_name, 'w') as f:
        outlines = []
        ## general settings
        outlines.append("# Library settings \n")
        outlines.append("| lib. name | delay model |\n")
        outlines.append("|----|----|\n")
        outlines.append("| "+targetLib.lib_name+" | "+targetLib.delay_model+" |\n")
        outlines.append("\n")
        outlines.append("## Units \n")
        outlines.append("| cap | volt | cur | leak | time | res |\n")
        outlines.append("|----|----|----|----|----|----|\n")
        outlines.append("| "+targetLib.capacitance_unit+" | "+targetLib.voltage_unit+"  | "+targetLib.current_unit+" | "+targetLib.leakage_power_unit+" | "+targetLib.time_unit+" | "+targetLib.resistance_unit+" |\n")
        outlines.append("\n")
        outlines.append("## Voltage terminals \n")
        outlines.append("| vdd | vss | gnd | pwell | nwell |\n")
        outlines.append("|----|----|----|----|----|\n")
        outlines.append("| "+targetLib.vdd_name+" | "+targetLib.vss_name+"  | gnd | "+targetLib.pwell_name+" | "+targetLib.nwell_name+" |\n")
        outlines.append("\n")
        outlines.append("## Operating conditions \n")
        outlines.append("| operationg cond. | temperature | voltage  |\n")
        outlines.append("|----|----|----|\n")
        outlines.append("| "+targetLib.operating_conditions+" | "+str(targetLib.temperature)+" | "+str(targetLib.vdd_voltage)+" |\n")
        outlines.append("\n")
        outlines.append("## Logic threshold \n")
        outlines.append("| input rise | input fall | output rise | output fall |\n")
        outlines.append("|----|----|----|----|\n")
        outlines.append("| "+str(targetLib.logic_low_to_high_threshold*100)+" | "+str(targetLib.logic_high_to_low_threshold*100)+" | "+str(targetLib.logic_low_to_high_threshold*100)+" | "+str(targetLib.logic_high_to_low_threshold*100)+" |\n")
        outlines.append("\n")
        #outlines.append("# End library settings \n")
        outlines.append("\\newpage \n")    #-- command for luatext
        outlines.append("# Cell settings \n")
        f.writelines(outlines)
    f.close()
    targetLib.set_exported2doc()

## export harness data to .doc
def exportHarness2doc(targetLib, targetCell, harnessList2):
    with open(targetLib.doc_name, 'a') as f:
        outlines = []
        outlines.append("## Cell : "+targetCell.cell+" \n")
        outlines.append("### Basics\n")
        outlines.append("| name | type | code | area | leak |\n")
        outlines.append("|----|----|----|----|----|\n")
        outlines.append("| "+targetCell.cell+" | Combinational | "+targetCell.logic+" | "+str(targetCell.area)+" | "+str(harnessList2[0][0].pleak)+" |\n")
        outlines.append("\n")

## select one input pin from pinlist(target_inports) 
        for target_inport in targetCell.inports:
            index1 = targetCell.inports.index(target_inport) 
            outlines.append("### Input pin : "+target_inport+"\n") ## input pin start
            outlines.append("| direction | related pwr pin | related gnd pin | max trans | cap. |\n")
            outlines.append("|----|----|----|----|----|\n")
            outlines.append("| input | "+targetLib.vdd_name+" | "+targetLib.vss_name+" | "+str(targetCell.slope[-1])+" | "+str(targetCell.cins[index1])+" |\n")
            outlines.append("\n")

            
## select one output pin from pinlist(target_outports) 
        for target_outport in targetCell.outports:
            index1 = targetCell.outports.index(target_outport) 
            outlines.append("### Output pin : "+target_outport+"\n") ## output pin start
            outlines.append("| direction | func | max cap | leak | \n")
            outlines.append("|----|----|----|----|\n")
            #outlines.append("| output | "+targetCell.functions[index1]+" | "+str(targetCell.load[-1])+" | "+str(harnessList2[0][0].pleak)+" |\n")
            outlines.append("| output | "+targetCell.functions[index1].replace('|','\|')+" | "+str(targetCell.load[-1])+" | "+str(harnessList2[0][0].pleak)+" |\n")

            outlines.append("\n")

            ## timing / power
            for target_inport in targetCell.inports:
                index2 = targetCell.inports.index(target_inport)

                outlines.append("#### related pin : " + target_inport + "\n")
                
                outlines.append("| related pin | func | max cap |\n")
                outlines.append("|----|----|----|\n")
                #outlines.append("| output | "+targetCell.functions[index1].replace('|','\|')+" | "+str(targetCell.load[-1])+" |\n")
                outlines.append("|" + target_inport + "|"+targetCell.functions[index1].replace('|','\|')+" | "+str(targetCell.load[-1])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | prop min. | prop center | prop max |\n")
                outlines.append("|----|----|----|----|\n")
                #outlines.append("| rise | "+str(harnessList2[index1][index2*2].lut_prop_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_prop_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_prop_mintomax[2])+" |\n")
                #outlines.append("| fall | "+str(harnessList2[index1][index2*2+1].lut_prop_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_prop_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_prop_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2].direction_prop   + "|"+str(harnessList2[index1][index2*2].lut_prop_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_prop_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_prop_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+1].direction_prop + "|"+str(harnessList2[index1][index2*2+1].lut_prop_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_prop_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_prop_mintomax[2])+" |\n")

                outlines.append("\n")
                
                outlines.append("| direction | tran min. | tran center | tran max |\n")
                outlines.append("|----|----|----|----|\n")
                
                #outlines.append("| rise | "+str(harnessList2[index1][index2*2].lut_tran_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_tran_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_tran_mintomax[2])+" |\n")
                #outlines.append("| fall | "+str(harnessList2[index1][index2*2+1].lut_tran_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_tran_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_tran_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2].direction_tran   + "|" +str(harnessList2[index1][index2*2].lut_tran_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_tran_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_tran_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+1].direction_tran + "|"+str(harnessList2[index1][index2*2+1].lut_tran_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_tran_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_tran_mintomax[2])+" |\n")

                outlines.append("\n")


                outlines.append("| direction | eintl min. | eintl center | eintl max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[2])+" |\n")
                #outlines.append("| fall | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2].direction_power   + "|"+str(harnessList2[index1][index2*2].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+1].direction_power + "|"+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[2])+" |\n")

                outlines.append("\n")
                
                #-- outlines.append("| direction | ein min. | ein center | ein max |\n")
                #-- outlines.append("|----|----|----|----|\n")
                #-- 
                #-- #outlines.append("| rise | "+str(harnessList2[index1][index2*2].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_ein_mintomax[2])+" |\n")
                #-- #outlines.append("| fall | "+str(harnessList2[index1][index2*2+1].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_ein_mintomax[2])+" |\n")
                #-- outlines.append("|" + harnessList2[index1][index2*2].direction_power   +"|"+str(harnessList2[index1][index2*2].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[2])+" |\n")
                #-- outlines.append("|" + harnessList2[index1][index2*2+1].direction_power +"|"+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[2])+" |\n")


                outlines.append("\n")
        outlines.append("\\newpage \n")
        f.writelines(outlines)
    f.close()
    targetCell.set_exported2doc()

## export harness data to doc
def exportHarnessFlop2doc(targetLib, targetCell, harnessList2):
    with open(targetLib.doc_name, 'a') as f:
        outlines = []
        outlines.append("## Cell : "+targetCell.cell+" \n")
        outlines.append("### Basics\n")
        outlines.append("| name | type | code | area | leak |\n")
        outlines.append("|----|----|----|----|----|\n")
        outlines.append("| "+str(targetCell.cell)+" | Sequential | "+targetCell.logic+" | "+str(targetCell.area)+" | "+str(harnessList2[0][0].pleak)+" |\n")
        outlines.append("\n")

## (1) clock 
        if targetCell.clock is not None:
            target_inport = targetCell.clock
            index1 = 0 
            outlines.append("### Clock pin : "+target_inport+"\n") ## input pin start
            outlines.append("| direction | related pwr pin | related gnd pin | max trans | cap. |\n")
            outlines.append("|----|----|----|----|----|\n")
            #outlines.append("| input | "+targetLib.vdd_name+" | "+targetLib.vss_name+" | "+str(targetCell.slope[-1])+" | "+str(targetCell.cins[index1])+" |\n")
            outlines.append("| input | "+targetLib.vdd_name+" | "+targetLib.vss_name+" | "+str(targetCell.slope[-1])+" | "+str(targetCell.cclks[index1])+" |\n")
            outlines.append("\n")

        ## (2) setup/hold for clock
        for target_inport in targetCell.inports:
            for target_outport in targetCell.outports:
              index1 = targetCell.outports.index(target_outport) 
              index2 = targetCell.inports.index(target_inport)
              if((harnessList2[index1][index2*2].timing_type_setup == "setup_rising") or (harnessList2[index1][index2*2].timing_type_setup == "setup_falling")):
                
                outlines.append("### Input pin : "+target_inport+"\n") ## input pin start
                outlines.append("| direction | related pwr pin | related gnd pin | max trans | cap. |\n")
                outlines.append("|----|----|----|----|----|\n")
                outlines.append("| input | "+targetLib.vdd_name+" | "+targetLib.vss_name+" | "+str(targetCell.slope[-1])+" | "+str(targetCell.cins[index1])+" |\n")
                outlines.append("\n")
                outlines.append("| direction | setup min. | setup center | setup max |\n")
                outlines.append("|----|----|----|----|\n")

                outlines.append("|" + harnessList2[index1][index2*2].timing_sense_setup + "|"+str(harnessList2[index1][index2*2].lut_setup_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_setup_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_setup_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+1].timing_sense_setup + "|"+str(harnessList2[index1][index2*2+1].lut_setup_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_setup_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_setup_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | hold min. | hold center | hold max |\n")
                outlines.append("|----|----|----|----|\n")

                outlines.append("|" + harnessList2[index1][index2*2].timing_sense_hold   + "|"+str(harnessList2[index1][index2*2].lut_hold_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_hold_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_hold_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+1].timing_sense_hold + "|"+str(harnessList2[index1][index2*2+1].lut_hold_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_hold_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_hold_mintomax[2])+" |\n")

                outlines.append("\n")
        
        ## (2.2) recovery/removal for reset
        for target_inport in targetCell.inports:
          for target_outport in targetCell.outports:
            if targetCell.reset is not None:
                target_reset = targetCell.reset
                index1 = targetCell.reset.index(target_reset) 
                index2 = targetCell.outports.index(target_outport) 
                index2_offset = 0
                index2_offset_max = 10
                while(index2_offset < index2_offset_max):
                    #targetLib.print_msg(harnessList2[index1][index2*2+index2_offset])
                    if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_reset"):
                        break
                    index2_offset += 1
                if(index2_offset == 10):
                    targetLib.print_error("Error: index2_offset exceed max. search number\n")

                outlines.append("### Input pin : "+target_reset+"\n") ## input pin start
                outlines.append("| direction | related pwr pin | related gnd pin | max trans | cap. |\n")
                outlines.append("|----|----|----|----|----|\n")
                outlines.append("| input | "+targetLib.vdd_name+" | "+targetLib.vss_name+" | "+str(targetCell.slope[-1])+" | "+str(targetCell.crsts[0])+" |\n")
                outlines.append("\n")
                outlines.append("| direction | recovery min. | recovery center | recovery max |\n")
                outlines.append("|----|----|----|----|\n")

                outlines.append("|" + harnessList2[index1][index2*2+index2_offset].timing_sense_reset_recov + "|"+str(harnessList2[index1][index2*2+index2_offset].lut_setup_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_setup_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_setup_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | removal min. | removal center | removal max |\n")
                outlines.append("|----|----|----|----|\n")

                outlines.append("|" + harnessList2[index1][index2*2+index2_offset].timing_sense_reset_remov   + "|"+str(harnessList2[index1][index2*2+index2_offset].lut_hold_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_hold_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_hold_mintomax[2])+" |\n")

                outlines.append("\n")


## (2.3) recovery/removal for set
        for target_inport in targetCell.inports:
          for target_outport in targetCell.outports:
            if targetCell.set is not None:
                target_set = targetCell.set
                index1 = targetCell.set.index(target_set) 
                index2 = targetCell.outports.index(target_outport) 
                index2_offset = 0
                index2_offset_max = 10
                while(index2_offset < index2_offset_max):
                    #targetLib.print_msg(harnessList2[index1][index2*2+index2_offset])
                    if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_set"):
                        break
                    index2_offset += 1
                if(index2_offset == 10):
                    targetLib.print_error("Error: index2_offset exceed max. search number\n")

                outlines.append("### Input pin : "+target_set+"\n") ## input pin start
                outlines.append("| direction | related pwr pin | related gnd pin | max trans | cap. |\n")
                outlines.append("|----|----|----|----|----|\n")
                outlines.append("| input | "+targetLib.vdd_name+" | "+targetLib.vss_name+" | "+str(targetCell.slope[-1])+" | "+str(targetCell.csets[0])+" |\n")
                outlines.append("\n")
                outlines.append("| direction | recovery min. | recovery center | recovery max |\n")
                outlines.append("|----|----|----|----|\n")

                outlines.append("|" + harnessList2[index1][index2*2+index2_offset].timing_sense_set_recov + "|"+str(harnessList2[index1][index2*2+index2_offset].lut_setup_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_setup_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_setup_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | removal min. | removal center | removal max |\n")
                outlines.append("|----|----|----|----|\n")

                outlines.append("|" + harnessList2[index1][index2*2+index2_offset].timing_sense_set_remov   + "|"+str(harnessList2[index1][index2*2+index2_offset].lut_hold_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_hold_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_hold_mintomax[2])+" |\n")

                outlines.append("\n")


                
## (3) output 
        for target_outport in targetCell.outports:
            index1 = targetCell.outports.index(target_outport) 
            outlines.append("### Output pin : "+target_outport+"\n") ## input pin start
            outlines.append("| direction | func | max cap | leak | \n")
            outlines.append("|----|----|----|----|\n")
            outlines.append("| output | "+targetCell.functions[index1].replace('|','\|')+" | "+str(targetCell.load[-1])+" | "+str(harnessList2[0][0].pleak)+" |\n")
            outlines.append("\n")

            ## (3-1) clock
            if targetCell.clock is not None:
                ## index2 is a base pointer for harness search
                ## index2_offset and index2_offset_max are used to 
                ## search harness from harnessList2 which contain "timing_type_set"
                index2 = targetCell.outports.index(target_outport) 
                index2_offset = 0
                index2_offset_max = 10
                while(index2_offset < index2_offset_max):
                    if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_setup"):
                        break
                    index2_offset += 1
                if(index2_offset == 10):
                    targetLib.print_error("Error: index2_offset exceed max. search number\n")

                outlines.append("#### related pin : " + targetCell.clock + "\n")

                outlines.append("| related pin | func | max cap |\n")
                outlines.append("|----|----|----|\n")
                outlines.append("| "+targetCell.clock+" | "+targetCell.functions[index1].replace('|','\|')+" | "+str(targetCell.load[-1])+" |\n")
                outlines.append("\n")
                outlines.append("| direction | prop min. | prop center | prop max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_mintomax[2])+" |\n")
                #outlines.append("| fall | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_prop_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_prop_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_prop_mintomax[2])+" |\n")
                outlines.append("|"+harnessList2[index1][index2*2+index2_offset].direction_prop+"|"+str(harnessList2[index1][index2*2+index2_offset].lut_prop_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_mintomax[1])  +" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_mintomax[2])+" |\n")
                outlines.append("|"+harnessList2[index1][index2*2+index2_offset+1].direction_prop+"|"+str(harnessList2[index1][index2*2+index2_offset+1].lut_prop_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset+1].lut_prop_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset+1].lut_prop_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | tran min. | tran center | tran max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_mintomax[2])+" |\n")
                #outlines.append("| fall | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_tran_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_tran_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_tran_mintomax[2])+" |\n")
                outlines.append("|"+harnessList2[index1][index2*2+index2_offset].direction_tran  +"|"+str(harnessList2[index1][index2*2+index2_offset].lut_tran_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_mintomax[2])+" |\n")
                outlines.append("|"+harnessList2[index1][index2*2+index2_offset+1].direction_tran+"|"+str(harnessList2[index1][index2*2+index2_offset+1].lut_tran_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset+1].lut_tran_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset+1].lut_tran_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | eintl min. | eintl center | eintl max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_eintl_mintomax[2])+" |\n")
                #outlines.append("| fall | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_eintl_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2].direction_power   + "|"+str(harnessList2[index1][index2*2].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+1].direction_power + "|"+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | ein min. | ein center | ein max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[2])+" |\n")
                #outlines.append("| fall | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1+index2_offset].lut_ein_mintomax[2])+" |\n")
                outlines.append("|" +harnessList2[index1][index2*2+index2_offset].direction_power   + "|"+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[2])+" |\n")
                #outlines.append("|" +harnessList2[index1][index2*2+index2_offset+1].direction_power + "|"+str(harnessList2[index1][index2*2+index2_offset+1].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset+1].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset+1].lut_ein_mintomax[2])+" |\n")

                outlines.append("\n")

            ## (2) reset
            if targetCell.reset is not None:
                ## Harness search for reset
                ## index2 is an base pointer for harness search
                ## index2_offset and index2_offset_max are used to 
                ## search harness from harnessList2 which contain "timing_type_set"
                index2 = targetCell.outports.index(target_outport) 
                index2_offset = 0
                index2_offset_max = 10
                while(index2_offset < index2_offset_max):
                    #targetLib.print_msg(harnessList2[index1][index2*2+index2_offset])
                    if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_reset"):
                        break
                    index2_offset += 1
                if(index2_offset == 10):
                    targetLib.print_error("Error: index2_offset exceed max. search number\n")

                outlines.append("#### related pin : " + targetCell.reset + "\n")
                
                outlines.append("| related pin | func | max cap |\n")
                outlines.append("|----|----|----|\n")
                outlines.append("| "+targetCell.reset+" | "+targetCell.functions[index1].replace('|','\|')+" | "+str(targetCell.load[-1])+" |\n")
                outlines.append("\n")
                outlines.append("| direction | prop min. | prop center | prop max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_reset_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_reset_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_reset_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+index2_offset].direction_reset_prop+   "|"+str(harnessList2[index1][index2*2+index2_offset].lut_prop_reset_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_reset_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_reset_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | tran min. | tran center | tran max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_reset_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_reset_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_reset_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+index2_offset].direction_reset_tran + "|"+str(harnessList2[index1][index2*2+index2_offset].lut_tran_reset_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_reset_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_reset_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | eintl min. | eintl center | eintl max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_eintl_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2].direction_power   + "|"+str(harnessList2[index1][index2*2].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+1].direction_power + "|"+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | ein min. | ein center | ein max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2].direction_power   + "|"+str(harnessList2[index1][index2*2].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_ein_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+1].direction_power + "|"+str(harnessList2[index1][index2*2+1].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_ein_mintomax[2])+" |\n")

                outlines.append("\n")

            ## (3) set
            if targetCell.set is not None:
                ## Harness search for set
                ## index2 is an base pointer for harness search
                ## index2_offset and index2_offset_max are used to 
                ## search harness from harnessList2 which contain "timing_type_set"
                index2 = targetCell.outports.index(target_outport) 
                index2_offset = 0
                index2_offset_max = 10
                while(index2_offset < index2_offset_max):
                    #targetLib.print_msg(harnessList2[index1][index2*2+index2_offset])
                    if hasattr(harnessList2[index1][index2*2+index2_offset], "timing_type_set"):
                        break
                    index2_offset += 1
                if(index2_offset == 10):
                    targetLib.print_error("Error: index2_offset exceed max. search number\n")

                outlines.append("#### related pin : " + targetCell.set + "\n")
                
                outlines.append("| related pin | func | max cap |\n")
                outlines.append("|----|----|----|\n")
                outlines.append("| "+targetCell.set+" | "+targetCell.functions[index1].replace('|','\|')+" | "+str(targetCell.load[-1])+" |\n")
                outlines.append("\n")
                outlines.append("| direction | prop min. | prop center | prop max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_set_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_set_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_set_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+index2_offset].direction_set_prop + "|" +str(harnessList2[index1][index2*2+index2_offset].lut_prop_set_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_set_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_prop_set_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | tran min. | tran center | tran max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_set_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_set_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_set_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+index2_offset].direction_set_tran + "|"+str(harnessList2[index1][index2*2+index2_offset].lut_tran_set_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_set_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_tran_set_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | eintl min. | eintl center | eintl max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_eintl_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2].direction_power   + "|"+str(harnessList2[index1][index2*2].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_eintl_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+1].direction_power + "|"+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_eintl_mintomax[2])+" |\n")

                outlines.append("\n")
                outlines.append("| direction | ein min. | ein center | ein max |\n")
                outlines.append("|----|----|----|----|\n")

                #outlines.append("| rise | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2+index2_offset].lut_ein_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2].direction_power + "|"+str(harnessList2[index1][index2*2].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2].lut_ein_mintomax[2])+" |\n")
                outlines.append("|" + harnessList2[index1][index2*2+1].direction_power + "|"+str(harnessList2[index1][index2*2+1].lut_ein_mintomax[0])+" | "+str(harnessList2[index1][index2*2+1].lut_ein_mintomax[1])+" | "+str(harnessList2[index1][index2*2+1].lut_ein_mintomax[2])+" |\n")

                outlines.append("\n")
        outlines.append("\\newpage \n")
        f.writelines(outlines)
    f.close()
    targetCell.set_exported2doc()
## export harness data to .lib

## export harness data to .lib
def exitDocFiles(targetLib, num_gen_file):
    with open(targetLib.doc_name, 'a') as f:
        outlines = []
        outlines.append("}\n")
        f.writelines(outlines)
    f.close()
    targetLib.print_msg("\n-- doc file generation completed!!  ")
    targetLib.print_msg("--  "+str(num_gen_file)+" cells generated!!  \n")

