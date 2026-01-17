module bus75_bramReader (
    input wire[63:0] bram_rddata,
    output wire[7:0] bram_addr,
    output wire bram_en,
    input wire[7:0] brightness,
    
    input wire clk,
    output wire[4:0] addr,
    output wire[2:0] rgb0,
    output wire[2:0] rgb1,
    output wire tick,
    output wire latch,
    output wire oe
);

reg[63:0] buffer_r0 = 64'b0;
reg[63:0] buffer_r1 = 64'b0;
reg[63:0] buffer_g0 = 64'b0;
reg[63:0] buffer_g1 = 64'b0;
reg[63:0] buffer_b0 = 64'b0;
reg[63:0] buffer_b1 = 64'b0;
reg[7:0] buffer_brt = 8'b0;

wire writer_can;
wire writer_next;
wire ioe;
bus75_rowWriter writerInst (
    .buffer_r0(buffer_r0),
    .buffer_r1(buffer_r1),
    .buffer_g0(buffer_g0),
    .buffer_g1(buffer_g1),
    .buffer_b0(buffer_b0),
    .buffer_b1(buffer_b1),
    .buffer_brt(buffer_brt),
    
    .write_can(writer_can),
    .write_next(writer_next),
    
    .rgb0(rgb0),
    .rgb1(rgb1),
    .tick(tick),
    .latch(latch),
    .oe(ioe),
    
    .clk(clk)
);
assign oe = ~ioe;
assign bram_en = writer_can;


reg[4:0] phase = 5'b0;
// intermediate phases are skipped

wire[63:0] bram_mdata;
always @(posedge clk) begin
    if (writer_can) begin
        if (&phase[1:0]) begin
            case (phase[4:2])
                3'b000: begin
                    buffer_r0 <= bram_mdata;
                end
                3'b001: begin
                    buffer_g0 <= bram_mdata;
                end
                3'b010: begin
                    buffer_b0 <= bram_mdata;
                end
                3'b011: begin
                    buffer_r1 <= bram_mdata;
                end
                3'b100: begin
                    buffer_g1 <= bram_mdata;
                end
                3'b101: begin
                    buffer_b1 <= bram_mdata;
                end
            endcase
        end
        
        if (phase < 5'b11011) begin
            phase <= phase + 5'd1;
        end else begin
            if (writer_next) begin
                buffer_brt <= brightness;
                phase <= 5'b0;
            end
        end
    end
end

reg[4:0] line_pos = 5'b0;

always @(posedge clk) begin
    if (writer_next) begin
        line_pos <= line_pos + 5'd1;
    end
end 
assign addr = line_pos;

hub75_bramMapper inst_mapper (
    .line(line_pos),
    .color(phase[4:2]),
    .out_addr(bram_addr),
    .in_data(bram_rddata),
    .out_data(bram_mdata)
);

endmodule