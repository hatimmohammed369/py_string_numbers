def split_number(a):
    if not isinstance(a, str):
        raise TypeError('non-string value for parameter (a),'
                        ' parameter (a) type:'+str(type(a)))

    if len(a) == 0:
        a = '0.0'

    if not a.__contains__('.'):
        a = a + '.0'

    decimal_point_index = a.find('.')
    return [a[0:decimal_point_index], decimal_point_index, a[decimal_point_index+1:]]


def remove_zeros_from(s, where):
    if not isinstance(s, str):
        raise TypeError('non-string value for parameter (s), parameter (s) type:'+str(type(s)))

    if not isinstance(where, str):
        raise TypeError('non-string value for parameter (where), parameter (where) type:'+str(type(where)))

    if where != 'left' and where != 'right':
        raise ValueError('(where) is (left) or (right) only:'+where)

    if len(s) == s.count('0'):
        return '0'

    if where == 'left' and s.startswith('0'):
        for i in range(0, len(s)):
            if s[i] != '0':
                return s[i:]

    if where == 'right' and s.endswith('0'):
        for i in range(len(s)-1, -1, -1):
            if s[i] != '0':
                return s[0:i+1]
    return s


def remove_all_zeros(s, is_number):
    if not isinstance(s, str):
        raise TypeError('non-string value for parameter (s),  parameter (s) type:'+str(type(s)))

    if not isinstance(is_number, bool):
        raise TypeError('non-bool value for parameter (is_number), '
                        'parameter (is_number) type:'+str(type(is_number)))

    if is_number:
        l = split_number(s)
        l[0] = remove_zeros_from(l[0], 'left')
        l[2] = remove_zeros_from(l[2], 'right')
        return l[0] + '.' + l[2]
    return remove_zeros_from(remove_zeros_from(s, 'right'), 'left')


def number_string_type(s):
    if not isinstance(s, str):
        raise TypeError('non-string value for parameter (s), parameter (s) type:'+str(type(s)))

    if len(s) == 0:
        raise ValueError('empty string (s)')

    def is_real_number_string(s):
        if not isinstance(s, str):
            raise TypeError('non-string value for parameter (s), parameter (s) type:' + str(type(s)))

        if len(s) == 0:
            raise ValueError('empty string (s)')

        for c in s:
            if (c != '+') and (c != '-') and (c != '.') and \
                    (c != '0') and (c != '1') and (c != '2') and \
                    (c != '3') and (c != '4') and (c != '5') and \
                    (c != '6') and (c != '7') and (c != '8') and (c != '9'):
                return False
        return True

    if s.__contains__('.') and is_real_number_string(s):
        return 'R'

    if not s.__contains__('.') and is_real_number_string(s):
        return 'Z'

    return 'non-numeric'


def fill(s, where, length):
    if not isinstance(s, str):
        raise TypeError('non-string value for parameter (s), parameter (s) type:'+str(type(s)))

    if not isinstance(where, str):
        raise TypeError('non-string value for parameter (where), parameter (where) type::'+str(type(where)))

    if not isinstance(length, int):
        raise TypeError('non-integer value for parameter (length),'
                        ' parameter (length) type:'+str(type(length)))

    if where != 'left' and where != 'right':
        raise ValueError('(where) is (left) or (right) only:'+where)

    if length < len(s):
        raise ValueError('length can not be less than '+str(len(s)))

    while True:
        if len(s) == length:
            return s
        if where == 'left':
            s = '0' + s
        else:
            s = s + '0'


def realize_fill(a, int_part_length, decimal_part_length):
    if not isinstance(a, str):
        raise TypeError('non-string value for parameter (a), parameter (a) type:' + str(type(a)))

    if number_string_type(a) == 'non-numeric':
        raise ValueError('string ' + a + ' contains non-numeric characters')

    if len(a) == 0:
        return ( int_part_length * '0' ) + '.' + ( decimal_part_length * '0' )
    l = split_number(a)
    l[0] = fill(l[0], 'left', int_part_length)
    l[2] = fill(l[2], 'right', decimal_part_length)
    return l[0] + '.' + l[2]


