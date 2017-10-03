#!/bin/bash 

export HOME=$PWD

chmod 777 * -R

#cd ${0%/*} || exit 1 # models/mesh

params=$1
meshParamsFile=params.txt
IFS=',' read -a paramcut <<< "$params"
for (( c=0; c<=$(echo ${#paramcut[@]} - 1 | bc); c=c+2 ))
do
    pname=${paramcut[$c]}
	pval=${paramcut[$c+1]}
	echo $pname $pval >> $meshParamsFile
done
cp params.txt models/mesh/params.txt
#$Home= PWD
#$2=results/case_i/mesh
meshOutDir=$HOME/$2

run_command="docker run --rm  -i -v `pwd`:/scratch -w /scratch/models/mesh -u 0:0 marmarm/salome:v8_2u "
SALOMEPATH=""

# Make sure the directories exist
mkdir -p $meshOutDir #Home or PWD/case_i/mesh

# Generate the mesh.unv file using salome
meshScript="genMesh.py"
unvMeshFile="mesh.unv"

# Running from models/mesh
cmd="${SALOMEPATH}salome start -t -w 1 $meshScript args:$meshParamsFile,$unvMeshFile"
#                                      genMesh.py       params.txt      mesh.unv
# run salome
echo $run_command $cmd
$run_command $cmd

mv models/mesh/*.stl $meshOutDir
#        HOME or PWD /case_i/mesh
# convert the mesh to abaqus format

AbqMeshFile="abq_mesh.inp"

echo $run_command ./unical $unvMeshFile $AbqMeshFile
$run_command ./unical $unvMeshFile $AbqMeshFile
#                      mesh.unv     abq_mesh.inp

CCXMesh="all.msh"
ExoMesh="mesh.exo"

cd models/mesh
./bootstrapMesh.sh $AbqMeshFile $CCXMesh $ExoMesh

mv $CCXMesh $meshOutDir
mv $ExoMesh $meshOutDir

# clean up files
#rm *.out *.err tmp *.abq *.unv *.inp -R > /dev/null 2>&1

exit 0
