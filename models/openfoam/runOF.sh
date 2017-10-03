#!/bin/bash

echo ""
echo "Running OpenFOAM Analysis..."
echo $@
echo ""

chmod 777 * -R

HOME=$PWD

params=$1 # string with the params
geomLocation=$HOME/$2 #HOME or PWD/ results/case_0/mesh
bodyFiles=$HOME/$3 #HOME or PWD/ results/case_0/openfoam/results.tgz
metricFile=$4 # results/case_0/openfoam/metric.csv
metricImages=$5 # results/case_0/case_0/openfoam/png

mkdir -p $metricImages
mkdir -p $(dirname $bodyFiles)

cd ${0%/*} || exit 1  # Run from this directory

caseParams=params.txt
IFS=',' read -a paramcut <<< "$params"
for (( c=0; c<=$(echo ${#paramcut[@]} - 1 | bc); c=c+2 ))
do
    pname=${paramcut[$c]}
	pval=${paramcut[$c+1]}
	echo $pname $pval >> $caseParams
done

chmod 777 * -R

# replace the openfoam stl file
mkdir -p constant/triSurface/
cp $geomLocation/*.stl constant/triSurface/
cp 0.template 0.orig -R
cp system.template system -R

# replace the params in the case files
echo "Replacing parameters:"
while IFS='' read -r line || [[ -n "$line" ]]; do
	pname=$(echo $line | cut -d " " -f1 | tr -d '[:space:]')
    pval=$(echo $line | cut -d " " -f2 | tr -d '[:space:]')
    echo $pname $pval
    find ../openfoam -type f  -not -path "*/polyMesh/*" -not -path "*/0.template/*" -not -path "*/system.template/*" -exec sed -i "s/@@$pname@@/$pval/g" {} \;
done < $caseParams
echo "Done replacing parameters"

# openfoam analysis
run_command="docker run --rm --user root -i -v `pwd`:/scratch -w /scratch parallelworks/openfoam:4.1_paraview"
#run_command=""
echo $run_command ./runOpenFOAM.sh
$run_command ./runOpenFOAM.sh

tar czvf tmp.tgz -C VTK body 
mv tmp.tgz $bodyFiles

# metric extraction
cd $HOME
echo "Extracting OpenFOAM Results..."
run_command="docker run --rm  -i --user root -v `pwd`:/scratch -w /scratch parallelworks/openfoam:4.1_paraview"
echo $run_command ./models/mexdex/extract.sh /opt/paraview540/bin models/mexdex/extract.py models/openfoam/system/controlDict models/openfoam/kpi.json $metricImages $metricFile
$run_command ./models/mexdex/extract.sh /opt/paraview540/bin models/mexdex/extract.py models/openfoam/system/controlDict models/openfoam/kpi.json $metricImages $metricFile

exit 0
