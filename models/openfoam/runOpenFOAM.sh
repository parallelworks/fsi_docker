#!/bin/bash

FOAM_INST_DIR=/opt
OPENFOAM_PATH=/opt/openfoam4
. $OPENFOAM_PATH/etc/bashrc
. $OPENFOAM_PATH/bin/tools/RunFunctions

SOLVER=buoyantBoussinesqSimpleFoam
NP=2

sed -i "s/.*numberOfSubdomains.*/numberOfSubdomains $NP;/" system/decomposeParDict
rm -rf constant/polyMesh

# meshing
blockMesh -dict system/blockMeshDict
decomposePar -force -noFunctionObjects
mpirun --allow-run-as-root -np $NP snappyHexMesh -parallel -overwrite
reconstructParMesh -constant

# move field templates to processors
ls -d processor* | xargs -I {} rm -rf ./{}/0
ls -d processor* | xargs -I {} cp -r 0.orig ./{}/0

# initialize fields
mpirun --allow-run-as-root -n $NP patchSummary -parallel
#mpirun --allow-run-as-root -n $NP potentialFoam -parallel

# solve
mpirun --allow-run-as-root  -np $NP $SOLVER -parallel

# reconstruction
reconstructPar -withZero

#foamToVTK -useTimeName #-ascii
foamToVTK -useTimeName     -allPatches -noInternal # -latestTime #-ascii
