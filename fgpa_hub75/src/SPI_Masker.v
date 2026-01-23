module SPI_imageMask (
    input wire clk,
    input wire ena,

    input wire[63:0] ctrl,
    input wire[7:0] I_addr,
    input wire[63:0] I_data,
    output reg[63:0] O_data,

    input wire div_clk
);

wire[1:0] bank = I_addr[7:6];
wire[5:0] pos = I_addr[5:0];

wire ctrl_ena = &ctrl[7:0];
wire[15:0] ctrl_div1 = ctrl[55:40];
reg[15:0] div1 = 16'b0;
wire[15:0] ctrl_div2 = ctrl[39:24];
reg[15:0] div2 = 16'b0;
reg div_result = 1'b0;

always @(posedge div_clk) begin
    div1 <= (div1 >= ctrl_div1) ? 16'b0 : (div1 + 16'b1);
    div2 <= (div2 >= ctrl_div2) ? 16'b0 : (div2 + (div1 >= ctrl_div1));
    div_result <= div2 >= ctrl_div2;
end

reg frame_state = 16'b0;
always @(posedge div_result) begin
    frame_state <= ~frame_state;
end

reg[63:0] buffer_always = 64'b0;
reg[63:0] buffer_never = 64'b0;

always @(posedge clk) begin
    if (ena) begin
        if (ctrl_ena) begin 
            if (bank < 2'b10) begin
                O_data <= 64'b0;
                if (bank == 2'b00) begin
                    buffer_always <= I_data;
                end else begin
                    buffer_never <= I_data;
                end
            end else begin
                if (bank == 2'b10) begin
                    O_data <= (buffer_always | (I_data ^ {64{frame_state}})) & (~buffer_never);
                end else begin
                    O_data <= 64'b0;
                end
            end
        end else begin
            O_data <= I_data;
        end
    end
end

endmodule