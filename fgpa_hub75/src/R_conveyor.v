module rotary_conveyorStep (
    input wire[1:0] data_prev,
    output wire prev_move,
    output reg[1:0] data = 2'b0,
    input wire next_move,
    input wire clk
);
    assign prev_move = next_move || !(|data);

    always @(posedge clk) begin
        if (prev_move) begin
            data <= data_prev;
        end
    end
endmodule

module rotary_conveyorLoader #(
    parameter DATA = 2'b00
) (
    input wire[1:0] data_prev,
    output wire prev_move,
    output reg[1:0] data = 2'b0,
    input wire next_move,
    input wire clk,

    input wire set
);
    reg transact = 1'b0;
    assign prev_move = next_move || !(|data);

    always @(posedge clk) begin
        if (!transact && set) begin
            transact <= 1'b1;
        end

        if (prev_move) begin
            if (|data_prev) begin
                data <= data_prev;
            end else begin
                if (transact) begin
                    data <= DATA;
                    transact <= 1'b0;
                end else begin
                    data <= data_prev;
                end
            end
        end
    end
endmodule


module rotary_conveyor (
    input wire clk,
    output wire[1:0] data,
    input wire data_next,
    input wire[2:0] set
);
    wire[1:0] data_bus [31:0];
    wire move_bus [31:0];
    genvar i;
    generate
        for (i=1; i < 32; i=i+1) begin
            rotary_conveyorStep step_inst (
                .data(data_bus[i]),
                .data_prev(data_bus[i-1]),
                .next_move(move_bus[i]),
                .prev_move(move_bus[i-1]),
                .clk(clk)
            );
        end
    endgenerate

    assign move_bus[31] = data_next;
    assign data = data_bus[31];

    wire[1:0] data_cw_btn;
    wire move_btn_cw;
    rotary_conveyorLoader #(
        .DATA(2'b11)
    ) ldr_btn (
        .data(data_bus[0]),
        .data_prev(data_cw_btn),
        .next_move(move_bus[0]),
        .prev_move(move_btn_cw),
        .clk(clk),
        .set(set[2])
    );

    wire[1:0] data_ccw_cw;
    wire move_cw_ccw;
    rotary_conveyorLoader #(
        .DATA(2'b10)
    ) ldr_cw (
        .data(data_cw_btn),
        .data_prev(data_ccw_cw),
        .prev_move(move_cw_ccw),
        .next_move(move_btn_cw),
        .clk(clk),
        .set(set[1])
    );

    rotary_conveyorLoader #(
        .DATA(2'b01)
    ) ldr_ccw (
        .data(data_ccw_cw),
        .data_prev(2'b00),
        .next_move(move_cw_ccw),
        .clk(clk),
        .set(set[0])
    );
endmodule