import math
from collections import Counter
from .vis import *
import scipy.stats


def get_quantiles(m, s, p):
    return scipy.stats.norm(m, s).ppf(p)


def kernel_gaussian(val):
    return 1 / math.sqrt(2 * math.pi) * math.exp(-val ** 2 / 2)


def kernel_epanechnikov(val):
    if abs(val) <= 1:
        return 3 / 4 * (1 - val ** 2)
    else:
        return 0


def kernel_tri_cube(val):
    if abs(val) <= 1:
        return (1 - abs(val) ** 3) ** 3
    else:
        return 0


class Distribution:

    def __init__(self, sample):

        self.values = sample
        self.values.sort()
        self.commonest = {}
        self.median = None
        self.variance = None
        self.lognormal_variance = None
        self.mean = sum(self.values) / len(self.values)
        self.lognormal_mean = None
        self.min = min(self.values)
        self.max = max(self.values)
        self.quartiles = []
        self.count_stats()

    def iqr(self):
        return scipy.stats.iqr(self.values)

    def count_commonest(self):

        freq_list = []
        m = Counter(self.values)
        frequency = m.most_common(1)[0][1]
        for a, b in m.items():
            if b == frequency:
                freq_list += [a]
        self.commonest[frequency] = freq_list

    def count_median(self):

        length = len(self.values)
        if length % 2 == 0:
            self.median = self.values[length // 2] + self.values[length // 2 - 1]
        else:
            self.median = self.values[length // 2]

        return

    def count_variance(self):

        self.variance = sum([(val - self.mean) ** 2 for val in self.values]) \
                        / (len(self.values) - 1)
        return

    def count_quartile(self):

        list_of_quartiles = []
        for i in [0.25, 0.5, 0.75]:
            list_of_quartiles += [self.count_quintile(i)]
        self.quartiles = list_of_quartiles

    def count_quintile(self, pp):

        i = math.floor(len(self.values) * pp + 1)
        # check
        # j = np.percentile(self.values, pp*100)
        return self.values[i]

    def count_stats(self):

        self.count_commonest()
        self.count_median()
        self.count_variance()
        self.standard_deviation = math.sqrt(self.variance)
        self.count_quartile()

        # self.skewness =
        # self.kurtosis =
        # self.quartiles =

        # self.print_stats()

    def print_cont_distrib_list(self):

        list = [
            'Normal distribution[a,sigma]',
            'Uniform distribution[{min,max}]',
            'Log-normal distribution[a,sigma]',
            'Triangular distribution[{a,c},b]',
            'Cauchy distribution[a,b]',
            'Exponential distribution[lambda]',
            'Laplace distribution[a,b]',
            'Pareto distribution[a,b]',
            'Weibull distribution[a,b,c]',
            'Beta distribution[a,b]',
            'Student distribution[v]',
            'Chi-square distribution[v]'
        ]
        for i in list:
            print(i)

    def print_stats(self):

        print('The commonest:', list(self.commonest.values())[0], 'with frequency', list(self.commonest.keys())[0])
        print('Max:', self.max)
        print('Min:', self.min)
        print('Mean:', self.mean)
        print('Median:', self.median)
        print('Variance:', self.variance)
        print('Standard deviation:', self.standard_deviation)
        print('Quartiles:', self.quartiles)

    def kernel_density(self, h):

        y_list1 = []
        y_list2 = []
        y_list3 = []
        for x in self.values:
            r = 1 / (len(self.values) * h)
            sm1 = 0
            sm2 = 0
            sm3 = 0
            for j in self.values:
                val = (x - j)
                sm1 += kernel_gaussian(val / h)
                sm2 += kernel_epanechnikov(val / 0.8)
                sm3 += kernel_tri_cube(val / 0.9)
            y_list1 += [r + sm1]
            y_list2 += [r + sm2]
            y_list3 += [r + sm3]
        self.show_kernel_density(y_list1, 'Gaussian_kernel.png')
        self.show_kernel_density(y_list2, 'Epanechnikov_kernel.png')
        self.show_kernel_density(y_list3, 'Tri-Cube_kernel.png')
        y_list = [y_list1] + [y_list2] + [y_list3]
        x_list = [self.values + self.values + self.values]
        self.show_all(x_list, y_list, 'Combined.png', ['Gaussian kernel', 'Epanechnikov kernel', 'Tri-Cube kernel'])

    def show_histogram(self, name='distrib_hist.png'):

        plot_histogram(self.values, name)

    def show_kernel_density(self, y_list, name):

        plot_kernel_density(self.values, y_list, name)

    def show_all(self, x_list, y_list, name, kernels):

        plot_on_one_graph(self.values, x_list, y_list, name, kernels)
