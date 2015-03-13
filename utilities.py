import numpy as np

def reduced_chi_sq(model, data, errors):
    if not len(model) == len(data) == len(errors):
        return np.nan
    chi_sq = 0
    for i in range(len(model)):
        chi_sq += ((model[i] - data[i])/errors[i])**2
    return chi_sq/(len(data))