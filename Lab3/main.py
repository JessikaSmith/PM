import pandas as pd
from Lab3.ML import *

def read_csv_data(fname, sample_size):
    data = pd.read_csv(fname, nrows=sample_size)
    data.dropna(how="all", inplace=True)
    names = data.columns
    # data[list(names[1:])]
    return data[list(names[1:])]


def main():
    data = read_csv_data('datatraining.txt', 1000)
    data = data.convert_objects(convert_numeric=True)
    print(data.dtypes)
    clust = Clustering(data[list(data.columns[:-1])], data['Occupancy'])
    clust.dbscan()


if __name__ == '__main__':
    main()
