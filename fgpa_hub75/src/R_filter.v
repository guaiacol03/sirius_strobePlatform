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

module rotary_orderScanner (
    input wire r_cw,
    input wire r_ccw,
    input wire clk,
    output reg o_cw,
    output reg o_ccw
);
    wire i_cw;
    rotary_filter16 f_cw (
        .I(r_cw),
        .clk(clk),
        .ticked_o(i_cw)
    );

    wire i_ccw;
    rotary_filter16 f_ccw (
        .I(r_ccw),
        .clk(clk),
        .ticked_o(i_ccw)
    );

    reg[21:0] last_timer = 22'b0;
    reg last_cw = 1'b0;
    reg last_begin = 1'b1;

    always @(posedge clk) begin
        if (i_cw || i_ccw) begin
            last_timer <= 22'hFFFFFF;
            last_cw <= i_cw;
            last_begin <= ~last_begin;
        end else begin
            if (|last_timer) begin
                last_timer <= last_timer - 22'b1;
            end else begin
                last_begin <= 1'b1;
            end
        end

        if (!last_begin) begin
            o_ccw <= last_cw && i_ccw;
            o_cw <= (!last_cw) && i_cw;
        end else begin
            o_cw <= 1'b0;
            o_ccw <= 1'b0;
        end
    end

endmodule