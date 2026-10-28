def minmax_quantize(W):
    # the following notations come from:
    # (1) scaling W to [0,1] ==> W' = (W - min(W)) / (max(W) - min(W)),
    # (2) scaling W' to [-128, 127] ==> W_q = W' * 255 - 128
    # by combining the two, we get that:
    # W_q = W * scale + offset
    # we will call the offset "zero_point", as it represent the value that maps to 0
    
    # TODO: find the scale factor that maps the minimum and maximum values in W to -128 and 127
    delta = W.max() - W.min() # the range of values in W
    scale = torch.where(delta > 0, 255 / delta, torch.ones_like(delta))
    zero_point = -128 - W.min() * scale # the value that maps to 0

    # TODO: quantize W using the scale factor (hint: remember to round to the nearest integer and convert to int8)
    W_q = torch.round(W * scale + zero_point).clamp(-128, 127).to(torch.int8)
    
    return W_q, scale, zero_point

def minmax_dequantize(W_q, scale, zero_point):
    # TODO: dequantize W_q using the scale factor and zero_point
    dequantized_W = (W_q.to(torch.float32) - zero_point) / scale
    return dequantized_W