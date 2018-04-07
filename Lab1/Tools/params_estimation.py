from .stats import *
import math
import copy
import random
from statistics import median
from scipy.stats import norm, lognorm, triang
from Lab1.Tools import Simulator
import time


def normal_distrib(m, s, x):
    return 1 / (math.sqrt(2 * math.pi) * s) * math.exp(-(x - m) ** 2 / (2 * s ** 2))


def log_normal_distrib(m, s, x):
    return (1 / x) * (1 / (s * math.sqrt(2 * math.pi))) * math.exp(-(math.log(x, math.e) - m) ** 2 / (2 * s ** 2))


def log_normal_distrib_check(m, s, x):
    return lognorm.pdf(x, m, s)


class Estimator:

    def __init__(self, sample):
        self.values = sample

    def get_q_q_plot(self, sample, theory_params, name):
        sample_quantiles = []
        m = Distribution(sample)
        for i in range(100):
            sample_quantiles.append(m.count_quintile(i / 100))
        theory_quantiles = get_quantiles([i / 100 for i in range(100)], theory_params[0], theory_params[1])
        # q_q_biplot(sample_quantiles, theory_quantiles, name + '.png')
        q_q_biplot_test(sample, theory_params, name + '.png')

    def divide_subset(self, num_of_distrib):
        h = len(self.values) // num_of_distrib
        list_of_samples = []
        sample = self.values
        for i in range(num_of_distrib - 1):
            subs = random.sample(sample, h)
            list_of_samples += [subs]
            sample = [i for i in sample if i not in subs]
        list_of_samples += [sample]
        if len(list_of_samples) > num_of_distrib:
            m = list_of_samples[-1]
            del list_of_samples[-1]
            list_of_samples[-1] += m
        list_of_names = ["moments"] #, "mle", "quintiles"]
        for method in list_of_names:
            res_list_of_samples, mean, std = self.method_of_estimation(list_of_samples, method)
            self.show_result(res_list_of_samples, [i / 5 for i in range(130)], mean, std, method)
            for i in range(len(res_list_of_samples)):
                self.get_q_q_plot(res_list_of_samples[i], [mean[i], std[i]], 'qq_plot_' + method + str(i))

    def show_result(self, res_list_of_samples, int, mean, sd, method, type='normal'):
        arr = []
        for i in range(len(mean)):
            tmp_arr = []
            for x in int:
                tmp_arr += [normal_distrib(mean[i], sd[i], x)]
            arr += [tmp_arr]
        names = []
        for i in range(len(mean)):
            names += ['Gaussian' + str(i)]
        nbins = [17, 4, 17]
        if method == 'quintiles':
            nbins = [10, 10, 10]
        for i in range(3):
            sample_plot(res_list_of_samples[i], int, arr[i], "Samples" + str(i) + "_div" + "_" + method + ".png",
                        nbins[i])
        # plot_on_one_graph(self.values, int, arr, 'Samples_divided.png', names)
        if method == 'moments':
            s = Simulator(res_list_of_samples, mean, sd)
            for i in range(10):
                # s.method_of_inverse_function(i)
                # s.geometrical_method(i)
                s.sample_boxmiller(i)

    def method_of_estimation(self, list_of_samples, method='moments', type='normal'):
        """

        :param list_of_samples: list of lists
        :param type: type of distribution (normal or lognormal)
        :return: new division on samples (list of lists), mean, sd
        """

        flag = True
        while flag:
            mean = []
            standard_dev = []
            ind = []
            for i in range(len(list_of_samples)):
                if not list_of_samples[i]:
                    ind += [i]
            if ind != []:
                if len(ind) == 1:
                    del list_of_samples[ind[0]]
                elif len(ind) == 2:
                    del list_of_samples[ind[-1]]
                    del list_of_samples[ind[0]]
            for sample in list_of_samples:
                m = Distribution(sample)
                if method == "moments":
                    mean += [m.mean]
                    standard_dev += [m.standard_deviation]
                if method == "mle":
                    mean += [m.mean]
                    standard_dev += [m.biased_variance ** (1 / 2)]
                if method == "quintiles":
                    standard_dev += [m.iqr / 1.34]
                    mean += [m.count_quintile(0.75) - (0.67 * (m.iqr / 1.34))]
            new_list_of_samples = []
            for y in range(len(list_of_samples)):
                new_list_of_samples += [[]]
            k = len(mean)
            for i in range(k):
                list_samp = list_of_samples[i]
                for sam in list_samp:
                    find_max = -float(math.inf)
                    ind = 0
                    for t in range(k):
                        elem = normal_distrib(mean[t], standard_dev[t], sam)
                        if elem > find_max:
                            ind, find_max = t, elem
                    new_list_of_samples[ind] += [sam]
            for i in range(len(list_of_samples)):
                list_of_samples[i].sort()
                new_list_of_samples[i].sort()
                if list_of_samples[i] == new_list_of_samples[i]:
                    flag = False
                else:
                    flag = True
            list_of_samples = copy.deepcopy(new_list_of_samples)
        print("Estimated parameters with " + method)
        for i in range(len(mean)):
            print("Sample", i, "mean:", mean[i], "sd:", standard_dev[i])
        return list_of_samples, mean, standard_dev