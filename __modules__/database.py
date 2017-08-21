import simplejson
from os.path import isfile


class Database:
    def __init__(self, file_name):
        """Constructor"""
        self.file_name = file_name
        self.__fields = None  # List of object fields
        if not isfile(self.file_name):  # Create database if it does not exist
            self.data = []
            self.save(safe_mode=False)
        self.load()

    @staticmethod
    def __extract(args):
        """Extracts list from arguments"""
        return args[0] if len(args) == 1 and type(args[0]) == list else args

    def __assign_fields(self):
        """Assigns object fields of data"""
        if self.__fields is not None:
            return

        with open(self.file_name) as data_file:
            data = data_file.read()
        tuples = simplejson.json_to_namedtuple(data)
        self.__fields = [f for f in tuples[0]._fields] if type(tuples) == list else [f for f in tuples._fields]

    def load(self):
        """Loads data"""
        self.data = simplejson.load(self.file_name)

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

    def add(self, *data):
        """Adds data"""
        for value in Database.__extract_args(data):
            self.data.append(value)

    def filter(self, *criteria):
        """Filters data which matches the criteria"""
        self.__assign_fields()

        result = []
        for datum in self.data:
            should_add = True
            values = []
            for field in self.__fields:
                values.append(getattr(datum, field))
            for criterium in Database.__extract(criteria):
                if criterium not in values:
                    should_add = False
            if should_add:
                result.append(datum)
        return result

    def delete(self, *criteria):
        """Deletes data which matches the criteria"""
        self.__assign_fields()

        indices = list()
        for index, datum in enumerate(self.data):
            should_delete = True
            values = []
            for field in self.__fields:
                values.append(getattr(datum, field))
            for criterium in Database.__extract(criteria):
                if criterium not in values:
                    should_delete = False
            if should_delete:
                indices.append(index)

        for index in sorted(indices, reverse=True):
            del self.data[index]

    def clear(self):
        """Clears database"""
        self.data = []
