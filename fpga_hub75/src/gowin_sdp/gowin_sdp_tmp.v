//Copyright (C)2014-2025 Gowin Semiconductor Corporation.
//All rights reserved.
//File Title: Template file for instantiation
//Tool Version: V1.9.12.01 (64-bit)
//IP Version: 1.0
//Part Number: GW5A-LV25MG121NC1/I0
//Device: GW5A-25
//Device Version: A
//Created Time: Tue Jan  6 04:53:34 2026

//Change the instance name and port connections to the signal names
//--------Copy here to design--------

    Gowin_SDP your_instance_name(
        .dout(dout), //output [63:0] dout
        .clka(clka), //input clka
        .cea(cea), //input cea
        .clkb(clkb), //input clkb
        .ceb(ceb), //input ceb
        .oce(oce), //input oce
        .reset(reset), //input reset
        .ada(ada), //input [7:0] ada
        .din(din), //input [63:0] din
        .adb(adb) //input [7:0] adb
    );

//--------Copy end-------------------
