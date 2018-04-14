import pandas as pd


def read_xlsx(fname):
    data = pd.read_excel(fname, header=1)
    return data


def main():
    fname = 'test.xlsx'
    data = read_xlsx(fname)


if __name__ == "__main__":
    main()
