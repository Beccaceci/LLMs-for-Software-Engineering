from datasets import load_dataset

# Load a sentiment analysis dataset
dataset = load_dataset('imdb')

train_dataset = dataset['train'].shuffle(seed=42).select(range(2000))
test_dataset = dataset['test'].shuffle(seed=42).select(range(1000))