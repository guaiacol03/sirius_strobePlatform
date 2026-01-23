module bus75_rowWriter (
    input wire[63:0] buffer_r0,
    input wire[63:0] buffer_r1,
    input wire[63:0] buffer_g0,
    input wire[63:0] buffer_g1,
    input wire[63:0] buffer_b0,
    input wire[63:0] buffer_b1,
    input wire[7:0] buffer_brt,
    output reg write_can,
    output reg write_next,
    
    
    input wire clk,
    
    output wire tick,
    output reg latch,
    output reg oe,
    output wire[2:0] rgb0,
    output wire[2:0] rgb1
);

reg[5:0] clk_timer = 6'b111111;
reg[7:0] clk_pause = 8'b11111111;

wire timer_full;
DL #(
   .INIT(1'b1)
) LDPE_inst (
   .Q(timer_full),
   .D(&clk_timer),
   .G(~clk)
);

assign tick = ~timer_full & ~clk;

always @(posedge clk) begin
    if (~&clk_timer) begin
        clk_timer <= clk_timer + 6'd1;
    end else begin
        if (&clk_pause) begin
            clk_timer <= 6'b0;
        end
    end
end

always @(posedge clk) begin
    if (&clk_timer) begin
        // will reset to 0 on last tick along with clk_timer
        clk_pause <= clk_pause + 8'd1;
    end
end

always @(posedge clk) begin
    latch <= &clk_timer & (~|clk_pause);
    oe <= &clk_timer & (clk_pause < buffer_brt);
end

always @(posedge clk) begin
    write_can <= &clk_timer & (~&clk_pause);
    write_next <= &clk_timer & (clk_pause == 8'b11111110);
end

assign rgb0 = {
    buffer_r0[clk_timer],
    buffer_g0[clk_timer],
    buffer_b0[clk_timer]
};
assign rgb1 = {
    buffer_r1[clk_timer],
    buffer_g1[clk_timer],
    buffer_b1[clk_timer]
};

endmodule