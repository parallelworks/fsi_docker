#!/bin/bash
# use this script to bootstrap a mesh.exo file for vtk mapping to cfd mesh

AbqMeshFile=$1
CCXMesh=$2
ExoMesh=$3

#cd ${0%/*} || exit 1    # Run from this directory
mkdir tmp

cp $AbqMeshFile tmp

cd tmp 

cat > mesh.fbd <<END
read $AbqMeshFile
send all abq
send all abq nam
END

cat > mesh.inp <<END
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
0.0,1,1

*step
*HEAT TRANSFER
1,1
*node file,TIMEPOINTS=T1
NT,U
*el file,TIMEPOINTS=T1
S,HFL
*end step
END

#dir=/opt/calculix
#$dir/cgx-212/cgx_2.12/src/cgx -bg mesh.fbd
#$dir/ccx-212-patch/src/ccx_2.12_MT mesh -o exo

docker run --rm -i -v `pwd`:/scratch -w /scratch -u 0:0 avidalto/calculix:v13 cgx_2.12 -bg mesh.fbd

cat all.msh *.nam *.bou  > allinone.inp 
mv allinone.inp all.msh

docker run --rm -i -v `pwd`:/scratch -w /scratch -u 0:0 avidalto/calculix:v13 cp /lib/ccx-212-patch.tgz .
tar -xvzf ccx**.tgz
ccx-212-patch/src/ccx_2.12_MT mesh -o exo

cd ../

cp tmp/all.msh $CCXMesh
cp tmp/mesh.exo $ExoMesh

rm tmp -R
