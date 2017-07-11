import json
import os.path


class Database:
    def __init__(self, file_name):
        """Constructor"""
        self.file_name = file_name
        if not os.path.isfile(self.file_name):  # Create database if it does not exist
            self.data = []
            self.save()
        self.load()

    def __check_data(self):
        """Checks if data is assigned"""
        if self.data is None:
            raise Exception("Data is not assigned")

    @staticmethod
    def __extract_list(arguments):
        """Extracts list from arguments"""
        if len(arguments) == 1 and type(arguments[0]) == list:
            return arguments[0]
        else:
            return arguments

    def load(self):
        """Loads data"""
        if not os.path.isfile(self.file_name):
            raise Exception("{0} does not exist".format(self.file_name))

        with open(self.file_name) as data_file:
            self.data = json.load(data_file)

    def save(self, fancy=True):
        """Saves data"""
        self.__check_data()

        with open(self.file_name, "w") as outfile:
            if fancy:
                json.dump(self.data, outfile, indent=4)
            else:
                json.dump(self.data, outfile)

    def add(self, *data):
        """Adds data"""
        self.__check_data()

        data = Database.__extract_list(data)

        add_data = list()
        for value in data:
            add_data.append(value)
        self.data.append(add_data)

    def print_data(self):
        """Prints data"""
        self.__check_data()

        for data in self.data:
            print(data)

    def filter(self, *criteria):
        """Filters data"""
        self.__check_data()

        criteria = Database.__extract_list(criteria)

        filter_list = []
        for data in self.data:
            should_add = True
            for value in criteria:
                if value not in data:
                    should_add = False
            if should_add:
                filter_list.append(data)
        return filter_list

    def delete_criteria(self, *criteria):
        """Deletes data which matches the criteria"""
        self.__check_data()

        criteria = Database.__extract_list(criteria)

        index_list = list()
        for index, data in enumerate(self.data):
            should_delete = True
            for value in criteria:
                if value not in data:
                    should_delete = False
            if should_delete:
                index_list.append(index)

        index_list = sorted(index_list, reverse=True)
        while index_list:
            index = index_list.pop()
            del self.data[index]

    def delete_indices(self, *indices):
        """Deletes indices"""
        self.__check_data()

        indices = Database.__extract_list(indices)

        indices = sorted(indices, reverse=True)
        for index in indices:
            del self.data[index]

    def clear(self):
        """Clears database"""
        self.data = []

    def get_by_criteria(self, *criteria):
        """Gets first item which matches the criteria"""
        self.__check_data()

        criteria = self.__extract_list(criteria)

        for data in self.data:
            should_return = True
            for value in criteria:
                if value not in data:
                    should_return = False
            if should_return:
                return data

        print("No matching data")
        print("Returned first element")
        return self.data[0]

    def get_by_index(self, index):
        """Gets item which matches the index"""
        self.__check_data()

        if 0 <= index < len(self.data):
            return self.data[index]
        else:
            print("Index out of range")
