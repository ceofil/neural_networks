from parse_utils import parse_equation
import numpy as np


def solve(path):
    equation = np.array(parse_equation(path))
    a = equation[:3, :3]
    b = equation[:3, 3]

    if not np.linalg.det(a):
        print('det=0')
    return np.linalg.inv(a).dot(b)


print(solve('input.txt'))
