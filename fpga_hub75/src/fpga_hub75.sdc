//Copyright (C)2014-2026 GOWIN Semiconductor Corporation.
//All rights reserved.
//File Title: Timing Constraints file
//Tool Version: V1.9.12.01 (64-bit) 
//Created Time: 2026-01-09 05:23:19
create_clock -name clk_20M -period 50 -waveform {0 25} [get_nets {clk_20M}]
