module SPI_bramComm #(
    parameter MAX_POS = 8'd0
) (
    input wire SPI_miso,
    input wire SPI_clk,
    input wire SPI_rst,
    
    input wire BRAM_clk,
    output wire[7:0] BRAM_addr,
    output wire[63:0] BRAM_data,
    output wire BRAM_en
);

reg[63:0] read_buffer = 64'b0;
reg[5:0] read_counter = 6'b111111;
reg[7:0] pos_counter = MAX_POS;

always @(posedge SPI_clk) begin
    if (SPI_rst) begin
        read_counter <= 6'b111111;
        pos_counter <= MAX_POS;
    end else begin
        read_buffer <= (read_buffer << 1) + SPI_miso;
        read_counter <= read_counter + 6'b1;

        if (&read_counter) begin
            pos_counter <= pos_counter < MAX_POS ? (pos_counter + 8'b1) : 8'b0;
        end
    end
end

wire bep_clr;
wire bep_q;
DFFCE #(
    .INIT(1'b0)
) bram_en_prop (
    .CLK(~SPI_clk),
    .CE((read_counter == 6'b111111) & ~SPI_rst),
    .D(1'b1),
    .CLEAR(bep_clr),
    .Q(bep_q)
);
wire bea_q;
DFF #(
    .INIT(1'b0)
) bram_en_act (
    .CLK(BRAM_clk),
    .D(bep_q),
    .Q(bea_q)
);
assign bep_clr = bea_q;

assign BRAM_en = bea_q;
assign BRAM_addr = pos_counter;
assign BRAM_data = read_buffer;

endmodule