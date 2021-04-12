import numpy


class PageRankCalculator:

    def calc(matrix, v, e, n):
        return


def mult_matrix_on_const(matrix, b):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] *= b
    return matrix


def mult_matrix_on_vector(matrix, vector):
    length = len(matrix)
    result = [0 for i in range(length)]
    for i in range(length):
        count = 0
        for j in range(length):
            count += vector[j] * matrix[i][j]
        result[i] = count
    return result


def sum_of_vectors(v1, v2):
    v3 = [0 for i in range(len(v1))]
    for i in range(len(v1)):
        count = v1[i] + v2[i]
        v3[i] = count
    return v3


def calc(matrix, v, e, n):
    trasponent_matrix(matrix)
    const = (1 - 0.85) / n
    matrix = mult_matrix_on_const(matrix, 0.85)
    b = [y * const for y in e]
    for i in range(20):
        v = mult_matrix_on_vector(matrix, v)
        v = sum_of_vectors(v, b)
    return v


def trasponent_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i < j:
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
