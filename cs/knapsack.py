import dialog
import itertools


class Item:
    def __init__(self, number, weight, use):
        """Constructor"""
        self.number = number
        self.weight = weight
        self.use = use
        self.relative_use = round(self.use / self.weight, 5)

    @staticmethod
    def from_list(item):
        """Creates Item from list"""
        # Takes list with property order [number, weight, use]
        return Item(item[0], item[1], item[2])


class PackedBackpack:
    def __init__(self, items, order, use, weight):
        """Constructor"""
        self.items = items
        self.order = order
        self.use = use
        self.weight = weight


class Backpack:
    def __init__(self, items, max_weight):
        """Constructor"""
        self.items = list()  # Initialize items
        self.__parse(items)  # Fill items
        self.max_weight = max_weight

    def __parse(self, items):
        """Parses a list and creates sorted items"""
        for item in items:
            self.items.append(Item.from_list(item))
        self.items = sorted(self.items, key=lambda x: x.relative_use, reverse=True)  # Sort by relative use (descending)

    def calculate_use(self, order):
        """Calculates use"""
        # order is a list of zeros and ones
        if len(order) != len(self.items):
            raise Exception("Order and item length is different")

        use = 0
        weight = 0
        full = False
        for i in range(0, len(self.items)):
            if order[i] == 1:
                difference = self.max_weight - weight
                if self.items[i].weight < difference:  # Add things if there is space
                    use += self.items[i].use
                    weight += self.items[i].weight
                else:  # Add fractions if there is not enough space (only for last item)
                    if not full:
                        use += round((difference * self.items[i].use) / self.items[i].weight, 5)
                        weight += round((difference * self.items[i].weight) / self.items[i].weight, 5)
                        full = True
                    else:  # Backpack is full
                        use = 0
                        break

        return use

    def calculate_best_order(self, order_list):
        """Calculates best order"""
        best_order = list()
        best_use = 0
        for order in order_list:
            use = self.calculate_use(order)
            if use > best_use:
                best_use = use
                best_order = order

        return best_order

    def pack(self, order_list):
        """Creates a return backpack"""
        best_order = self.calculate_best_order(order_list)
        packed_backpack = PackedBackpack(
            self.items,
            best_order,
            self.calculate_use(best_order),
            self.max_weight
        )

        return packed_backpack


def knapsack_naive(items, max_weight):
    """Naively solves the knapsack problem"""
    # Items [[number, weight, use], [...]]
    backpack = Backpack(items, max_weight)
    order_list = list()
    for binary in itertools.product([0, 1], repeat=len(backpack.items)):  # Count in binary
        order_list.append(list(binary))

    return backpack.pack(order_list)


if __name__ == "__main__":
    # l = [[1, 2, 7], [2, 3, 3], [3, 6, 5], [4, 9, 6]]  # Number, weight, use
    # pbp = knapsack_naive(l, 14)
    # for v in pbp.items:
    #     print("Item:", v.number, "|", "Weight:", v.weight, "|", "Use:", v.use, "|", "Relative use:", v.relative_use)
    # print("Order:", pbp.order)
    # print("Use:", pbp.use)
    # print("Weight:", pbp.weight)

    l = [[1, 4, 5], [2, 8, 10], [3, 3, 3], [4, 5, 2], [5, 2, 3]]
    pbp = knapsack_naive(l, 10)
    for v in pbp.items:
        print("Item:", v.number, "|", "Weight:", v.weight, "|", "Use:", v.use, "|", "Relative use:", v.relative_use)
    print("Order:", pbp.order)
    print("Use:", pbp.use)
    print("Weight:", pbp.weight)

    # l = [[1, 8, 2], [2, 6, 2], [3, 10, 4], [4, 12, 6]]
    # pbp = knapsack_naive(l, 11)
    # for v in pbp.items:
    #     print("Item:", v.number, "|", "Weight:", v.weight, "|", "Use:", v.use, "|", "Relative use:", v.relative_use)
    # print("Order:", pbp.order)
    # print("Use:", pbp.use)
    # print("Weight:", pbp.weight)

    dialog.enter("exit")
