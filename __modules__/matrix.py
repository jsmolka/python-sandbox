class Matrix:
    def __init__(self, matrix):
        """Constructor"""
        self.matrix = matrix
        if not self.__validate():
            raise Exception("Invalid matrix")

    def __validate(self):
        """Validates matrix"""
        if not (type(self.matrix) and type(self.matrix)) == list:
            return False

        length = len(self.matrix[0])
        for row in self.matrix:
            if len(row) != length:
                return False
        return True

    @property
    def row_count(self):
        """Returns row count"""
        return len(self.matrix)

    @property
    def col_count(self):
        """Returns col count"""
        return len(self.matrix[0])

    @property
    def __is_row(self):
        """Checks if matrix is a row"""
        return True if len(self.matrix) == 1 else False

    @property
    def __is_col(self):
        """Checks if matrix is a column"""
        return True if len(self.matrix[0]) == 1 else False

    @property
    def __is_square(self):
        """Checks if matrix is square matrix"""
        return True if len(self.matrix) == len(self.matrix[0]) else False

    @staticmethod
    def create(m, n, default=0, unit=False):
        """Creates empty (m x n) or unit matrix"""
        if (m or n) <= 0:
            raise Exception("Invalid row or column count")

        if not unit:  # Empty matrix
            matrix = list()
            for i in range(0, m):
                matrix.append(list())
                for j in range(0, n):
                    matrix[i].append(default)
            return Matrix(matrix)
        else:  # Unit matrix
            matrix = Matrix.create(m, n)
            for i in range(0, m):
                for j in range(0, n):
                    matrix.matrix[i][j] = 0 if i != j else 1
            return matrix

    def print_rows(self):
        """Prints matrix in rows"""
        for row in self.matrix:
            print(row)

    def duplicate(self):
        """Duplicates matrix"""
        matrix = Matrix.create(self.row_count, self.col_count)
        for i in range(0, self.row_count):
            for j in range(0, self.col_count):
                matrix.matrix[i][j] = self.matrix[i][j]
        return matrix

    def __duplicate_row(self, m):
        """Duplicates row"""
        row = Matrix.create(1, self.col_count)
        for i in range(0, self.col_count):
            row.matrix[i] = self.matrix[m][i]
        return row

    def transpose(self):
        """Transposes matrix"""
        matrix = Matrix.create(self.col_count, self.row_count)
        for i in range(0, self.row_count):
            for j in range(0, self.col_count):
                matrix.matrix[j][i] = self.matrix[i][j]
        self.matrix = matrix.matrix

    def add(self, matrix):
        """Adds matrices"""
        if not self.row_count == matrix.row_count:
            raise Exception("Different row count")
        if not self.col_count == matrix.col_count:
            raise Exception("Different column count")

        for i in range(0, self.row_count):
            for j in range(0, self.col_count):
                self.matrix[i][j] = self.matrix[i][j] + matrix.matrix[i][j]
        return self.duplicate()

    def subtract(self, matrix):
        """Subtracts matrices"""
        if not self.row_count == matrix.row_count:
            raise Exception("Different row count")
        if not self.col_count == matrix.col_count:
            raise Exception("Different column count")

        for i in range(0, self.row_count):
            for j in range(0, self.col_count):
                self.matrix[i][j] = self.matrix[i][j] - matrix.matrix[i][j]
        return self.duplicate()

    def multiply(self, matrix):
        """Multiplies matrices"""
        if not self.row_count == matrix.col_count:
            raise Exception("Different row / column count")
        if not self.col_count == matrix.row_count:
            raise Exception("Different row / column count")

        result = Matrix.create(self.row_count, self.row_count)
        for i in range(0, self.row_count):
            for j in range(0, self.row_count):
                for k in range(0, self.col_count):
                    result.matrix[i][j] += self.matrix[i][k] * matrix.matrix[k][j]
        self = result
        return self.duplicate()

    def multiply_scalar(self, scalar):
        """Multiplies matrix with a scalar"""
        for i in range(0, self.row_count):
            for j in range(0, self.col_count):
                self.matrix[i][j] *= scalar
        return self.duplicate

    def __multiply_row_scalar(self, m):
        """Multiplies row with a scalar"""
        for i in range(0, self.col_count):
            self.matrix[m][i] = self.matrix[m][i] * scalar
        return self.duplicate

    def determinant(self, result=0):
        """Calculates determinant recursively"""
        if not self.__is_square:
            raise Exception("No square matrix")

        if self.row_count == 1:
            result += self.matrix[0][0]
        else:
            for i in range(0, self.row_count):
                matrix = self.duplicate()
                for j in range(0, self.row_count):  # Delete first column
                    del matrix.matrix[j][0]
                del matrix.matrix[i]  # Delete i-th row
                # Multiply sign and factor for deleted row / column with smaller determinant
                result += pow(-1, i + 2) * self.matrix[i][0] * Matrix.determinant(matrix)
        return result

    def regular(self):
        """Checks if matrix is regular"""
        # regular matrix = invertible square matrix (determinant != 0)
        if self.__is_square:
            return True if self.determinant() != 0 else False
        else:
            return False

    def singular(self):
        """Checks if matrix is singular"""
        # singular matrix = not invertible square matrix (determinant == 0)
        if self.__is_square:
            return True if self.determinant() == 0 else False
        else:
            return False

    def __add_rows(self, m1, m2):
        """Adds rows"""
        for i in range(0, self.col_count):  # Add row m1 to row m2
            self.matrix[m2][i] += self.matrix[m1][i]

    def __add_external_row(self, m, row):
        """Adds external row"""
        if not self.col_count == row.col_count:
            raise Exception("Different column count")

        for i in range(0, self.col_count):
            self.matrix[m][i] += row.matrix[0][i]

    def __change_rows(self, m1, m2):
        """Changes rows"""
        self.matrix[m1], self.matrix[m2] = self.matrix[m2], self.matrix[m1]

    # TODO: Continue here!
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
