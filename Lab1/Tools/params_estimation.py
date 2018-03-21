from .vis import *
from .stats import *
import math
import copy
import random


def normal_distrib(m, s, x):
    return 1 / (math.sqrt(2 * math.pi) * s) * math.exp(-(x - m) ** 2 / (2 * s ** 2))


def log_normal_distrib(m, s, x):
    1 / (x * s * math.sqrt(2 * math.pi)) * math.exp(-(math.log(x) - m) ** 2 / (2 * s ** 2))
    return True


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
            theory_quantiles.append(get_quantiles(theory_params[0], theory_params[1], i / 100))
        q_q_biplot(sample_quantiles, theory_quantiles, name + '.png')

    # normal distrib
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
        for i in range(len(list_of_samples)):
            self.get_q_q_plot(list_of_samples[i], [mean[i], std[i]], 'qq_plot_' + str(i))

        # print(res_list_of_samples)
        # h = 1
        # self.show_result(res_list_of_samples,h)

        # res_list_of_samples = self.method_of_moments(list_of_samples, 'lognormal')
        # print(res_list_of_samples)

    # bad implementation
    def show_result(self, list_of_samples, h):

        y_list = []
        for t in range(len(list_of_samples)):
            y_list += [[]]

        for i in range(len(list_of_samples)):
            for x in list_of_samples[i]:
                r = 1 / (len(list_of_samples[i]) * h)
                sm = 0
                for j in list_of_samples[i]:
                    val = (x - j)
                    sm += kernel_gaussian(val / h)
                y_list[i] += [r + sm]

        names = []
        for i in range(len(y_list)):
            names += ['Gaussian' + str(i)]

    def method_of_moments(self, list_of_samples, type='normal'):

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

                if type == 'normal':
                    mean += [m.mean]
                    standard_dev += [m.standard_deviation]
                if type == 'lognormal':
                    mean += [m.lognormal_mean]
                    standard_dev += [math.sqrt(m.lognormal_variance)]

            new_list_of_samples = []

            for y in range(len(list_of_samples)):
                new_list_of_samples += [[]]
            k = len(mean)

            for i in range(k):
                list_samp = list_of_samples[i]
                for sam in list_samp:
                    find_max = -1000
                    ind = 0
                    for t in range(k):

                        if type == 'normal':
                            elem = normal_distrib(mean[t], standard_dev[t], sam)
                        if type == 'lognormal':
                            elem = log_normal_distrib(mean[t], standard_dev[t], sam)

                        if elem > find_max:
                            ind = t
                            find_max = elem
                    new_list_of_samples[ind] += [sam]

            for i in range(len(list_of_samples)):
                list_of_samples[i].sort()
                new_list_of_samples[i].sort()
                if list_of_samples[i] == new_list_of_samples[i]:
                    flag = False
                else:
                    flag = True

            list_of_samples = copy.deepcopy(new_list_of_samples)

        return list_of_samples, mean, standard_dev

    def params_validation(self):
        return True

        # plot_on_one_graph(self.values, list_of_samples, y_list, 'Samples_divided.png', names)
