# TODO: Implement the TimeSeriesDataset class to generate a dataset of time series with jumps
class TimeSeriesDataset(torch.utils.data.Dataset):
    def __init__(self, seq_len, num_samples):
        """
        Initializes the dataset by generating a number of time series samples with jumps.

        Args:
        - seq_len (int): The length of each time series sequence.
        - num_samples (int): The number of samples in the dataset.

        Notes:
        - Each time series will have jumps every 'val' steps, starting at a random point.
        - The size of the jump is 'initial_jump' plus some random noise.
        """
        val = 3  
        initial_jump = 5 

        self.seq_len = seq_len
        self.data = []
        for _ in range(num_samples):
            time_series = np.zeros(seq_len + 1)

            # TODO: Introduce the first jump at a random point between 0 and val
            first_jump = np.random.randint(0, val)
            time_series[first_jump] += initial_jump + np.random.rand()  # Add a jump with some random noise

            # TODO: Continue introducing jumps every val timesteps after the first jump
            for i in range(first_jump + val, seq_len + 1, val):
                jump = 0 if i % 2 == 1 else initial_jump  # Alternate between 0 and initial_jump
                time_series[i] += jump + np.random.rand()  # Add a jump with some random noise

            self.data.append(time_series)

    def __len__(self):
        # TODO: Return the length of the dataset
        return len(self.data)

    def __getitem__(self, idx):
        """
        Returns the time series at the specified index.

        Args:
        - idx (int): The index of the desired time series.

        Returns:
        - A tuple of (time series, final jump value)
        """
        series = self.data[idx]
        return torch.tensor(series[:self.seq_len], dtype=torch.float32), torch.tensor(series[self.seq_len], dtype=torch.float32)