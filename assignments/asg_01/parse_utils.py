import re


def map_capture_to_coefficient(capture):
    if capture == '':
        return 1
    if capture == '+':
        return 1
    if capture == '-':
        return -1
    if capture.startswith('+'):
        return float(capture.lstrip('+'))
    if capture.startswith('-'):
        return -float(capture.lstrip('-'))
    return float(capture)


def get_regex_for_line(line):
    regex = ''
    first = True
    for unknown in ['x', 'y', 'z']:
        if unknown in line:
            optional_sign = '?' if first else ''
            regex += r'([\+\-]' + optional_sign + r'\d*\.?\d*)' + unknown
            first = False
    return regex + r'=([\+\-]?\d*\.?\d*)'


def parse_equation(path):
    with open(path, 'r') as fd:
        lines = [line.replace('\n', '').replace(' ', '')
                 for line in fd.readlines()]

        # regex = r'([\+\-]?\d*\.?\d*)x([\+\-]\d*\.?\d*)y([\+\-]\d*\.?\d*)z=([\+\-]?\d*\.?\d*)'

        raw_coefficients = []
        for line in lines:
            res = re.search(get_regex_for_line(line), line)
            factors = []
            index = 0
            groups = list(res.groups())
            for unknown in ['x', 'y', 'z']:
                if unknown in line:
                    factors.append(groups[index])
                    index += 1
                else:
                    factors.append('0')
            factors.append(groups[-1])
            raw_coefficients.append(factors)

        output = []
        for line in raw_coefficients:
            output.append([map_capture_to_coefficient(c) for c in line])

        return output


print(parse_equation('input.txt'))
