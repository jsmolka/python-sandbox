from cli import *

def goedel_to_word(number, sigma):
    """Converts Goedel number to word"""
    base = len(sigma) + 1
    s = str()
    while number > base:
        s += sigma[number % base - 1]
        number = number // base

    s += sigma[number % base - 1]

    s = "".join(reversed(s))  # Reverse string
    return s


def word_to_goedel(word, sigma):
    """Converts word to Goedel number"""
    goedel = 0
    base = len(sigma) + 1
    word = list(reversed(word))
    for i in range(0, len(word)):
        goedel += (sigma.index(word[i]) + 1) * base ** i

    return goedel


if __name__ == "__main__":
    sig = ["a", "b", "g", "i", "l", "s", "t", "u", "_"]
    w = "ba_ist_lustig"
    n = 2194679586743
    print("Sigma:", sig)
    print("Number:", n)
    print("goedel_to_word(number, sigma):", goedel_to_word(n, sig))
    print("word_to_goedel(word, sigma):", word_to_goedel(w, sig))

    enter("exit")
