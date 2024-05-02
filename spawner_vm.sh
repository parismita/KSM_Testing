#!/bin/bash

# This script is used to spawn multiple writer process on core0 and core1 

if [ $# -ne 2 ]; then
    echo "Usage: $0 <num_process> <num_pages_per_process>"
    exit 1
fi

num_process=$1
num_pages_per_process=$2

p=0
while [ $p -lt $num_process ]
do
    cp disk.qcow2 disk$p.qcow2
    sudo bash start_vm.sh $p $2 &
    echo "vm no:" $p
    ((p++))
done