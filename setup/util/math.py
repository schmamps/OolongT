def mean(vals):
    value_sum = sum([float(val) for val in vals])
    count = len(vals)

    return value_sum / count


def median(vals):
    index = int(len(vals) / 2) - 1

    return sorted(vals)[index]
