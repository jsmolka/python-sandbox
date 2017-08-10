class Matrix:
    def __init__(self, matrix):
        """Constructor"""
        self.__matrix = matrix
        if not self.__validate():
            raise Exception("Invalid matrix")

    def __getitem__(self, item):
        """Better indexing for getting"""
        if type(item) != tuple or len(item) != 2:
            raise IndexError("Index must be a tuple")
        r, c = item
        if 0 <= r < len(self.__matrix) and 0 <= c < len(self.__matrix[0]):
            return self.__matrix[r][c]
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, key, value):
        """Better indexing for setting"""
        if type(key) != tuple or len(key) != 2:
            raise IndexError("Index must be a tuple")
        r, c = key
        if 0 <= r < len(self.__matrix) and 0 <= c < len(self.__matrix[0]):
            self.__matrix[r][c] = value
        else:
            raise IndexError("Index out of range")

    def __add__(self, other):
        """Adds matrices"""
        if not type(other) != Matrix:
            raise ArithmeticError("Invalid type")
        return self.__add(other)

    def __sub__(self, other):
        """Subtracts matrices"""
        if type(other) != Matrix:
            raise ArithmeticError("Invalid type")
        return self.__subtract(other)

    def __mul__(self, other):
        """Multiplies matrices"""
        if type(other) != Matrix and type(other) != int and type(other) != float:
            raise ArithmeticError("Invalid type")
        if type(other) == Matrix:
            return self.__multiply(other)
        if type(other) == (int or float):
            return self.__multiply_scalar(other)

    def __rmul__(self, other):
        """Multiplies matrices reversely"""
        return self.__mul__(other)  # Use scalar from both sides

    @property
    def row_count(self):
        """Returns row count"""
        return len(self.__matrix)

    @property
    def col_count(self):
        """Returns col count"""
        return len(self.__matrix[0])

    @property
    def regular(self):
        """Checks if matrix is regular"""
        return self.__regular()

    @property
    def singular(self):
        """Checks if matrix is singular"""
        return self.__singular()

    @property
    def determinant(self):
        """Returns determinant"""
        return self.__determinant()

    @property
    def rank(self):
        """Returns rank"""
        return self.__rank()

    @property
    def __is_row(self):
        """Checks if matrix is a row"""
        return True if len(self.__matrix) == 1 else False

    @property
    def __is_col(self):
        """Checks if matrix is a column"""
        return True if len(self.__matrix[0]) == 1 else False

    @property
    def __is_square(self):
        """Checks if matrix is square matrix"""
        return True if len(self.__matrix) == len(self.__matrix[0]) else False

    def __validate(self):
        """Validates matrix"""
        if not (type(self.__matrix) and type(self.__matrix[0])) == list:
            return False

        length = self.col_count
        for row in self.__matrix:
            if len(row) != length:
                return False
        return True

    @staticmethod
    def create(rows, cols, default=0, unit=False):
        """Creates (r x c) matrix with default values or unit matrix"""
        if (rows or cols) <= 0:
            raise Exception("Invalid row or column count")

        if not unit:  # Empty matrix
            result = list()
            for r in range(0, rows):
                result.append(list())
                for c in range(0, cols):
                    result[r].append(default)
            return Matrix(result)
        else:  # Unit matrix
            result = Matrix.create(rows, cols)
            for r in range(0, rows):
                for c in range(0, cols):
                    result[r, c] = 0 if r != c else 1
            return result

    def print_rows(self):
        """Prints matrix in rows"""
        for row in self.__matrix:
            print(row)

    def duplicate(self):
        """Duplicates matrix"""
        result = Matrix.create(self.row_count, self.col_count)
        for r in range(0, result.row_count):
            for c in range(0, result.col_count):
                result[r, c] = self[r, c]
        return result

    def transpose(self):
        """Transposes matrix"""
        result = Matrix.create(self.col_count, self.row_count)
        for r in range(0, result.row_count):
            for c in range(0, result.col_count):
                result[c, r] = self[r, c]
        return result

    def __add(self, matrix):
        """Adds matrices"""
        if not self.row_count == matrix.row_count:
            raise Exception("Different row count")
        if not self.col_count == matrix.col_count:
            raise Exception("Different column count")

        result = self.duplicate()
        for r in range(0, result.row_count):
            for c in range(0, result.col_count):
                result[r, c] += matrix[r, c]
        return result

    def __subtract(self, matrix):
        """Subtracts matrices"""
        if not self.row_count == matrix.row_count:
            raise Exception("Different row count")
        if not self.col_count == matrix.col_count:
            raise Exception("Different column count")

        result = self.duplicate()
        for r in range(0, result.row_count):
            for c in range(0, result.col_count):
                result[r, c] -= matrix[r, c]
        return result

    def __multiply(self, matrix):
        """Multiplies matrices"""
        if not self.row_count == matrix.col_count:
            raise Exception("Different row / column count")
        if not self.col_count == matrix.row_count:
            raise Exception("Different row / column count")

        result = self.duplicate()
        for r in range(0, result.row_count):
            for c in range(0, matrix.col_count):
                sum_ = 0
                for i in range(0, result.col_count):
                    sum_ += result[r, i] * matrix[i, c]
                result[r, c] = sum_
        return result

    def __multiply_scalar(self, scalar):
        """Multiplies matrix with a scalar"""
        result = self.duplicate()
        for r in range(0, result.row_count):
            for c in range(0, result.col_count):
                result[r, c] *= scalar
        return result

    def __determinant(self, result=0):
        """Calculates determinant recursively"""
        if not self.__is_square:
            raise Exception("No square matrix")

        if self.row_count == 1:
            result += self[0, 0]
        else:
            for r in range(0, self.row_count):
                matrix = self.duplicate()
                for c in range(0, self.col_count):  # Delete first column
                    del matrix.__matrix[c][0]
                del matrix.__matrix[r]  # Delete r-th row
                # Multiply sign and factor for deleted row / column with smaller determinant
                result += pow(-1, r + 2) * self[r, 0] * Matrix.__determinant(matrix)
        return result

    def __regular(self):
        """Checks if matrix is regular"""
        # Regular matrix = invertible square matrix (determinant != 0)
        if self.__is_square:
            return True if self.determinant() != 0 else False
        else:
            return False

    def __singular(self):
        """Checks if matrix is singular"""
        # Singular matrix = not invertible square matrix (determinant == 0)
        if self.__is_square:
            return True if self.determinant() == 0 else False
        else:
            return False

    def __add_rows(self, row1, row2):
        """Adds rows"""
        for c in range(0, self.col_count):
            self[row2, c] += self[row1, c]

    def __add_external_row(self, row, ex_row):
        """Adds external row"""
        if not self.col_count == ex_row.col_count:
            raise Exception("Different column count")

        for c in range(0, self.col_count):
            self[row, c] += ex_row[0, c]

    def __change_rows(self, row1, row2):
        """Changes rows"""
        self.__matrix[row1], self.__matrix[row2] = self.__matrix[row2], self.__matrix[row1]

    def __duplicate_row(self, row):
        """Duplicates row"""
        row_ = Matrix.create(1, self.col_count)
        for c in range(0, self.col_count):
            row_[0, c] = self[row, c]
        return row_

    def __multiply_row_scalar(self, row, scalar):
        """Multiplies row with a scalar"""
        for c in range(0, self.col_count):
            self[row, c] *= scalar

    def gauss(self, round_=True, digits=8):
        """Creates lower triangular matrix using Gaussian elimination"""
        if self.__is_row or self.__is_col:
            raise Exception("Gaussian elimination is not defined for row or column matrices")

        result = self.duplicate()
        for r in range(0, result.row_count):
            if result[r, r] == 0:  # Change rows to eliminate zero
                if r < result.row_count - 1:  # Check if it is the last line
                    for r2 in range(r + 1, result.row_count):  # Check all lower rows
                        if result[r2, r] != 0:
                            result.__change_rows(r, r2)  # Change with row without zero
                            break
                        if r2 == result.row_count - 1:  # Check if last line is reached
                            return
                else:
                    return  # Return if it is the last line
            result.__multiply_row_scalar(r, 1 / result[r, r])  # [r, r] in row to 1
            for r2 in range(r + 1, result.row_count):  # Add base row to lower rows
                if result[r2, r] != 0:  # Checks if row is zero already
                    result.__multiply_row_scalar(r2, (-1) / result[r2, r])  # [r2, r] in target row to -1
                    result.__add_rows(r, r2)
        if round_:
            for r in range(0, result.row_count):
                for c in range(0, result.col_count):
                    result[r, c] = round(result[r, c], digits)
        return result

    def gauss_jordan(self, round_=True, digits=8):
        """Creates lower and upper triangular matrix using Gauss-Jordan elimination"""
        if self.__is_row or self.__is_col:
            raise Exception("Gauss-Jordan elimination is not defined for row or column matrices")

        result = self.gauss(round_=False)

        for r in range(result.row_count - 1, -1, -1):  # Reverse gauss
            for c in range(r - 1, -1, -1):
                row = result.__duplicate_row(r)  # Duplicate base row
                row.multiply_scalar((-1) * result[c, r])  # Multiply with negative value above
                result.__add_external_row(c, row)  # Add to get zero
        if round_:
            for r in range(0, result.row_count):
                for c in range(0, result.col_count):
                    result[r, c] = round(result[r, c], digits)
        return result

    def __combine(self, matrix):
        """Combines two matrices"""
        if not self.row_count == matrix.row_count:
            raise Exception("Different row count")

        result = Matrix.create(self.row_count, self.col_count + matrix.col_count)
        for r in range(0, result.row_count):
            for c in range(0, result.col_count):
                result[r, c] = self[r, c]
                result[r, c + matrix.col_count] = matrix[r, c]
        return result

    def invert(self, round_=True, digits=8):
        """Inverts matrix"""
        if not self.__is_square:
            raise Exception("No square matrix")
        if not self.regular:
            raise Exception("Is not regular")

        result = self.duplicate()
        unit = Matrix.create(result.row_count, result.row_count, unit=True)
        combined = result.__combine(unit)
        combined.gauss_jordan(round_=round_, digits=digits)
        for r in range(0, result.row_count):  # Cut out old matrix
            for c in range(0, result.col_count):
                result[r, c] = combined[r, c + result.col_count]
        return result

    def __rank(self):
        """Calculates rank"""
        if self.__is_row:
            return 1

        rank = self.row_count
        matrix = self.duplicate()
        matrix.gauss()
        for r in range(0, matrix.row_count):
            for c in range(0, matrix.col_count):
                if matrix[r, c] != 0:  # Check if element is unequal to zero
                    break  # Continue with next line
                if c == matrix.col_count - 1:  # Count rank down if whole line is zero
                    rank -= 1
        return rank
