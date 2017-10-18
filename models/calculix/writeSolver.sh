#!/bin/bash

file=solve.inp

writeInterval=$1
endTime=$2

echo "" > $file

cat >> $file <<END
*include, input=all.msh

** material definition
** {m,kg,s,K} 
*material, name=steel
*elastic
2.1e11,0.333333333,0
*density
** kg/m3
7850
*expansion
12e-6
*conductivity
** W/mK
50.,0
*specific heat
** J/kg-K
500

*BOUNDARY
NFixedLine,1,3

** material assignment to bodies
*solid section, elset=Eall, material=steel

** initial temperature
*initial conditions, type=temperature
Nall,300

*TIME POINTS,NAME=T1,GENERATE 
0.0,$endTime,$writeInterval

**CONTROLS, PARAMETERS=FIELD
**0.02, 1.0

END

for step in $(ls -1v bc/T);do
echo $step
cat >> $file <<END
*step
** boundary conditions
*include, input=bc/T/$step
**include, input=bc/p/$(echo $step | sed 's/T/p/g')
*UNCOUPLED TEMPERATURE-DISPLACEMENT
1,$writeInterval
*node file,TIMEPOINTS=T1
NT,U
*el file,TIMEPOINTS=T1
S,HFL
*end step

END
done
