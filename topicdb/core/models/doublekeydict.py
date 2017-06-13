"""
DoubleKeyDict(ionary) class. Part of the StoryTechnologies Builder project.

July 02, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class DoubleKeyDict:

    def __init__(self):
        self.__dict = {}

    @property
    def dict(self):
        return self.__dict

    def __getitem__(self, keys):
        key1, key2 = keys  # Unpack values.
        nested_dict = self.__dict[key1]
        return nested_dict[key2]

    def __setitem__(self, keys, value):
        key1, key2 = keys  # Unpack values.
        if key1 in self.__dict:
            nested_dict = self.__dict[key1]
            nested_dict[key2] = value
            self.__dict[key1] = nested_dict
        else:
            nested_dict = {key2: value}
            self.__dict[key1] = nested_dict

    def __contains__(self, keys):
        key1, key2 = keys  # Unpack values.
        result = False
        if key1 in self.__dict:
            nested_dict = self.__dict[key1]
            if key2 in nested_dict:
                result = True
        return result

    def __len__(self):
        return len(self.__dict)
