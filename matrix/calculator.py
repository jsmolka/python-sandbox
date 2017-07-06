import dialog
import draw
from matrix import *


def print_menu():
    """Prints the menu"""
    draw.line()
    draw.menu("Choose your action:",
              "Determinant, rank, regular or singular",
              "Transpose",
              "Add",
              "Subtract",
              "Multiply",
              "Gauss algorithm",
              "Gauss Jordan algorithm",
              "Invert",
              "Exit")
    draw.line()


def determinant_function(matrix):
    """Determinant and other things"""
    draw.line()
    det = matrix.determinant()
    print("Determinant:", det)
    rank = matrix.rank()
    print("Rank:", rank)
    if matrix.singular():
        print("Matrix is singular")
    if matrix.regular():
        print("Matrix is regular")
    dialog.enter("continue")


def transpose_function(matrix):
    """Transposing a matrix"""
    draw.line()
    transpose_matrix = matrix.duplicate()
    transpose_matrix.transpose()
    print("Transposed matrix:")
    transpose_matrix.print_rows()
    dialog.enter("continue")


def add_function(matrix):
    """Adds matrices"""
    draw.line()
    print("Input matrix to add!")
    add_matrix = Matrix(input())
    add_matrix.print_rows()
    matrix.add(add_matrix)
    print("Result:")
    matrix.print_rows()
    dialog.enter("continue")
    return matrix


def subtract_function(matrix):
    """Subtracts matrices"""
    draw.line()
    print("Input matrix to subtract!")
    subtract_matrix = Matrix(input())
    subtract_matrix.print_rows()
    matrix.subtract(subtract_matrix)
    print("Result:")
    matrix.print_rows()
    dialog.enter("continue")
    return matrix


def multiply_function(matrix):
    """Multiplies matrices"""
    draw.line()
    print("Input matrix to multiply!")
    multiply_matrix = Matrix(input())
    multiply_matrix.print_rows()
    matrix.multiply(multiply_matrix)
    print("Result:")
    matrix.print_rows()
    dialog.enter("continue")
    return matrix


def gauss_function(matrix):
    """Uses gauss algorithm"""
    draw.line()
    round_results = dialog.yes_no("Round the results?")
    if round_results:
        matrix.gauss()
    else:
        matrix.gauss(False)
    print("Result:")
    matrix.print_rows()
    dialog.enter("continue")


def gauss_jordan_function(matrix):
    """Uses gauss jordan algorithm"""
    draw.line()
    round_results = dialog.yes_no("Round the results?")
    if round_results:
        matrix.gauss_jordan()
    else:
        matrix.gauss_jordan(False)
    print("Result:")
    matrix.print_rows()
    dialog.enter("continue")


def invert_function(matrix):
    """Uses gauss jordan algorithm"""
    draw.line()
    round_results = dialog.yes_no("Round the results?")
    if round_results:
        matrix.invert()
    else:
        matrix.invert(False)
    print("Result:")
    matrix.print_rows()
    dialog.enter("continue")


print("Enter your matrix:")
main_matrix = Matrix(input())
main_matrix.print_rows()
try:
    while True:
        print_menu()
        choice = dialog.user_input(1, 10, create_range=True)
        if choice == 1:
            determinant_function(main_matrix)
        if choice == 2:
            transpose_function(main_matrix)
        if choice == 3:
            main_matrix = add_function(main_matrix)
        if choice == 4:
            main_matrix = subtract_function(main_matrix)
        if choice == 5:
            main_matrix = multiply_function(main_matrix)
        if choice == 6:
            gauss_function(main_matrix)
        if choice == 7:
            gauss_jordan_function(main_matrix)
        if choice == 8:
            invert_function(main_matrix)
        if choice == 9:
            dialog.enter("exit")
            break
except Exception as e:
    print(str(e))
    input()