def compare(a, b):
    if not isinstance(a, str):
        raise TypeError('non-string value for parameter (a), parameter (a) type:'+str(type(a)))

    if not isinstance(b, str):
        raise TypeError('non-string value for parameter (b), parameter (b) type:'+str(type(b)))

    if len(a) == 0:
        raise ValueError('empty string (a)')

    if len(b) == 0:
        raise ValueError('empty string (b)')

    if number_string_type(a) == 'non-numeric':
        raise ValueError('string ' + a + ' contains non-numeric characters')

    if number_string_type(b) == 'non-numeric':
        raise ValueError('string ' + b + ' contains non-numeric characters')

    a_negative = a.startswith('-')
    if a_negative:
        a = a[1:]

    b_negative = b.startswith('-')
    if b_negative:
        b = b[1:]

    if not a.__contains__('.'):
        a = a + '.0'
    if not b.__contains__('.'):
        b = b + '.0'

    a = remove_all_zeros(a, True)
    b = remove_all_zeros(b, True)

    if a == '0.0' and b == '0.0':
        return 0
    elif a == '0.0' and b != '0.0':
        return 1 if b_negative else -1
    elif b == '0.0' and a != '0.0':
        return -1 if a_negative else 1

    if not a_negative and b_negative:
        return 1
    elif a_negative and not b_negative:
        return -1

    a_decimal_point_index = a.find('.')
    b_decimal_point_index = b.find('.')
    int_max = max( len(a[0:a_decimal_point_index]) , len(b[0:b_decimal_point_index]) )
    decimal_max = max( len(a[a_decimal_point_index+1:]) , len(b[b_decimal_point_index+1:]) )
    a = realize_fill(a, int_max, decimal_max)
    b = realize_fill(b, int_max, decimal_max)

    def compare_int(n, m):
        for i in range(0, len(n)):
            n_digit = int(n[i])
            m_digit = int(m[i])
            if n_digit < m_digit:
                return -1
            elif n_digit > m_digit:
                return 1
        return 0

    la = split_number(a)
    lb = split_number(b)
    int_compare = compare_int(la[0], lb[0])
    if int_compare == -1:  # |a| < |b|
        return 1 if a_negative else -1
    elif int_compare == 1:  # |a| > |b|
        return -1 if a_negative else 1

    decimal_compare = compare_int(la[2], lb[2])
    if decimal_compare == -1:  # |a| < |b|
        return 1 if a_negative else -1
    elif decimal_compare == 1:  # |a| > |b|
        return -1 if a_negative else 1
    return 0


def add(a, b):
    if not isinstance(a, str):
        raise TypeError('non-string value for parameter (a), parameter (a) type:'+str(type(a)))

    if not isinstance(b, str):
        raise TypeError('non-string value for parameter (b), parameter (b) type:'+str(type(b)))

    if len(a) == 0:
        raise ValueError('empty string (a)')

    if len(b) == 0:
        raise ValueError('empty string (b)')

    if number_string_type(a) == 'non-numeric':
        raise ValueError('string ' + a + ' contains non-numeric characters')

    if number_string_type(b) == 'non-numeric':
        raise ValueError('string ' + b + ' contains non-numeric characters')

    a_negative = a.startswith('-')
    if a_negative:
        a = a[1:]

    b_negative = b.startswith('-')
    if b_negative:
        b = b[1:]

    if not a.__contains__('.'):
        a = a + '.0'
    if not b.__contains__('.'):
        b = b + '.0'

    a = remove_all_zeros(a, True)
    b = remove_all_zeros(b, True)

    if a == '0.0' and b == '0.0':
        return '0.0'
    elif a == '0.0' and b != '0.0':
        return ('-' if b_negative else '') + b
    elif b == '0.0' and a != '0.0':
        return ('-' if a_negative else '') + a

    a_decimal_point_index = a.find('.')
    b_decimal_point_index = b.find('.')
    int_max = max(len(a[0:a_decimal_point_index]), len(b[0:b_decimal_point_index]))
    decimal_max = max(len(a[a_decimal_point_index + 1:]), len(b[b_decimal_point_index + 1:]))
    a = realize_fill(a, int_max, decimal_max)
    b = realize_fill(b, int_max, decimal_max)

    result = ''
    if a_negative == b_negative:
        carry = 0
        for i in range(len(a)-1, -1, -1):
            if a[i] == '.':
                result = '.' + result
                continue
            x = str(carry + int(a[i]) + int(b[i]))
            if i == 0:
                result = x + result
                break
            if len(x) == 1:
                x = '0' + x
            result = x[1] + result
            carry = int(x[0])
        return (a_negative * '-') + remove_all_zeros(result, True)

    c = compare(a, b)
    sign = ((c == 1 and a_negative) or (c == -1 and b_negative)) * '-'

    if c == -1:  # |a| < |b|
        a, b = b, a

    a_map = {}
    for i in range(0, len(a)):
        if a[i] == '.':
            continue
        a_map[i] = int(a[i])

    for i in range(len(a)-1, -1, -1):
        if a[i] == '.':
            result = '.' + result
            continue
        a_digit = a_map[i]
        b_digit = int(b[i])
        if a_digit >= b_digit:
            result = str(a_digit - b_digit) + result
        else:
            for j in range(i, -1, -1):
                if a[j] == '.':
                    continue
                if j == i:
                    a_map[j] = a_map[j] + 10
                    result = str(a_map[j] - b_digit) + result
                elif a_map[j] == 0:
                    a_map[j] = a_map[j] + 9
                elif a_map[j] != 0:
                    a_map[j] = a_map[j] - 1
                    break
    return sign + remove_all_zeros(result, True)


