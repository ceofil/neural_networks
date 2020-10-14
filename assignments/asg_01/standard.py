from parse_utils import parse_equation


def get_determinant2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]


def get_determinant3(matrix):
    a, b, c = matrix[0][:3]
    d, e, f = matrix[1][:3]
    g, h, i = matrix[2][:3]
    return a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h


def get_transpose_matrix(matrix):
    n = range(len(matrix))
    return [
        [matrix[x][y] for x in n] for y in n
    ]


def get_cofactor(matrix, i, j):
    n = range(len(matrix))
    mat2x2 = [
        [matrix[y][x] for x in n if not x == j] for y in n if not y == i
    ]
    factor = 1 if i % 2 == j % 2 else -1
    return factor * get_determinant2(mat2x2)


def get_adjoint_matrix(matrix):
    n = range(len(matrix))
    cofactor_matrix = [
        [get_cofactor(matrix, y, x) for x in n] for y in n
    ]
    return get_transpose_matrix(cofactor_matrix)


def get_inverse_matrix(matrix):
    n = range(len(matrix))
    determinant = get_determinant3(matrix)

    if determinant:
        adjoint_matrix = get_adjoint_matrix(matrix)
        return [
            [adjoint_matrix[y][x] / determinant for x in n] for y in n
        ]
    else:
        return False


def multiply(m1, m2):
    h1, w1 = range(len(m1)), range(len(m1[0]))
    h2, w2 = range(len(m2)), range(len(m2[0]))
    assert w1 == h2, 'invalid matrix dimnesions'
    return[
        [sum([a*b for a, b in zip(m1[i], [m2[row][j] for row in h2])]) for j in w2] for i in h1
    ]


def solve(path):
    equation = parse_equation(path)
    a = [line[:3] for line in equation]
    b = [[line[-1]] for line in equation]

    inverse_a = get_inverse_matrix(a)

    return multiply(inverse_a, b)


print(solve('input.txt'))
