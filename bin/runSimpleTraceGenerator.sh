#!/usr/bin/env bash

# Absolute path to this script, e.g. /home/user/bin/foo.sh
# Absolute path this script is in, thus /home/user/bin
pushd `dirname $0` > /dev/null
BASEDIR=`pwd`
popd > /dev/null
# set the output path for the traces
tracePath="/home/s1671850/hermes/traces"
#tracePath="defaultPath"

if [ $tracePath = "defaultPath" ]
then
    tracePath=${BASEDIR}/../traces
    echo $tracePath
fi

# declare parameters to produce traces
declare -a zipfExp=(0.99)                 #("0.60" "0.70" "0.90" "0.99" "1.01" )
declare -a workloadSize=(10000000)        #("25000000" "50000000")
#declare -a workloadSize=(100000)        #("25000000" "50000000")
declare -a numberOfKeys=(1000000)       #("125000000" "250000000")

for a in "${zipfExp[@]}"
do
    for w in "${workloadSize[@]}"
    do
        for k in "${numberOfKeys[@]}"
        do
            echo "Running with -a $a -w $w -k $k"
            ./../src/runSimpleTraceGenerator.py -a $a -w $w -k $k \
             > ${tracePath}/simple_trace_w_${w}_k_${k}_a_${a}.txt
        done
    done
done
