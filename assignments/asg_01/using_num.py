from parse_utils import parse_equation
import numpy as np


def solve(path):
    equation = parse_equation(path)
    a = np.array([line[:3] for line in equation])
    b = np.array([[line[-1]] for line in equation])

    if not np.linalg.det(a):
        print('det=0')
    return np.linalg.inv(a).dot(b)


print(solve('input.txt'))
