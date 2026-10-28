print(x_q)
print(x)

# TODO: dequantize x_q and check how close it is to the original x
x_deq = absmax_dequantize(x_q, scale_x)
print(x_deq)
x_diff = (x - x_deq).abs().mean()
print(x_diff)