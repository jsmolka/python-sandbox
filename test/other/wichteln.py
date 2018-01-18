from random import shuffle, seed


def ready(l1, l2):
    for i in range(0, len(l1)):
        if l1[i] == l2[i]:
            return False
    return True


seed(765)

people = {
    1: "Julian",
    2: "Bastian",
    3: "Frederik",
    4: "Max Burgert",
    5: "Max Schlotz",
    6: "Marc Reisenhofer",
    7: "Marc Kleber",
    8: "Jakob",
    9: "Fabian",
    10: "Simon"
}

l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
l2 = l1[:]

while not ready(l1, l2):
    shuffle(l1)
    shuffle(l2)

for i in range(0, len(l1)):
    with open("{0}.txt".format(people[l1[i]]), "w") as f:
        s = people[l2[i]]
        f.write(s)
