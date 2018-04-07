import asciitable
import random

from Lab1.Tools import Distribution, Estimator


def main():
    data = asciitable.read('ringwaydata.txt', fill_values=('---', None))
    data = data.filled()
    data.dtype.names = ('year', 'mm', 'tmax_deg', 'tmin_deg',
                        'af_days', 'rain_mm', 'sun_hours')
    max_deg = list(data['tmax_deg'])
    max_deg = [float(x) for x in max_deg if x != 'N/A']
    random.seed(42)
    max_deg = [x + 0.01 * random.random() for x in max_deg]
    m = Distribution(max_deg)
    # m.show_histogram()
    # m.kernel_density(1)
    est = Estimator(max_deg)
    est.divide_subset(3)


if __name__ == '__main__':
    main()


