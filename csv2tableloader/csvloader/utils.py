
import sys
from .csvtype import CSVTypeId

def get_default_csv_value(type_id):
    if type_id == CSVTypeId.INT:
        return '0'
    elif type_id == CSVTypeId.UINT:
        return '0'
    elif type_id == CSVTypeId.ULONG:
        return '0'
    elif type_id == CSVTypeId.FLOAT:
        return '0.0'

    return ''

def typeid_to_typename(type_id):
    if CSVTypeId.BOOL == type_id:
        return 'bool'
    elif CSVTypeId.INT == type_id:
        return 'int'
    elif CSVTypeId.UINT == type_id:
        return 'uint'
    elif CSVTypeId.ULONG == type_id:
        return 'ulong'
    elif CSVTypeId.FLOAT == type_id:
        return 'float'
    elif CSVTypeId.STRING == type_id:
        return 'string'
    elif CSVTypeId.TIME == type_id:
        return 'time'
    elif CSVTypeId.VECTOR == type_id:
        return 'vector'

    return '<unknown>'

def min_value(type_id):
    if CSVTypeId.INT == type_id:
        return -2147483648
    return 0

def max_value(type_id):
    if CSVTypeId.INT == type_id:
        return 2147483647
    elif CSVTypeId.UINT == type_id:
        return 4294967295
    elif CSVTypeId.ULONG == type_id:
        #ULONG 이긴하나 최대치는 LONG 기준으로 체크한다.
        return 9223372036854775807
    return 0

def print_and_exit(level, message):
    print(level, '>', message)
    sys.exit(0)
