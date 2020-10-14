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


def get_determinant_leibinz(matrix):
    a, b, c = matrix[0][:3]
    d, e, f = matrix[1][:3]
    g, h, i = matrix[2][:3]
    return a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h


def get_transpose_matrix(matrix):
    n = range(len(matrix))
    return [
        [matrix[x][y] for x in n] for y in n
    ]


matrix = [
    [3, 2, 1],
    [6, 5, 4],
    [9, 8, 7]


]


print(get_determinant_leibinz(matrix))

for i in get_transpose_matrix(matrix):
    print(i)
