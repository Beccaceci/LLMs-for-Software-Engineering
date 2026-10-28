# TODO: perform the matrix multiplication using the quantized values converted to int16
out_q = W_q.to(torch.int16) @ x_q.to(torch.int16) 
print(out_q)