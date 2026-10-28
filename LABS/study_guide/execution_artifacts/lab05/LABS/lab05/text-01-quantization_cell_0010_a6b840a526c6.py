def absmax_dequantize(W_q, scale):
    # TODO: dequantize W_q using the scale factor
    dequantized_W = W_q.to(torch.float32) * scale
    return dequantized_W