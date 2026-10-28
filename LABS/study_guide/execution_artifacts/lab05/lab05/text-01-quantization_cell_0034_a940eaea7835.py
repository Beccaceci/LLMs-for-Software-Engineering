# Expand (W_q - zero_point_W) @ (x_q - zero_point_x).
# Use the quantized operand sums, rather than the original floats: rounding
# means the latter no longer give the same dequantized product.
out_deq = (
    out_q.to(torch.float32)
    - zero_point_x * W_q.to(torch.float32).sum(dim=1)
    - zero_point_W * x_q.to(torch.float32).sum()
    + W.shape[1] * zero_point_W * zero_point_x
) / (scale_W * scale_x)