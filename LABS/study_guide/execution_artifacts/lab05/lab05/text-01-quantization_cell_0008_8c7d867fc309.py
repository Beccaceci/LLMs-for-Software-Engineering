def absmax_quantize(W):
    # NOTE: we assume that we always map to 8-bit integers

    # TODO: find the scale factor that maps the maximum absolute value in W to the maximum value of int8
    max_value = W.abs().max()
    scale = torch.where(max_value > 0, max_value / 127, torch.ones_like(max_value)) # how "long" the step between any two int8 values is

    # TODO: quantize W using the scale factor (hint: remember to round to the nearest integer and convert to int8)
    W_q = torch.round(W / scale).clamp(-127, 127).to(torch.int8)
    return W_q, scale