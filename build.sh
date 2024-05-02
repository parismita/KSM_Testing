#!/bin/bash

g++ -o process process.c -lrt

# tar -xvf cs695_amd64.ova
# qemu-img convert -O qcow2 cs695_amd64-disk001.vmdk disk.qcow2

# sudo usermod -aG kvm $USER
# sudo chown root:kvm /dev/kvm
# sudo chmod 660 /dev/kvm