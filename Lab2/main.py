import random
import numpy as np
import pandas as pd
from Lab2.Analize import DimRed

def modify_to_cont(sample, seed=42):
    random.seed(seed)
    return [x + 0.01 * random.random() for x in sample]


def read_csv_data(fname, sample_size):
    data = pd.read_csv(fname, dtype=float, nrows=sample_size)
    names = data.columns
    return data[list(names[1:])]


def main():
    data = read_csv_data('year_prediction.csv', 1000)
    red = DimRed(data)
    red.pca_svd(2)
    red.spectral_emb(2)

if __name__ == '__main__':
    main()
