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


def parse_equation(path):
    with open(path, 'r') as fd:
        lines = [line.replace('\n', '').replace(' ', '')
                 for line in fd.readlines()]

        regex = r'([\+\-]?\d*\.?\d*)x([\+\-]\d*\.?\d*)y([\+\-]\d*\.?\d*)z=([\+\-]?\d*\.?\d*)'

        raw_coefficients = []
        for line in lines:
            res = re.search(regex, line)
            a, b, c, r = res.groups()
            raw_coefficients.append([a, b, c, r])

        output = []
        for line in raw_coefficients:
            output.append([map_capture_to_coefficient(c) for c in line])

        return output


# for testing purposes
expected = [
    [2.0, 3, 3.14, 0],
    [1, 0, -2, -2.3],
    [-1.1234, -0.524, 1, 3]
]

result = parse_equation('input.txt')

print(expected)
print(result)
print(result == expected)
