# library settings
| lib | model | 
|----|----|----|----|----|
| lib | model | 
## Unit
| cap | volt | cur | leak | time | 
|----|----|----|----|----|
| cap | volt | cur | leak | time | 
## Voltage terminals
| vdd | vss | gnd | pwell | nwell | 
|----|----|----|----|----|
| vdd | vss | gnd | pwell | nwell | 
## Operating conditions
| process | temp |
|----|----|
| process | temp |

## Logic thresholds
### input thresholds 
| rise | fall |
|----|----|
| rise | fall |
### output thresholds
| rise | fall |
|----|----|
| rise | fall |


# cells
## combcell 1
### Common
| area | leak | 
|----|----|
| area | leak |
### Input Pin A
| max_tran | cap | 
|----|----|
| max_tran | cap |
### Output Pin Y
| max_cap | func | dly r | dly f | pow r | pow f | 
|----|----|----|----|----|----|
| max_cap | func | dly r | dly f | pow r | pow f | 

## seqcell 1
### Common
| area | leak | 
|----|----|
| area | leak |
### Input Pin A
| max_tran | cap | setup r | setup f | hold r | hold f | 
|----|----|----|----|----|----|
| max_tran | cap | setup r | setup f | hold r | hold f |
### Clock Pin C
| max_tran | cap |
|----|----|
| max_tran | cap |
### Reset Pin R
| max_tran | cap | dly r | dly f | pow r | pow f | recov | remov |
|----|----|----|----|----|----|----|----|----|----|
| max_tran | cap | dly r | dly f | pow r | pow f | recov | remov |
### Output Pin Y
| max_cap | func | dly r | dly f | pow r | pow f | 
|----|----|----|----|----|----|
| max_cap | func | dly r | dly f | pow r | pow f | 

