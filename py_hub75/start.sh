#!/bin/bash

cd /root/prog
openFPGALoader -b tangprimer25k --freq 2500000 ./fpga_hub75.fs
python3 -u ./main.py
