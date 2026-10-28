# Perform backpropagation to compute gradients
loss.backward()

print("Loss:", loss.item())
print("Gradients:")
print("dL/d(theta1):", theta1.grad)
print("dL/d(theta2):", theta2.grad)