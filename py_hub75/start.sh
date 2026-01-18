#!/bin/bash

cd /root/prog
openFPGALoader -b tangprimer25k ./ao_0.fs
python3 -u ./main.py
