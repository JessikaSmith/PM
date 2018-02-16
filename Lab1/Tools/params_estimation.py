from .vis import *
from .stats import *
import math
import copy


def normal_PDF(m, s, x):

    return 1/(math.sqrt(2*math.pi)*s)*math.exp(-(x-m)**2/(2*s**2))


class Estimator:

    def __init__(self, sample):

        self.values = sample

    # normal distrib
    def estimate_params(self, num_of_distrib):

        h = len(self.values)//num_of_distrib
        list_of_samples = []
        for i in range(0,len(self.values),h):
            list_of_samples += [self.values[i:i+h]]

        if len(list_of_samples) > num_of_distrib:
            m = list_of_samples[-1]
            del list_of_samples[-1]
            list_of_samples[-1] += m

        new_list_of_samples = []
        flag = True

        while flag:
            mean = []
            standard_dev = []
            ind = -1
            for i in range(len(list_of_samples)):
                if list_of_samples[i] == []:
                    ind = i

            if ind != -1:
                del list_of_samples[ind]

            for sample in list_of_samples:
                m = Distribution(sample)
                mean += [m.mean]
                standard_dev += [m.standard_deviation]

            new_list_of_samples = []

            for y in range(num_of_distrib):
                new_list_of_samples += [[]]
            k = len(mean)
            for i in range(k):
                list_samp = list_of_samples[i]
                for sam in list_samp:
                    find_max = -1000
                    ind = 0
                    for t in range(k):
                        elem = normal_PDF(mean[t],standard_dev[t],sam)
                        if elem > find_max:
                            ind = t
                            find_max = elem
                    new_list_of_samples[ind] += [sam]

            for i in range(num_of_distrib):
                list_of_samples[i].sort()
                new_list_of_samples[i].sort()
                if list_of_samples[i] == new_list_of_samples[i]:
                    flag = False
                else:
                    flag = True
            list_of_samples = copy.deepcopy(new_list_of_samples)
        print(list_of_samples)
        h = 1
        self.show_result(list_of_samples,h)


    # bad implementation
    def show_result(self,list_of_samples,h):

        y_list = []
        for t in range(len(list_of_samples)):
            y_list += [[]]

        for i in range(len(list_of_samples)):
            for x in list_of_samples[i]:
                r = 1/(len(list_of_samples[i])*h)
                sm = 0
                for j in list_of_samples[i]:
                    val = (x - j)
                    sm += kernel_gaussian(val / h)
                y_list[i] += [r + sm]

        names = []
        for i in range(len(y_list)):
            names += ['Gaussian'+str(i)]


        plot_on_one_graph(self.values, list_of_samples, y_list, 'Samples_divided.html', names)


