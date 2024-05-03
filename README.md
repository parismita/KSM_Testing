# KSM_Testing

# Introduction
Kernel Samepage Merging (KSM) is a memory management feature implemented in the Linux kernel that enhances the efficiency of memory usage by identifying and merging duplicate pages based on content. By allowing the system to consolidate identical data into fewer memory pages, KSM can significantly reduce the overall memory footprint of running applications, especially in virtualized environments where many instances might run similar or identical tasks. This service is particularly useful when combined with virtual machine platforms such as QEMU and KVM, where each VM instance can be treated as a separate process by the host system, thereby optimizing memory utilization across virtual machines. 

# Problem Statement
The goal of this project is to study a comprehensive  performance characterization of KSM  to understand its behavior, workings and its impact thoroughly by using various workloads, setups and configurations such as scan rates to obtain performance and cost metrics. We aim to study the above to find out behavior and workings of this service.

# Setup
Step 1: Install Dependencies 

`sudo apt install build-essential ksmtuned smem systat qemu-system libguestfs-tools`

`sudo apt install qemu-kvm virt-manager virtinst libvirt-clients bridge-utils libvirt-daemon-system -y`  

`sudo apt install sysbench`

Note: Sysbench - multiple table were created inside each vm and read write query workload was run - for multiple VMs

Step 2: To Monitor run monitor.sh 

`Usage: ./monitor.sh <num_process> <num_pages_per_process> <number_of_rounds> <round_wait_time> <pages_to_scan>`

The spawning and monitoring happens with this step, but if you want to spawn individually use spawner as step 3

Step 3: 

`Usage: ./spawner.sh <num_process> <num_pages_per_process> <number_of_rounds> <round_wait_time> `

Step 4: 

To generate data use data-gen.sh 

Step 5: 

To initiate the VM, install the VM using `https://wiki.archlinux.org/title/libvirt#Installation`
