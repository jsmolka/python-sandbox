import itertools
import numpy as np


def NOT(a):
    """Returns <not a>"""
    if a == 1:
        return 0
    else:
        return 1


def AND(a, b):
    """Returns <a and b>"""
    return a & b


def OR(a, b):
    """Returns <a or b>"""
    return a | b


def XOR(a, b):
    """Returns <a xor b>"""
    return a ^ b


def IMP(a, b):
    """Returns <a -> b>"""
    return NOT(a) | b


def EQU(a, b):
    """Returns <a <-> b>"""
    return (a & b) | (NOT(a) & NOT(b))


class Logic:
    def __init__(self, encrypted_string):
        """Constructor"""
        self.encrypted_string = encrypted_string
        self.decrypted_string = Logic.__decrypt(encrypted_string)

        # Create set of arguments
        self.arguments = list()
        for char in self.encrypted_string:
            if char.islower() and char not in self.arguments:
                self.arguments.append(char)
        self.arguments.sort()

        # Create values
        self.values = list()
        for i in itertools.product([0, 1], repeat=len(self.arguments)):  # Count in binary
            i = list(i)  # Tuple to list
            i.append(0)  # Add result position
            self.values.append(i)
        self.values = np.array(self.values)

        self.__solve()

    @staticmethod
    def __replace_not(replace_string):
        """Replaces !"""
        index = replace_string.index("!")
        a = replace_string[index + 1: len(replace_string) - 1]
        return "NOT({0})".format(a)

    @staticmethod
    def __replace_and(replace_string):
        """Replaces &"""
        index = replace_string.index("&")
        a = replace_string[1: index]
        b = replace_string[index + 1: len(replace_string) - 1]
        return "AND({0},{1})".format(a, b)

    @staticmethod
    def __replace_or(replace_string):
        """Replaces |"""
        index = replace_string.index("|")
        a = replace_string[1: index]
        b = replace_string[index + 1: len(replace_string) - 1]
        return "OR({0},{1})".format(a, b)

    @staticmethod
    def __replace_xor(replace_string):
        """Replaces ^"""
        index = replace_string.index("^")
        a = replace_string[1: index]
        b = replace_string[index + 1: len(replace_string) - 1]
        return "XOR({0},{1})".format(a, b)

    @staticmethod
    def __replace_imp(replace_string):
        """Replaces ->"""
        index = replace_string.index("->")
        a = replace_string[1: index]
        b = replace_string[index + 2: len(replace_string) - 1]
        return "IMP({0},{1})".format(a, b)

    @staticmethod
    def __replace_equ(replace_string):
        """Replaces <->"""
        index = replace_string.index("<->")
        a = replace_string[1: index]
        b = replace_string[index + 3: len(replace_string) - 1]
        return "EQU({0},{1})".format(a, b)

    @staticmethod
    def __decrypt(function_string):
        """Decrypts logic string"""
        exclamation_fix = True
        decrypt = True

        skip_open = 0
        skip_close = 0

        # Prepare function string for exclamation formatting
        function_string = function_string.replace(" ", "")  # Remove spaces
        function_string = "  {0}  ".format(function_string)  # Add borders to prevent index out of bounds

        # Format exclamation marks
        while exclamation_fix:
            for i in range(0, len(function_string)):
                if function_string[i] == "!" and function_string[i + 1].islower() and \
                        (function_string[i - 1] != "(" or function_string[i + 2] != ")"):  # Format !x to (!x)
                    exclamation_string = function_string[i] + function_string[i + 1]
                    function_string = function_string.replace(exclamation_string, "({0})".format(exclamation_string))

                if function_string[i] == "!" and function_string[i + 1] == "(" and \
                        function_string[i - 1] != "(":  # Format !() to (!())
                    j = i + 1
                    bracket_count = 0
                    while j < len(function_string):  # Find bracket length after !
                        if function_string[j] == "(":
                            bracket_count += 1
                        if function_string[j] == ")":
                            bracket_count -= 1
                        if bracket_count == 0:
                            exclamation_string = function_string[i:j]
                            function_string = function_string.replace(exclamation_string, "({0})".format(
                                                                      exclamation_string))  # Replace full bracket
                            break
                        j += 1

                # End while loop at last index
                if i == len(function_string) - 1:
                    exclamation_fix = False

        # Prepare function string for replacing
        function_string = function_string.replace(" ", "")  # Remove spaces
        function_string = "({0})".format(function_string)  # Add brackets for main function
        function_string = " {0} ".format(function_string)  # Add borders to prevent index out of bounds

        # Decrypt string
        while decrypt:
            index1 = 0
            for i in range(0, len(function_string)):
                if function_string[i] in ["T", "D", "R", "P", "U"]:  # Skip already formatted parts
                    skip_open += 1
                    skip_close += 1

                if function_string[i] == "(":
                    if skip_open > 0:
                        skip_open -= 1
                    else:
                        index1 = i

                if function_string[i] == ")":
                    if skip_close > 0:
                        skip_close -= 1
                    else:
                        index2 = i + 1
                        replace_string = function_string[index1: index2]

                        # Replace replace string
                        if "!" in replace_string:
                            function_string = function_string.replace(replace_string,
                                                                      Logic.__replace_not(replace_string))
                            break

                        if "&" in replace_string:
                            function_string = function_string.replace(replace_string,
                                                                      Logic.__replace_and(replace_string))
                            break

                        if "|" in replace_string:
                            function_string = function_string.replace(replace_string,
                                                                      Logic.__replace_or(replace_string))
                            break

                        if "^" in replace_string:
                            function_string = function_string.replace(replace_string,
                                                                      Logic.__replace_xor(replace_string))
                            break

                        if "<->" in replace_string:
                            function_string = function_string.replace(replace_string,
                                                                      Logic.__replace_equ(replace_string))
                            break

                        if "->" in replace_string:
                            function_string = function_string.replace(replace_string,
                                                                      Logic.__replace_imp(replace_string))
                            break

                # End while loop
                if i == len(function_string) - 1:
                    decrypt = False

        # Format function string
        function_string = function_string.replace(" ", "")  # Remove spaces
        while function_string[0] == "(":  # Remove unnecessary brackets
            function_string = function_string[1: len(function_string) - 1]

        return function_string

    def __solve(self):
        """Solves logic function"""
        for i in range(0, len(self.values)):
            function_string = self.decrypted_string
            for j in range(0, len(self.values[0]) - 1):  # Replace argument with appropriate value
                function_string = function_string.replace(self.arguments[j], str(self.values[i, j]))

            try:
                self.values[i, len(self.values[0]) - 1] = eval(function_string)
            except Exception as e:
                print(str(e))

    def draw_table(self):
        """Draws table"""
        for i in range(0, len(self.values)):
            print_string = ""
            for j in range(0, len(self.values[0]) - 1):
                print_string += "{0} = {1} | ".format(self.arguments[j], self.values[i, j])  # Add each variable
            print_string += "result = {0}".format(self.values[i, len(self.values[0]) - 1])  # Add result

            print(print_string)
