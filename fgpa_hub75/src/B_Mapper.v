module hub75_bramMapper #(
    parameter DEAD_ADDR = 8'hFF
) (
    input wire[4:0] line,
    input wire[2:0] color,
    output reg[7:0] out_addr,
    input wire[63:0] in_data,
    output wire[63:0] out_data
);
// 2'b00 - right border
assign out_data = {2'b00, in_data[62:1]};

always @(*) begin
    if (color <= 3'b010) begin
        if (&line) begin
            out_addr = DEAD_ADDR;
        end else begin
            out_addr = line + (8'd64 * color) + 8'd1;         
        end
    end else begin
        if (&line) begin
            out_addr = 8'd32 + (8'd64 * (color - 3'b011));
        end else begin
            if (line == 8'd30) begin
                out_addr = DEAD_ADDR;
            end else begin
                out_addr = line + 8'd32 + (8'd64 * (color - 3'b011)) + 8'd1;
            end
        end
    end
end

endmodule