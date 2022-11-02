
import sys
import re

from enum import Enum

vector_type_regex = re.compile(r'vector<(?P<inner_type>(bool|int|uint|ulong|float|string|time|Vector3))>')

class CSVTypeId(Enum):
    NONE = 0
    BOOL = 1
    INT = 2
    UINT = 3
    ULONG = 4
    FLOAT = 5
    STRING = 6
    TIME = 7
    VECTOR = 8
    VECTOR3 = 9

class CSVType:
    def __init__(self, type, inner_type = CSVTypeId.NONE):
        self._type = type
        self._inner_type = inner_type

    def type_id(self):
        return self._type

    def inner_type_id(self):
        return self._inner_type

    def is_vector(self):
        return CSVTypeId.VECTOR == self._type

    def __str__(self):
        if self.is_vector():
            return 'vector<' + str(self._inner_type) + '>'
        else:
            return str(self._type)

        return 'uint'


def str_to_typeid(str):
    if str == 'bool':
        return CSVTypeId.BOOL
    elif str == 'int':
        return CSVTypeId.INT
    elif str == 'uint':
        return CSVTypeId.UINT
    elif str == 'ulong':
        return CSVTypeId.ULONG
    elif str == 'float':
        return CSVTypeId.FLOAT
    elif str == 'string':
        return CSVTypeId.STRING
    elif str == 'time':
        return CSVTypeId.TIME
    elif str == 'Vector3':
        return CSVTypeId.VECTOR3
    elif None != vector_type_regex.match(str):
        return CSVTypeId.VECTOR

    return CSVTypeId.NONE

def str_to_type(str):
    if str == 'bool':
        return CSVType(CSVTypeId.BOOL)
    elif str == 'int':
        return CSVType(CSVTypeId.INT)
    elif str == 'uint':
        return CSVType(CSVTypeId.UINT)
    elif str == 'ulong':
        return CSVType(CSVTypeId.ULONG)
    elif str == 'float':
        return CSVType(CSVTypeId.FLOAT)
    elif str == 'string':
        return CSVType(CSVTypeId.STRING)
    elif str == 'time':
        return CSVType(CSVTypeId.TIME)
    elif str == 'Vector3':
        return CSVType(CSVTypeId.VECTOR3)
    elif m := vector_type_regex.match(str):
        return CSVType(CSVTypeId.VECTOR, str_to_typeid(m.group('inner_type')))

    return None

typeid_to_str_dic = {
    CSVTypeId.BOOL: 'bool',
    CSVTypeId.INT: 'int',
    CSVTypeId.UINT: 'uint',
    CSVTypeId.ULONG: 'ulong',
    CSVTypeId.FLOAT: 'float',
    CSVTypeId.STRING: 'string',
    CSVTypeId.TIME: 'time',
    CSVTypeId.VECTOR: 'vector',
    CSVTypeId.VECTOR3: 'Vector3',
}

def type_to_str(type):
    if type.type_id() == CSVTypeId.VECTOR:
        return f'vector<{typeid_to_str_dic[type.inner_type_id()]}>'
    return typeid_to_str_dic[type.type_id()]
