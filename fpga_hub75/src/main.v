module main (
    input wire clk_50M,

    input wire SPI_miso,
    input wire SPI_sclk,
    input wire SPI_ce,
    input wire SPI_alt,

    output wire A,
    output wire B,
    output wire C,
    output wire D,
    output wire E,
    
    output wire R0,
    output wire G0,
    output wire B0,
    
    output wire R1,
    output wire G1,
    output wire B1,

    output wire TCK,
    output wire LTC,
    output wire OE
);

wire clk_20M_u;
Gowin_PLL gen_20M (
    .clkin(clk_50M),
    .clkout0(clk_20M_u),
    .mdclk(clk_50M)
);

wire clk_8M;
Gowin_PLL_1 gen_8M(
    .clkin(clk_50M), //input  clkin
    .clkout0(clk_8M), //output  clkout0
    .mdclk(clk_50M) //input  mdclk
);

wire clk_20M;
DCE uut_20M (
    .CLKIN(clk_20M_u),
    .CE(1'b1),
    .CLKOUT(clk_20M)
);

wire[7:0] SPI_addr;
wire[63:0] SPI_data;
wire SPI_en;
SPI_bramComm #(
    .MAX_POS(8'd191)
) inst_spiImg(
    .SPI_miso(SPI_miso),
    .SPI_clk(SPI_sclk),
    .SPI_rst(SPI_alt),
    .BRAM_clk(clk_20M),
    .BRAM_addr(SPI_addr),
    .BRAM_data(SPI_data),
    .BRAM_en(SPI_en)
);

reg[63:0] Ctrl_reg;
wire[63:0] SPI_ctData;
wire SPI_ctEn;
SPI_bramComm #(
    .MAX_POS(8'd0)
) inst_spiCtrl (
    .SPI_miso(SPI_miso),
    .SPI_clk(SPI_sclk),
    .SPI_rst(~SPI_alt),
    .BRAM_clk(clk_20M),
    .BRAM_addr(),
    .BRAM_data(SPI_ctData),
    .BRAM_en(SPI_ctEn)
);
always @(posedge clk_20M) begin
    if (SPI_ctEn) begin
        Ctrl_reg <= SPI_ctData;
    end
end

wire[63:0] bram_dout;
wire[7:0] bram_oaddr;
wire bram_oen;
Gowin_SDP inst_bram (
    .dout(bram_dout), //output [63:0] dout
    .clka(clk_20M), //input clka
    .cea(SPI_en), //input cea
    .clkb(clk_20M), //input clkb
    .ceb(bram_oen), //input ceb
    .oce(1'b1), //input oce
    .reset(1'b0), //input reset
    .ada(SPI_addr), //input [7:0] ada
    .din(SPI_data), //input [63:0] din
    .adb(bram_oaddr) //input [7:0] adb
);

wire[63:0] bram_dout_mask;
SPI_imageMask inst_masker (
    .ena(bram_oen),
    .clk(clk_20M),
    .I_addr(bram_oaddr),
    .I_data(bram_dout),
    .O_data(bram_dout_mask),
    .ctrl(Ctrl_reg),
    .div_clk(clk_8M)
);

wire[4:0] addr;
wire[2:0] rgb0;
wire[2:0] rgb1;
bus75_bramReader inst_bram_reader (
    .bram_rddata(bram_dout_mask),
    .bram_addr(bram_oaddr),
    .bram_en(bram_oen),

    .brightness(Ctrl_reg[63:56]),
    
    .clk(clk_20M),
    
    .addr(addr),
    .rgb0(rgb0),
    .rgb1(rgb1),

    .tick(TCK),
    .latch(LTC),
    .oe(OE)
);

assign A = addr[0];
assign B = addr[1];
assign C = addr[2];
assign D = addr[3];
assign E = addr[4];

assign R0 = rgb0[0];
assign G0 = rgb0[1];
assign B0 = rgb0[2];

assign R1 = rgb1[0];
assign G1 = rgb1[1];
assign B1 = rgb1[2];

endmodule