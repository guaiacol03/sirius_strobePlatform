module SPI_RComm (
    input wire clk,
    input wire SPI_clk,
    output wire SPI_miso,

    input wire[1:0] data_vals,
    output reg data_next = 1'b0
);
    reg[3:0] w_buffer = 4'b0;

    always @(posedge clk) begin
        data_next <= rea_q && !(|w_buffer);

        if (rea_q) begin
            if (!(|w_buffer)) begin
                w_buffer[3] <= |data_vals;
                w_buffer[2] <= data_vals >= 2'b10;
                w_buffer[1] <= &data_vals;
            end else begin
                w_buffer <= w_buffer >> 1;
            end
        end
    end
    
    wire rep_q;
    wire rea_q;
    DFFC #(
        .INIT(1'b0)
    ) rot_en_prop (
        .CLK(SPI_clk),
        .D(1'b1),
        .CLEAR(rea_q),
        .Q(rep_q)
    );
    DFF #(
        .INIT(1'b0)
    ) rot_en_act (
        .CLK(clk),
        .D(rep_q),
        .Q(rea_q)
    );

    assign SPI_miso = w_buffer[0];

endmodule