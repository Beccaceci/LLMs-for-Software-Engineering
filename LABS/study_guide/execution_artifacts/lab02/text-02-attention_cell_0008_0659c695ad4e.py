# show a sample of the dataset

dataset = TimeSeriesDataset(seq_len=40, num_samples=1)
x, y = dataset[0]
plt.plot(range(40), x, label='x')
plt.title(f"Example Time Series Data Point\n y: {y}")
plt.scatter(40, y, color='r', label='y')
plt.legend()
plt.show()