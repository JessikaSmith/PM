import scipy.stats
import numpy as np
import math
from .vis import *


def normal_distrib(m, s, x):
    return 1 / (math.sqrt(2 * math.pi) * s) * math.exp(-(x - m) ** 2 / (2 * s ** 2))


class Simulator:

    def __init__(self, res_list_of_samples, list_of_means, list_of_stds):
        self.samples = res_list_of_samples
        self.means = list_of_means
        self.stds = list_of_stds

    def sample_boxmiller(self, iter=0):
        array_of_vals = []
        for i in range(len(self.samples)):
            num = 0
            tmp_min = min(self.samples[i])
            tmp_max = max(self.samples[i])
            while (num < len(self.samples[i])):
                u = np.random.uniform(0, 1, 2)
                x = math.cos(2 * np.pi * u[0]) * math.sqrt(-2 * math.log(u[1]))
                s = self.means[i] + self.stds[i]*x
                if s >= tmp_min and s <= tmp_max:
                    array_of_vals += [s]
                    num += 1
            plot_histogram(array_of_vals, 'boxmiller_estimation' + str(iter) + '.png')

    def method_of_inverse_function(self, iter=0):
        array_of_vals = []
        for i in range(len(self.samples)):
            num = 0
            tmp_min = min(self.samples[i])
            tmp_max = max(self.samples[i])
            while (num < len(self.samples[i])):
                s = np.random.normal(self.means[i], self.stds[i], 1)[0]
                if s >= tmp_min and s <= tmp_max:
                    array_of_vals += [s]
                    num += 1
        plot_histogram(array_of_vals, 'inverse_func_estimation' + str(iter) + '.png')

    def geometrical_method(self, iter=0):
        array_of_vals = []
        for i in range(len(self.samples)):
            num = 0
            tmp_min = min(self.samples[i])
            tmp_max = max(self.samples[i])
            min_prob = 0
            max_prob = normal_distrib(self.means[i], self.stds[i], self.means[i])
            while (num < len(self.samples[i])):
                x = np.random.uniform(low=tmp_min, high=tmp_max+1, size=1)[0]
                y = np.random.uniform(low=min_prob, high=max_prob, size=1)[0]
                if y <= normal_distrib(self.means[i], self.stds[i], x):
                    array_of_vals += [x]
                    num += 1
        plot_histogram(array_of_vals, 'geometrical_estimation' + str(iter) + '.png')
