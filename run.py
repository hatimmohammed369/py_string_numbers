from arithmetic import *
from math import e as euler_number


def int_reciprocal(n, decimal_part_length):
    if not isinstance(n, str):
        raise TypeError('argument (n) must be of type str, provided type:'+str(type(n)))

    if number_string_type(n) != 'Z' or n.__contains__('-') or n.__contains__('.'):
        raise TypeError('string '+n+' is not a positive integer string')

    if not isinstance(decimal_part_length, int):
        raise TypeError('argument (decimal_part_length) must be of type int,'
                        ' provided type:' + str(type(decimal_part_length)))

    if decimal_part_length < 0:
        raise ValueError('argument (decimal_part_length) must be a positive integer')

    negative = n.startswith('-')
    if negative:
        n = n[1:]
    n = remove_zeros_from(n, 'left')
    if compare(n, '0') == 0:
        raise ZeroDivisionError()

    if compare(n, '1') == 0:
        return (negative * '-') + '1.0'

    one = '1'
    result = ''
    while True:
        if len(result) > decimal_part_length or compare(one, '0') == 0:
            return (negative * '-') + '0.' + result[0:decimal_part_length+1]

        zeros = 0
        while compare(one, n) == -1:  # while one < n
            one = one + '0'
            zeros = zeros + 1
        result = result + ((zeros-1) * '0')

        r = '0.0'
        while compare(one, n) != -1:
            one = sub(one, n)
            r = add(r, '1')
        r = r[0:r.find('.')]
        if one.__contains__('.'):
            one = one[0:one.find('.')]
        result = result + r


def real_reciprocal(x, decimal_part_length):
    if not isinstance(x, str):
        raise TypeError('argument (x) must be of type str, provided type:' + str(type(x)))

    if number_string_type(x) == 'non-numeric':
        raise TypeError('string ' + x + ' is not a numeric string')

    if not isinstance(decimal_part_length, int):
        raise TypeError('argument (decimal_part_length) must be of type int,'
                        ' provided type:' + str(type(decimal_part_length)))

    if decimal_part_length < 0:
        raise ValueError('argument (decimal_part_length) must be a positive integer')

    sign = ''
    negative = x.startswith('-')
    if negative:
        x = x[1:]
        sign = '-'
    x = remove_all_zeros(x, True)
    if compare(x, '1') == 0:
        return sign + '1.0'

    result_exponent = 0
    x_decimal_part = x[x.find('.')+1:]
    if x_decimal_part == '0':
        x = x[0:x.find('.')]
        return sign + int_reciprocal(x, decimal_part_length)
    else:
        x = remove_zeros_from(x.replace('.', ''), 'left')
        result_exponent = len(x_decimal_part)

    reciprocal = int_reciprocal(x, decimal_part_length)

    if reciprocal == '1.0':
        reciprocal = '1'
    else:
        reciprocal = reciprocal[2:]

    if reciprocal != '1':
        result_exponent = -len(reciprocal) + result_exponent

    print()
    if result_exponent > 0:
        return sign + reciprocal + (result_exponent * '0') + '.0'

    elif result_exponent < 0:
        result_exponent = -result_exponent
        if len(reciprocal) <= result_exponent:
            return sign + '0.' + fill(reciprocal, 'left', result_exponent)
        else:
            for i in range(0, len(reciprocal)):
                if len(reciprocal) - (i+1) == result_exponent:
                    return sign + reciprocal[0:i+1] + '.' + reciprocal[i+1:]

    return sign + reciprocal + '.0'


def fac(n):
    if n.__contains__('.'):
        n = n[0:n.find('.')]
    assert isinstance(n, str) and (number_string_type(n) == 'Z' and not n.__contains__('-'))
    return '1' if (compare(n, '1') == 0 or compare(n, '0') == 0) else mul(n, fac(sub(n, '1')))


N = 0.0017
print(1/N)
print(real_reciprocal(str(N), 10))