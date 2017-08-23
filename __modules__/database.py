import simplejson
from os.path import isfile


class Database:
    def __init__(self, file_name, target=None):
        """Constructor"""
        self.file_name = file_name
        self.__fields = None  # List of object fields
        self.__target = target
        if not isfile(self.file_name):  # Create database if it does not exist
            self.data = []
            self.save(safe_mode=False)
        self.load()

    @staticmethod
    def __extract(args):
        """Extracts list from arguments"""
        return args[0] if len(args) == 1 and type(args[0]) == list else args

    def load(self):
        """Loads data"""
        self.data = simplejson.load(self.file_name, target=self.__target)

    def save(self, indent=4, safe_mode=True):
        """Saves data"""
        backup = []
        if safe_mode:
            if not self.data or self.data == []:
                raise Exception("Data is not assigned or empty")
            backup = simplejson.load(self.file_name)  # Create backup in case of exception

        try:
            simplejson.save(self.file_name, self.data, indent=indent)
        except Exception as e:  # Save backup
            simplejson.save(self.file_name, backup, indent=indent)
            raise Exception("Something went wrong: {0}".format(str(e)))

    def add(self, value):
        """Adds value"""
        self.data.append(value)

    def filter(self, *criteria):
        """Filters data which matches the criteria"""
        if self.data == []:
            raise Exception("Data is empty")

        result = []
        for i in range(0, len(self.data)):
            should_add = True
            for (key, value) in Database.__extract(criteria):
                if eval("self.data[{0}].{1}".format(i, key)) != value:
                    should_add = False
                    break
            if should_add:
                result.append(self.data[i])
        return result

    def delete(self, *criteria):
        """Deletes data which matches the criteria"""
        if self.data == []:
            raise Exception("Data is empty")

        indices = list()
        for i in range(0, len(self.data)):
            should_delete = True
            for (key, value) in Database.__extract(criteria):
                if eval("self.data[{0}].{1}".format(i, key)) != value:
                    should_delete = False
                    break
            if should_delete:
                indices.append(i)

        for index in sorted(indices, reverse=True):
            del self.data[index]

    def clear(self):
        """Clears database"""
        self.data = []
