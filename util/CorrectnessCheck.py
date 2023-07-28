def true_rate(array1, array2):
    count = sum([1 for a, b in zip(array1, array2) if a == b])
    result = count / len(array1)
    percentage = round(result * 100, 4)
    return f"{percentage}%"