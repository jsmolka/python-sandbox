class MatrixError(MatrixError):
    def __init__(self, err):
        super(MatrixError, self).__init__(err)


class Matrix:
    def __init__(self, matrix):
        """
        Constructor.

        :param matrix: matrix
        :return: new Matrix instance
        """
        self._matrix = matrix
        if not self._validate():
            raise MatrixError("Invalid matrix")

    def __getitem__(self, item):
        """
        Numpy-like indexing.

        :param item: index
        :return: value at index
        """
        if isinstance(item, int):
            if 0 <= item < self.row_count:
                return self._matrix[item]
            raise IndexError("Index out of range")
        if isinstance(item, tuple):
            if len(item) != 2:
                raise IndexError("Invalid tuple length")
            r, c = item
            if 0 <= r < self.row_count and 0 <= c < self.col_count:
                return self._matrix[r][c]
            raise IndexError("Index out of range")
        raise IndexError("Index must be tuple or int")

    def __setitem__(self, key, value):
        """
        Numpy-like indexing.

        :param key: index to set
        :param value: value to set index to
        :return: None
        """
        if isinstance(key, int):
            if 0 <= key < self.row_count:
                self._matrix[key] = value
            raise IndexError("Index out of range")
        if isinstance(key, tuple):
            if len(key) != 2:
                raise IndexError("Invalid tuple length")
            r, c = key
            if 0 <= r < self.row_count and 0 <= c < self.col_count:
                self._matrix[r][c] = value
            raise IndexError("Index out of range")
        raise IndexError("Index must be tuple or int")

    def __add__(self, other):
        """
        Adds matrices.

        :param other: other matrix
        :return: Matrix
        """
        if not isinstance(other, Matrix):
            raise ArithmeticError("Invalid type")
        return self._add(other)

    def __sub__(self, other):
        """
        Subtracts matrices.

        :param other: other matrix
        :return: Matrix
        """
        if not isinstance(other, Matrix):
            raise ArithmeticError("Invalid type")
        return self._subtract(other)

    def __mul__(self, other):
        """
        Multiplies matrices.

        :param other: other matrix
        :return: Matrix
        """
        if isinstance(other, Matrix):
            return self._multiply(other)
        if isinstance(other, int) or isinstance(other, float):
            return self._multiply_scalar(other)
        raise ArithmeticError("Invalid type")

    def __rmul__(self, other):
        """
        Multiplies matrices reversely.

        :param other: other matrix
        :return: Matrix
        """
        return self.__mul__(other)  # Use scalar from both sides

    @property
    def row_count(self):
        """
        Returns row count.

        :return: int
        """
        return len(self._matrix)

    @property
    def col_count(self):
        """
        Returns col count.

        :return: int
        """
        return len(self[0])

    @property
    def regular(self):
        """
        Checks if matrix is regular.

        :return: boolean
        """
        return self._regular()

    @property
    def singular(self):
        """
        Checks if matrix is singular.

        :return: boolean
        """
        return self._singular()

    @property
    def determinant(self):
        """
        Returns determinant.

        :return: float or int
        """
        return self._determinant()

    @property
    def rank(self):
        """
        Returns rank.

        :return: int
        """
        return self._rank()

    @property
    def is_row(self):
        """
        Checks if matrix is a row.

        :return: boolean
        """
        return self.row_count == 1

    @property
    def is_col(self):
        """
        Checks if matrix is a column.

        :return: boolean
        """
        return self.col_count == 1

    @property
    def square(self):
        """
        Checks if matrix is square matrix.

        :return: boolean
        """
        return self.row_count == self.col_count

    def _validate(self):
        """
        Validates matrix.

        :return: boolean
        """
        if not (isinstance(self._matrix, list) and isinstance(self[0], list)):
            return False
        for row in self._matrix:
            if len(row) != self.col_count:
                return False
        return True

    @staticmethod
    def create(rows, cols, default=0, unit=False):
        """
        Creates (r x c) matrix with default values or unit matrix.

        :param rows: row count
        :param cols: column count
        :param default: fill value
        :param unit: create unit matrix
        :return: new Matrix
        """
        if rows <= 0 or cols <= 0:
            raise MatrixError("Invalid row or column count")
        if not unit:  # Empty matrix
            result = list()
            for r in range(rows):
                result.append(list())
                for c in range(cols):
                    result[r].append(default)
            return Matrix(result)
        else:  # Unit matrix
            result = Matrix.create(rows, cols)
            for r in range(rows):
                for c in range(cols):
                    result[r, c] = 0 if r != c else 1
            return result

    def print_rows(self):
        """
        Prints matrix in rows.

        :return: None
        """
        for row in self._matrix:
            print(row)

    def duplicate(self):
        """
        Duplicates matrix.

        :return: duplicated Matrix
        """
        return Matrix(self._matrix[:])

    def transpose(self):
        """
        Transposes matrix.

        :return: transposed Matrix
        """
        result = Matrix.create(self.col_count, self.row_count)
        for r in range(result.row_count):
            for c in range(result.col_count):
                result[c, r] = self[r, c]
        return result

    def _add(self, other):
        """
        Adds matrices.

        :param other: other matrix
        :return: added Matrix
        """
        if self.row_count != other.row_count or self.col_count != other.col_count:
            raise MatrixError("Different row or column count")
        result = self.duplicate()
        for r in range(0, result.row_count):
            for c in range(0, result.col_count):
                result[r, c] += other[r, c]
        return result

    def _subtract(self, other):
        """
        Subtracts matrices.

        :param other: other matrix
        :return: subtracted Matrix
        """
        if self.row_count != other.row_count or self.col_count != other.col_count:
            raise MatrixError("Different row or column count")
        result = self.duplicate()
        for r in range(0, result.row_count):
            for c in range(0, result.col_count):
                result[r, c] -= other[r, c]
        return result

    def _multiply(self, other):
        """
        Multiplies matrices.

        :param other: other matrix
        :return: multiplied Matrix
        """
        if self.row_count != other.col_count or self.col_count != other.row_count:
            raise MatrixError("Different row or column count")
        result = self.duplicate()
        for r in range(result.row_count):
            for c in range(other.col_count):
                sum_ = 0
                for i in range(result.col_count):
                    sum_ += result[r, i] * other[i, c]
                result[r, c] = sum_
        return result

    def _multiply_scalar(self, scalar):
        """
        Multiplies matrix with a scalar.

        :param scalar: scalar to multiply
        :return: multiplied Matrix
        """
        result = self.duplicate()
        for r in range(result.row_count):
            for c in range(result.col_count):
                result[r, c] *= scalar
        return result

    def _determinant(self, result=0):
        """
        Calculates determinant recursively.

        :param result: final result
        :return: int
        """
        if not self.square:
            raise MatrixError("No square matrix")
        if self.row_count == 1:
            result += self[0, 0]
        else:
            for r in range(self.row_count):
                matrix = self.duplicate()
                for c in range(self.col_count):  # Delete first column
                    del matrix._matrix[c][0]
                del matrix._matrix[r]  # Delete r-th row
                # Multiply sign and factor for deleted row / column with smaller determinant
                result += pow(-1, r + 2) * self[r, 0] * Matrix._determinant(matrix)
        return result

    def _regular(self):
        """
        Checks if matrix is regular.

        :return: boolean
        """
        # Regular matrix = invertible square matrix (determinant != 0)
        if self.square:
            return self.determinant != 0
        return False

    def _singular(self):
        """
        Checks if matrix is singular.

        :return: boolean
        """
        # Singular matrix = not invertible square matrix (determinant == 0)
        if self.square:
            return self.determinant == 0
        else:
            return False

    def _add_rows(self, row1, row2):
        """
        Adds rows.

        :param row1: first row index
        :param row2: second row index
        :return: None
        """
        for c in range(self.col_count):
            self[row2, c] += self[row1, c]

    def _add_external_row(self, row, ex_row):
        """
        Adds external row.

        :param row: row index
        :param ex_row: external row
        :return: None
        """
        if self.col_count != ex_row.col_count:
            raise MatrixError("Different column count")
        for c in range(self.col_count):
            self[row, c] += ex_row[0, c]

    def _change_rows(self, row1, row2):
        """
        Changes rows.

        :param row1: first row index
        :param row2: second row index
        :return: None
        """
        self[row1], self[row2] = self[row2], self[row1]

    def _duplicate_row(self, row):
        """
        Duplicates row.

        :param row: row index
        :return: new Matrix
        """
        result = Matrix.create(1, self.col_count)
        for c in range(self.col_count):
            result[0, c] = self[row, c]
        return result

    def _multiply_row_scalar(self, row, scalar):
        """
        Multiplies row with a scalar.

        :param row: row index
        :param scalar: scalar to multiply
        :return: None
        """
        for c in range(self.col_count):
            self[row, c] *= scalar

    def gauss(self, rnd=True, digits=8):
        """
        Creates lower triangular matrix using Gaussian elimination.

        :param rnd: round result
        :param digits: digits to round to
        :return: Matrix
        """
        if self.is_row or self.is_col:
            raise MatrixError("Gaussian elimination is not defined for row or column matrices")

        result = self.duplicate()
        for r in range(result.row_count):
            if result[r, r] == 0:  # Change rows to eliminate zero
                if r < result.row_count - 1:  # Check if it is the last line
                    for r2 in range(r + 1, result.row_count):  # Check all lower rows
                        if result[r2, r] != 0:
                            result._change_rows(r, r2)  # Change with row without zero
                            break
                        if r2 == result.row_count - 1:  # Check if last line is reached
                            return
                else:
                    return  # Return if it is the last line
            result._multiply_row_scalar(r, 1 / result[r, r])  # [r, r] in row to 1
            for r2 in range(r + 1, result.row_count):  # Add base row to lower rows
                if result[r2, r] != 0:  # Checks if row is zero already
                    result._multiply_row_scalar(r2, (-1) / result[r2, r])  # [r2, r] in target row to -1
                    result._add_rows(r, r2)
        if rnd:
            for r in range(result.row_count):
                for c in range(result.col_count):
                    result[r, c] = round(result[r, c], digits)
        return result

    def gauss_jordan(self, rnd=True, digits=8):
        """
        Creates lower and upper triangular matrix using Gauss-Jordan elimination.

        :param rnd: round result
        :param digits: digits to round to
        :return: Matrix
        """
        if self.is_row or self.is_col:
            raise MatrixError("Gauss-Jordan elimination is not defined for row or column matrices")

        result = self.gauss(rnd=False)

        for r in range(result.row_count - 1, -1, -1):  # Reverse gauss
            for c in range(r - 1, -1, -1):
                row = result._duplicate_row(r)  # Duplicate base row
                row.multiply_scalar((-1) * result[c, r])  # Multiply with negative value above
                result._add_external_row(c, row)  # Add to get zero
        if rnd:
            for r in range(result.row_count):
                for c in range(result.col_count):
                    result[r, c] = round(result[r, c], digits)
        return result

    def _combine(self, other):
        """
        Combines two matrices.

        :param other: other matrix
        :return: Matrix
        """
        if self.row_count != other.row_count:
            raise MatrixError("Different row count")
        result = Matrix.create(self.row_count, self.col_count + other.col_count)
        for r in range(result.row_count):
            for c in range(result.col_count):
                result[r, c] = self[r, c]
                result[r, c + other.col_count] = other[r, c]
        return result

    def invert(self, rnd=True, digits=8):
        """
        Inverts matrix.

        :param rnd: round result
        :param digits: digits to round to
        :return: Matrix
        """
        if not (self.square and self.regular):
            raise MatrixError("No regular square matrix")
        result = self.duplicate()
        combined = result._combine(Matrix.create(result.row_count, result.row_count, unit=True))
        combined = combined.gauss_jordan(rnd=rnd, digits=digits)
        for r in range(result.row_count):  # Cut off old matrix
            for c in range(result.col_count):
                result[r, c] = combined[r, c + result.col_count]
        return result

    def _rank(self):
        """
        Calculates rank

        :return: int
        """
        if self.is_row:
            return 1
        rank = self.row_count
        matrix = self.gauss()
        for r in range(matrix.row_count):
            for c in range(matrix.col_count):
                if matrix[r, c] != 0:  # Check if element is unequal to zero
                    break  # Continue with next line
                if c == matrix.col_count - 1:  # Count rank down if whole line is zero
                    rank -= 1
        return rank