def sub(a, b):
    if b.startswith('-'):
        b = b[1:]
    else:
        b = '-' + b
    return add(a, b)


def mul(a, b):
    if not isinstance(a, str):
        raise TypeError('non-string value for parameter (a), parameter (a) type:'+str(type(a)))

    if not isinstance(b, str):
        raise TypeError('non-string value for parameter (b), parameter (b) type:'+str(type(b)))

    if len(a) == 0:
        raise ValueError('empty string (a)')

    if len(b) == 0:
        raise ValueError('empty string (b)')

    if number_string_type(a) == 'non-numeric':
        raise ValueError('string ' + a + ' contains non-numeric characters')

    if number_string_type(b) == 'non-numeric':
        raise ValueError('string ' + b + ' contains non-numeric characters')

    a_negative = a.startswith('-')
    if a_negative:
        a = a[1:]

    b_negative = b.startswith('-')
    if b_negative:
        b = b[1:]

    sign = (a_negative != b_negative) * '-'

    if not a.__contains__('.'):
        a = a + '.0'
    if not b.__contains__('.'):
        b = b + '.0'

    if compare(a, '0') == 0 or compare(b, '0') == 0:
        return '0.0'

    a = remove_all_zeros(a, True)
    la = split_number(a)
    n = 0
    if la[2] == '0':
        for i in range(len(la[0])-1, -1, -1):
            if (la[0])[i] != '0':
                break
            n = n + 1
    if la[2] != '0':
        n = -len(la[2])

    b = remove_all_zeros(b, True)
    lb = split_number(b)
    m = 0
    if lb[2] == '0':
        for i in range(len(lb[0]) - 1, -1, -1):
            if (lb[0])[i] != '0':
                break
            m = m + 1
    if lb[2] != '0':
        m = -len(lb[2])

    exponent = n + m

    a = remove_all_zeros(a.replace('.', ''), False)
    b = remove_all_zeros(b.replace('.', ''), False)

    c = compare(a, b)
    if c == -1:  # |a| < |b|
        b, a = a, b

    result = '0'
    if a == '1' or b == '1':
        result = a if b == '1' else b
    else:
        for i in range(0, len(b)):
            if b[i] == '.' or b[i] == '0':
                continue
            b_digit = int(b[i])
            inner_carry = 0
            inner_result = (len(b) - (i + 1)) * '0'

            for j in range(len(a)-1, -1, -1):
                if a[j] == '.':
                    continue
                x = str(inner_carry + b_digit * int(a[j]))
                if len(x) == 1:
                    x = '0' + x
                inner_result = x[1] + inner_result
                inner_carry = int(x[0])
            inner_result = ((inner_carry != 0) * str(inner_carry)) + inner_result
            result = add(result, inner_result)
        result = remove_zeros_from(result[0:result.find('.')], 'left')

    if exponent > 0:
        return sign + remove_all_zeros(result + (exponent * '0') + '.0', True)
    elif exponent < 0:
        exponent = -exponent
        if len(result) <= exponent:
            return remove_all_zeros(sign + '0.' + fill(result, 'left', exponent), True)

        for i in range(len(result)-1, -1, -1):
            if (len(result) - (i + 1)) == exponent:
                result = sign + result[0:i+1] + '.' + result[i+1:]
                if not result.__contains__('.'):
                    result = result + '.0'
                return remove_all_zeros(result, True)
    return sign + result + '.0'


def int_reciprocal(n, decimal_part_length):
    if not isinstance(n, str):
        raise TypeError('parameter (n) must be of type str, provided type:'+str(type(n)))

    if number_string_type(n) != 'Z' or n.__contains__('-') or n.__contains__('.'):
        raise TypeError('string '+n+' is not a positive integer string')

    if not isinstance(decimal_part_length, int):
        raise TypeError('parameter (decimal_part_length) must be of type int,'
                        ' provided type:' + str(type(decimal_part_length)))

    if decimal_part_length < 0:
        raise ValueError('parameter (decimal_part_length) must be a positive integer')

    negative = n.startswith('-')
    if negative:
        n = n[1:]
    n = remove_zeros_from(n, 'left')
    if n == '0':
        raise ZeroDivisionError()

    if n == '1':
        return (negative * '-') + '1.0'

    one = '1'
    result = ''
    while True:
        if len(result) > decimal_part_length or one == '0':
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
        one = remove_all_zeros(one, True)
        if one.__contains__('.'):
            one = one[0:one.find('.')]
        result = result + r


