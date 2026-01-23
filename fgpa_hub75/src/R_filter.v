module rotary_filter16 (
    input wire I,
    input wire clk,
    output reg ticked_o
);
    reg[15:0] time_l = 16'b0;
    reg[15:0] time_h = 16'b0;
    reg state = 1'b0;
    reg last_state = 1'b0;

    always @(posedge clk) begin
        if (I) begin
            time_l <= 16'b0;
            time_h <= time_h + (&time_h ? 16'b0 : 16'b1);
        end else begin
            time_l <= time_l + (&time_l ? 16'b0 : 16'b1);
            time_h <= 16'b0;
        end

        if (&time_h || &time_l) begin
            state <= &time_h;
        end
    end 

    always @(posedge clk) begin
        ticked_o <= (!state) && last_state;
        last_state <= state;
    end

endmodule