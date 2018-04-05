from .stats import *
import math
import copy
import random
from statistics import median
from scipy.stats import norm, lognorm, triang


def normal_distrib(m, s, x):
    return 1 / (math.sqrt(2 * math.pi) * s) * math.exp(-(x - m) ** 2 / (2 * s ** 2))


def log_normal_distrib(m, s, x):
    return (1 / x) * (1 / (s * math.sqrt(2 * math.pi))) * math.exp(-(math.log(x, math.e) - m) ** 2 / (2 * s ** 2))


def log_normal_distrib_check(m, s, x):
    return lognorm.pdf(x, m, s)


def triangular_distrib():
    pass


def weibull_distrib():
    return True


class Estimator:

    def __init__(self, sample):
        self.values = sample

    def get_q_q_plot(self, sample, theory_params, name):
        sample_quantiles = []
        theory_quantiles = []
        m = Distribution(sample)
        for i in range(100):
            sample_quantiles.append(m.count_quintile(i / 100))
        theory_quantiles = get_quantiles([i / 100 for i in range(100)], theory_params[0], theory_params[1])
        q_q_biplot(sample_quantiles, theory_quantiles, name + '.png')

    # normal&lognormal distrib
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
        res_list_of_samples, mean, std = self.method_of_moments(list_of_samples, 'normal')
        self.show_result(res_list_of_samples, [i / 5 for i in range(130)], mean, std)
        for i in range(len(list_of_samples)):
            self.get_q_q_plot(list_of_samples[i], [mean[i], std[i]], 'qq_plot_' + str(i))

    def show_result(self,res_list_of_samples, int, mean, sd, type='normal'):
        arr = []
        for i in range(len(mean)):
            tmp_arr = []
            if type == 'normal':
                for x in int:
                    tmp_arr += [normal_distrib(mean[i], sd[i], x)]
                arr += [tmp_arr]
            else:
                for x in int:
                    tmp_arr += log_normal_distrib(mean[i], sd[i], x)
                arr += [tmp_arr]
        names = []
        for i in range(len(mean)):
            names += ['Gaussian' + str(i)]
        nbins = [17, 4, 17]
        for i in range(len(arr)):
            sample_plot(res_list_of_samples[i], int, arr[i], "Samples"+str(i)+"_div.png",nbins[i])
        plot_on_one_graph(self.values, int, arr, 'Samples_divided.png', names)

    def mlm(self, sample):
        m = Distribution(sample)
        mean = m.mean
        sd = m.count_biased_variance()


    def method_of_quintiles(self, sample, type='lognormal'):
        m = Distribution(sample)
        if type == 'lognormal':
            # median of the sample
            return math.log(median(sample)), math.log(m.count_quintile(0.25) / m.count_quintile(0.75)) / 1.35
        if type == 'normal':
            return

    def method_of_moments(self, list_of_samples, type='normal'):
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
                for i in ind.reverse():
                    del list_of_samples[ind]
            for sample in list_of_samples:
                m = Distribution(sample)
                mean += [m.mean]
                standard_dev += [m.standard_deviation]
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
                        if type == 'normal':
                            elem = normal_distrib(mean[t], standard_dev[t], sam)
                        if type == 'lognormal':
                            elem = log_normal_distrib(mean[t], standard_dev[t], sam)
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
        print("Estimated parameters with method of moments")
        for i in range(len(mean)):
            print("Sample", i, "mean:", mean[i], "sd:", standard_dev[i])
        return list_of_samples, mean, standard_dev

    def params_validation(self):
        return True