def div(a, b, decimal_part_length):
    if not isinstance(a, str):
        raise TypeError('non-string value for parameter (a), parameter (a) type:'+str(type(a)))

    if not isinstance(b, str):
        raise TypeError('non-string value for parameter (b), parameter (b) type:'+str(type(b)))

    if len(a) == 0:
        raise ValueError('empty string (a)')

    if len(b) == 0:
        raise ValueError('empty string (b)')

    if number_string_type(a) == 'non-numeric':
        raise ValueError('string ' + a + ' contains non-numeric characters')

    if number_string_type(b) == 'non-numeric':
        raise ValueError('string ' + b + ' contains non-numeric characters')

    a_negative = a.startswith('-')
    if a_negative:
        a = a[1:]

    b_negative = b.startswith('-')
    if b_negative:
        b = b[1:]

    if not a.__contains__('.'):
        a = a + '.0'
    if not b.__contains__('.'):
        b = b + '.0'

    a = remove_all_zeros(a, True)
    b = remove_all_zeros(b, True)

    if b == '0.0':
        raise ZeroDivisionError()

    sign = (a_negative != b_negative) * '-'
    if b == '1.0':
        return sign + a

    if a == '0.0':
        return '0.0'

    if a[a.find('.')+1:] == '0' and b[b.find('.')+1:] == '0':
        a = a[0:a.find('.')]
        b = b[0:b.find('.')]
        div_list = floordiv(a, b)
        return add(div_list[0], mul(div_list[1], int_reciprocal(b, decimal_part_length)) )


    b_decimal_part = b[b.find('.')+1:]
    if b_decimal_part == '0':
        b = b[0:b.find('.')]
        return sign + mul(a, int_reciprocal(b, decimal_part_length))

    new_decimal_part_length = len(b_decimal_part)
    if b[0:b.find('.')] == '0':
        b = b[b.find('.')+1:]
    else:
        b = b.replace('.', '')
    return sign + mul(div(a, b, decimal_part_length) , '1' + (new_decimal_part_length * '0'))


def floordiv(dividend, divisor):
    """
    Division of 2 positive integers
    :return: a list of the form [integer result, remainder]
    """
    if divisor == '0':
        raise ZeroDivisionError()

    if compare(dividend, divisor) == -1:  # dividen < divisor, e.g. 2/3
        return ['0', dividend]

    if dividend == '0':
        return ['0', '0']

    if divisor == '1':
        return [dividend, '0']

    if dividend == divisor:
        return ['1', '0']

    exp = 0
    dividend_first_non_zero_value_index_from_left = len(dividend) - 1
    divisor_first_non_zero_value_index_from_left = len(divisor) - 1
    if dividend.endswith('0') or divisor.endswith('0'):
        dividend_exponent = 0
        for i in range(len(dividend)-1, -1, -1):
            if dividend[i] != '0':
                dividend_first_non_zero_value_index_from_left = i
                break
            dividend_exponent += 1

        divisor_exponent = 0

        for i in range(len(divisor)-1, -1, -1):
            if divisor[i] != '0':
                divisor_first_non_zero_value_index_from_left = i
                break
            divisor_exponent += 1

        exp = dividend_exponent - divisor_exponent
        del dividend_exponent, divisor_exponent

    if exp >= 0:  # things like 10000/100, which equals 100/1
        if dividend_first_non_zero_value_index_from_left != len(dividend) - 1:
            dividend = dividend[0:dividend_first_non_zero_value_index_from_left + 1] + (exp * '0')
        if divisor_first_non_zero_value_index_from_left != len(divisor) - 1:
            divisor = divisor[0:divisor_first_non_zero_value_index_from_left + 1]
        del dividend_first_non_zero_value_index_from_left, divisor_first_non_zero_value_index_from_left
        if divisor == '1':
            return [dividend, '0']


    # things like 9999/100, exp = -2
    # exp < 0, division must be done manually
    del exp

    result = ''
    dividend_copy = dividend
    x = dividend_copy[0]
    index = 0

    while True:
        if compare(x, divisor) == -1:
            result = result + '0'
            if index + 1 < len(dividend_copy):
                x = x + dividend_copy[index+1]
        else:
            r = '0.0'
            while compare(x, divisor) != -1:
                x = add(x, '-' + divisor)
                r = add(r, '1')
            r = r[0:r.find('.')]
            x = x[0:x.find('.')]
            if x == '0':
                x = ''
            result = result + r
            if index + 1 < len(dividend_copy):
                x = x + dividend_copy[index + 1]
        index += 1
        if index == len(dividend_copy):
            return [remove_zeros_from(result, 'left'), remove_zeros_from(x, 'left')]