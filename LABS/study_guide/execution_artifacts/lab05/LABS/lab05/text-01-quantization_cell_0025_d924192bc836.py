#TODO: check the difference between the original and the dequantized result
out_diff = (out - out_deq).abs().mean()
print("Mean absolute output error:", out_diff.item())