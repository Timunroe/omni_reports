def humanize_number(value, fraction_point=1):
    powers = [10 ** x for x in (12, 9, 6, 3, 0)]
    human_powers = ('T', 'B', 'M', 'K', '')
    is_negative = False
    if not isinstance(value, float):
        value = float(value)
    if value < 0:
        is_negative = True
        value = abs(value)
    for i, p in enumerate(powers):
        if value >= p:
            return_value = str(round(value / (p / (10.0 ** fraction_point))) /
                               (10 ** fraction_point)) + human_powers[i]
            break
    if is_negative:
        return_value = "-" + return_value
    # remove pesky situation where xXX.0 occurs
    return_value = return_value.replace('.0', '')

    return return_value


def diff(new, old, kind=None):
    # takes in numbers
    # kinds: none (just subtraction), % is (new-old)/old, %90 (new-(old/90)/(old/90))
    # returns a formatted string
    if kind == '%90':
        if old == 0:
            result = 'NA'
        else:
            result = ((new - (old / 90)) / (old / 90))
            result = "{:+.1%}".format(result)
    else:
        result = new - old
        result = "{:+.1}".format(result)
    return result


def percent(partial, total):
    # takes in numbers
    # returns formatted string
    result = (partial / total)
    result = "{:.1%}".format(result)
    return result
