# TODO: dequantize the result and check how close it is to the original result
out_deq = out_q.to(torch.float32) * scale_W * scale_x

print(out_deq)
print(out)