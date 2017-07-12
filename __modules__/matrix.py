class Matrix:
    def __init__(self, matrix):
        """Constructor"""
        if type(matrix) == str:
            self.__build(matrix)
        else:
            self.matrix = matrix
        if self.__validate():
            self.__update()
        else:
            self.matrix = []
            print("Matrix is not valid")

    def __build(self, matrix_string):
        """Builds matrix out of a string"""
        matrix_string = matrix_string.replace(" ", "")
        if "|" in matrix_string:
            matrix_string = matrix_string.replace("|", "],[")
            matrix_string = "[[{0}]]".format(matrix_string)
        else:
            matrix_string = "[{0}]".format(matrix_string)
        try:
            matrix = eval(matrix_string)
            self.matrix = matrix
        except Exception as e:
            print(str(e))

    def __validate(self):
        """Validates matrix"""
        try:
            if type(self.matrix[0]) == list:
                row_length = len(self.matrix[0])
                for i in range(0, len(self.matrix)):
                    if row_length != len(self.matrix[i]):
                        print("Invalid matrix")
                        return False
                return True
            else:
                return True
        except Exception as e:
            print(str(e))
            return False

    def __update(self):
        """Updates matrix properties"""
        if type(self.matrix[0]) != list:  # Row
            self.__row = True
            self.__col = False
            self.row_count = 1
            self.col_count = len(self.matrix)
        elif type(self.matrix[0]) == list and len(self.matrix[0]) == 1:  # Column
            self.__col = True
            self.__row = False
            self.row_count = len(self.matrix)
            self.col_count = 1
        else:  # Matrix
            self.__row = False
            self.__col = False
            self.row_count = len(self.matrix)
            self.col_count = len(self.matrix[0])

    @staticmethod
    def create(m, n, unit_matrix=False):
        """Creates empty (m x n) matrix or a unit matrix"""
        if m > 0 and n > 0:
            if not unit_matrix:
                if m == 1:  # Row
                    matrix = list()
                    for i in range(0, n):
                        matrix.append(None)
                else:  # Matrix / column
                    matrix = list()
                    for i in range(0, m):
                        matrix.append(list())
                        for j in range(0, n):
                            matrix[i].append(None)
                matrix = Matrix(matrix)
                return matrix
            else:  # Unit matrix
                matrix = Matrix.create(m, n)
                for i in range(0, m):
                    for j in range(0, n):
                        if i != j:
                            matrix.matrix[i][j] = 0
                        else:
                            matrix.matrix[i][j] = 1
                return matrix
        else:
            if m <= 0:
                print("Row count cannot be", m)
            if n <= 0:
                print("Column count cannot be", n)

    def print_rows(self):
        """Prints matrix in rows"""
        try:
            if not self.__row:  # Matrix / column
                m = self.row_count
                for i in range(0, m):
                    print(self.matrix[i])
            else:  # Row
                print(self.matrix)
        except Exception as e:
            print(str(e))

    def duplicate(self, row_number=None):
        """Creates copy"""
        if row_number is None:
            if not self.__row:  # Matrix / column
                m = self.row_count
                n = self.col_count
                return_matrix = Matrix.create(m, n)
                for i in range(0, m):
                    for j in range(0, n):
                        return_matrix.matrix[i][j] = self.matrix[i][j]
            else:  # Row
                n = self.col_count
                return_matrix = Matrix.create(1, n)
                for i in range(0, n):
                    return_matrix.matrix[i] = self.matrix[i]

            return return_matrix

        else:  # Specific row
            n = len(self.matrix[row_number])
            return_row = Matrix.create(1, n)
            for i in range(0, n):
                return_row.matrix[i] = self.matrix[row_number][i]

            return return_row

    def transpose(self):
        """Transposes matrix"""
        if not self.__row:
            m = self.row_count
            n = self.col_count
            trans_matrix = Matrix.create(n, m)
            if not self.__col:  # Matrix
                for i in range(0, m):
                    for j in range(0, n):
                        trans_matrix.matrix[j][i] = self.matrix[i][j]
                self.matrix = trans_matrix.matrix
            else:  # Column
                for i in range(0, m):
                    trans_matrix.matrix[i] = self.matrix[i][0]
                self.matrix = trans_matrix.matrix
        else:  # Row
            n = self.col_count
            trans_matrix = Matrix.create(n, 1)
            for i in range(0, n):
                trans_matrix.matrix[i][0] = self.matrix[i]
            self.matrix = trans_matrix.matrix

        self.__update()

    def add(self, matrix):
        """Adds matrices"""
        if not self.__row and not matrix.__row:  # Matrix / column
            m1 = self.row_count
            m2 = matrix.row_count
            n1 = self.col_count
            n2 = matrix.col_count
            if m1 == m2 and n1 == n2:
                for i in range(0, m1):
                    for j in range(0, n1):
                        self.matrix[i][j] = self.matrix[i][j] + matrix.matrix[i][j]
            else:
                print("Cannot add")
                print("Different row or column count")
                print("Self: {0} rows and {1} columns".format(m1, n1))
                print("Matrix: {0} rows and {1} columns".format(m2, n2))
                self.matrix = []
        else:  # Row
            n1 = self.col_count
            n2 = matrix.col_count
            if n1 == n2:
                for i in range(0, n1):
                    self.matrix[i] = self.matrix[i] + matrix.matrix[i]
            else:
                print("Cannot add")
                print("Different column count")
                print("Self: 1 row and {0} columns".format(n1))
                print("Matrix: 1 row and {0} columns".format(n2))
                self.matrix = []

    def subtract(self, matrix):
        """Subtracts matrices"""
        if not self.__row and not matrix.__row:  # Matrix / column
            m1 = self.row_count
            m2 = matrix.row_count
            n1 = self.col_count
            n2 = matrix.col_count
            if m1 == m2 and n1 == n2:
                for i in range(0, m1):
                    for j in range(0, n1):
                        self.matrix[i][j] = self.matrix[i][j] - matrix.matrix[i][j]
            else:
                print("Cannot subtract")
                print("Different row or column count")
                print("Self: {0} rows and {1} columns".format(m1, n1))
                print("Matrix: {0} rows and {1} columns".format(m2, n2))
                self.matrix = []
        else:
            n1 = self.row_count
            n2 = matrix.col_count
            if n1 == n2:  # Row
                for i in range(0, n1):
                    self.matrix[i] = self.matrix[i] - matrix.matrix[i]
            else:
                print("Cannot add")
                print("Different column count")
                print("Self: 1 row and {0} columns".format(n1))
                print("Matrix: 1 row and {0} columns".format(n2))
                self.matrix = []

    def multiply(self, matrix):
        """Multiplies matrices"""
        if not self.__row and not matrix.__row:  # Matrix
            m1 = self.row_count
            m2 = matrix.row_count
            n1 = self.col_count
            n2 = matrix.col_count
            if m1 == n2 and m2 == n1:
                result_matrix = Matrix.create(m1, m1)
                for i in range(0, m1):
                    for j in range(0, m1):
                        result = 0
                        for k in range(0, n1):
                            result += self.matrix[i][k] * matrix.matrix[k][j]
                        result_matrix.matrix[i][j] = result

                self.matrix = result_matrix.matrix
            else:
                print("Cannot multiply")
                print("Self row count unequal to matrix col count")
                print("Self: {0} rows and {1} columns".format(m1, n1))
                print("Matrix: {0} rows and {1} columns".format(m2, n2))
        else:
            if self.__col and matrix.__row:  # Column
                m1 = self.row_count
                n2 = matrix.col_count
                if m1 == n2:
                    result_matrix = Matrix.create(m1, m1)
                    for i in range(0, m1):
                        for j in range(0, m1):
                            result_matrix.matrix[i][j] = self.matrix[i][0] * matrix.matrix[j]

                    self.matrix = result_matrix.matrix
                else:
                    print("Cannot multiply")
                    print("Self row count unequal to matrix col count")
                    print("Self: {0} rows and 1 columns".format(m1))
                    print("Matrix: 1 rows and {0} columns".format(n2))

            elif self.__row and matrix.__col:  # Row
                n1 = self.col_count
                m2 = matrix.row_count
                if n1 == m2:
                    result_matrix = Matrix.create(1, 1)
                    result = 0
                    for i in range(0, n1):
                        result += self.matrix[i] * matrix.matrix[i][0]
                    result_matrix.matrix[0] = result

                    self.matrix = result_matrix.matrix
                else:
                    print("Cannot multiply")
                    print("Self row count unequal to matrix col count")
                    print("Self: 1 rows and {0} columns.".format(n1))
                    print("Matrix: {0} rows and 1 columns.".format(m2))
            else:
                if self.__row and matrix.__row:
                    print("Cannot multiply two rows")
                if self.__col and matrix.__col:
                    print("Cannot multiply two columns")

        self.__update()

    def multiply_scalar(self, scalar, row=None):
        """Multiplies matrix with a scalar"""
        if row is None:
            if not self.__row:  # Matrix / column
                m = self.row_count
                n = self.col_count
                for i in range(0, m):
                    for j in range(0, n):
                        self.matrix[i][j] *= scalar
            else:  # Row
                n = self.col_count
                for i in range(0, n):
                    self.matrix[i] *= scalar
        else:  # Specific row
            n = len(self.matrix[row])
            for i in range(0, n):
                self.matrix[row][i] = self.matrix[row][i] * scalar

    def __square_matrix(self):
        """Checks if matrix is square matrix"""
        if self.__row or self.__col:
            return False
        else:
            if self.row_count == self.col_count:
                return True
            else:
                return False

    def determinant(self, result=0):
        """Calculates determinant recursively"""
        if not self.__square_matrix():
            print("No square matrix")
            print("Cannot calculate the determinant")
            return
        self.__update()
        m = self.row_count
        if m == 1:
            result += self.matrix[0][0]
        else:
            for i in range(0, m):
                rec_matrix = self.duplicate()
                for j in range(0, m):  # Delete first column
                    del rec_matrix.matrix[j][0]
                del rec_matrix.matrix[i]  # Delete i row
                sign = pow(-1, i + 2)
                factor = self.matrix[i][0]  # Factor for deleted row and column
                result += factor * sign * Matrix.determinant(rec_matrix)

        return result

    def regular(self):
        """Checks if matrix is regular"""
        # regular matrix = invertible square matrix (determinant != 0)
        if self.__square_matrix():
            if self.determinant() != 0:
                return True
            else:
                return False
        else:
            print("Regular is only defined for square matrices")

    def singular(self):
        """Checks if matrix is singular"""
        # singular matrix = not invertible square matrix (determinant == 0)
        if self.__square_matrix():
            if Matrix.determinant(self) == 0:
                return True
            else:
                return False
        else:
            print("Singular is only defined for square matrices")

    def __add_rows(self, row1, row2, external_row=None):
        """Adds rows"""
        if external_row is None:  # Rows in matrix
            n = self.col_count
            for i in range(0, n):
                self.matrix[row2][i] = self.matrix[row1][i] + self.matrix[row2][i]
        else:  # Row in matrix and external row
            n1 = self.col_count
            n2 = len(external_row.matrix)
            if n1 == n2:
                help_row = Matrix.create(1, n1)
                for i in range(0, n1):
                    help_row.matrix[i] = self.matrix[row1][i] + external_row.matrix[i]
                self.matrix[row2] = help_row.matrix
            else:
                print("Different row length")
                print("Row 1 length:", n1)
                print("External row length:", n2)

    def __change_rows(self, row1, row2):
        """Changes rows"""
        list1 = self.matrix[row1]
        list2 = self.matrix[row2]
        self.matrix[row1] = list2
        self.matrix[row2] = list1

    def gauss(self, round_float=True, digits=8):
        """Creates lower triangular matrix with the gauss algorithm"""
        if not self.__row and not self.__col:  # Matrix
            try:
                m = self.row_count
                n = self.col_count
                for i in range(0, m):
                    if self.matrix[i][i] == 0:  # Change row to eliminate zero
                        if i < m - 1:  # Check if it is the last line
                            for k in range(i + 1, m):
                                if self.matrix[k][i] != 0:
                                    self.__change_rows(i, k)
                                    break
                                if k == m - 1:  # Check if last line is reached
                                    return  # Cancel if there is no line left
                        else:
                            return  # Cancel if it is the last line
                    self.multiply_scalar(1 / self.matrix[i][i], i)  # Matrix[i][i] to 1
                    for j in range(i + 1, m):  # Add base row to lower rows
                        if self.matrix[j][i] != 0:  # Checks if row is zero already
                            self.multiply_scalar((-1) / self.matrix[j][i], j)  # Make target row minus one
                            self.__add_rows(i, j)
                if round_float:
                    for i in range(0, m):
                        for j in range(0, n):
                            self.matrix[i][j] = round(self.matrix[i][j], digits)
            except Exception as e:
                print("Gauss failed")
                print("Error:", e)
        else:
            print("Gauss algorithm is not intended for rows or columns")

    def gauss_jordan(self, round_float=True, digits=8):
        """Creates lower and upper triangular matrix with the gauss jordan algorithm"""
        if not self.__row or not self.__col:  # Matrix
            self.gauss(False)
            try:
                m = self.row_count
                n = self.col_count
                for i in range(m - 1, -1, -1):  # Reverse gauss
                    for j in range(i - 1, -1, -1):
                        help_row = self.duplicate(i)  # Duplicate base row
                        help_row.multiply_scalar((-1) * self.matrix[j][i])  # Multiply with negative value above
                        self.__add_rows(j, j, help_row)  # Add to get zero
                if round_float:
                    for i in range(0, m):
                        for j in range(0, n):
                            self.matrix[i][j] = round(self.matrix[i][j], digits)

            except Exception as e:
                print("Gauss Jordan failed")
                print("Error:", e)
        else:
            print("Gauss jordan algorithm is not intended for rows or columns")

    def __combine(self, matrix):
        """Combines two matrices"""
        if not self.__row and not matrix.__row:  # Matrix / column
            m1 = self.row_count
            m2 = matrix.row_count
            n1 = self.col_count
            n2 = matrix.col_count
            if m1 == m2:
                return_matrix = Matrix.create(m1, n1 + n2)
                for i in range(0, m1):  # Add self
                    for j in range(0, n1):
                        return_matrix.matrix[i][j] = self.matrix[i][j]
                for i in range(0, m2):  # Add matrix
                    for j in range(n1, n1 + n2):
                        return_matrix.matrix[i][j] = matrix.matrix[i][j - n1]

                self.matrix = return_matrix.matrix
            else:
                print("Matrices cannot have a different row count")
                print("Self: {0} rows and {1} columns".format(m1, n1))
                print("Matrix: {0} rows and {1} columns".format(m2, n2))
        else:  # Row
            if self.__row and matrix.__row:
                n1 = self.col_count
                n2 = matrix.col_count
                return_matrix = Matrix.create(1, n1 + n2)
                for i in range(0, n1):  # Add self
                    return_matrix.matrix[i] = self.matrix[i]
                for i in range(n1, n1 + n2):  # Add matrix
                    return_matrix.matrix[i] = matrix.matrix[i - n1]

                self.matrix = return_matrix.matrix
            else:
                if self.__row:
                    m1 = 1
                    n1 = self.col_count
                else:
                    m1 = self.row_count
                    n1 = self.col_count
                if matrix.__row:
                    m2 = 1
                    n2 = matrix.col_count
                else:
                    m2 = matrix.row_count
                    n2 = matrix.col_count
                print("Matrices cannot row count")
                print("Self: {0} rows and {1} columns".format(m1, n1))
                print("Matrix: {0} rows and {1} columns".format(m2, n2))

        self.__update()

    def invert(self, round_float=True):
        """Inverts matrix"""
        if self.__square_matrix():
            if self.regular():
                m = self.row_count
                unit_matrix = Matrix.create(m, m, True)
                self.__combine(unit_matrix)
                self.gauss_jordan(round_float)
                return_matrix = Matrix.create(m, m)
                for i in range(0, m):  # Cut out old matrix
                    for j in range(0, m):
                        return_matrix.matrix[j][i] = self.matrix[j][i + m]
                self.matrix = return_matrix.matrix
            else:
                print("Only regular matrices can be inverted")
        else:
            print("Only square matrices can be inverted")

    def rank(self):
        """Calculates rank"""
        if not self.__row:
            rank_matrix = self.duplicate()
            rank_matrix.gauss()
            m = rank_matrix.row_count
            n = rank_matrix.col_count
            rank = m
            for i in range(0, m):
                for j in range(0, n):
                    if rank_matrix.matrix[i][j] != 0:  # Check if element is unequal to zero
                        break  # Continue with next line
                    if j == n - 1:  # Count rank down if whole line is zero
                        rank -= 1
            return rank
        else:
            return 1
