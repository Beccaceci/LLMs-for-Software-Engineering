# Evaluate the model
results = trainer.evaluate()
print(f"Accuracy on the validation set: {results['eval_accuracy']:.4f}")
