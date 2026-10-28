print(W_q)
print(W)

#TODO: dequantize W_q and check how close it is to the original W
W_deq = minmax_dequantize(W_q, scale_W, zero_point_W)
print(W_deq)
W_diff = (W - W_deq).abs().mean()
print(W_diff)
print("zero point", zero_point_W)