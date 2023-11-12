import pandas as pd

def standardize(data):
    # impute to [0,1]
    array = data.to_numpy()
    min_max = []

    # min-max
    for i in range(len(array)):
        max_x = max(array[i])
        min_x = min(array[i])
        temp_array = [round((j - min_x)/(max_x - min_x), 2) * 10 for j in array[i]]
        min_max.append(temp_array)


def sharp_increase(data):
    df = standardize(data)
    if (any((df < 1) & (df > 9))):
        return 1
    else:
        return 0


def sharp_drop(data):
    df = standardize(data)
    if (any((df < 1) & (df.shift(-1) > 9))):
        return 1
    else:
        return 0
    