import random
import numpy as np
import pandas as pd
from Lab2.Analize import *


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

    print('Optimal number of components is ', red.select_num_comp(10))

    optimal = red.select_num_comp(10)
    red.pca_svd(optimal)
    red.spectral_emb(optimal)
    red.fa(optimal)

if __name__ == '__main__':
    main()
