
import sys
import re
from .csvtype import *
from .csvtable import *
from .utils import *
from .reporter import *

time_format_regex = re.compile(r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}')
vector_format_regex = re.compile(r'\([0-9]+,[0-9]+,[0-9]+\)')

class TypeValueVerifier:
    def __init__(self):
        pass

    def prologue(self, table_name, header):
        return True

    def epilogue(self):
        pass

    def visit(self, header, columns):
        i = 0
        for column in columns:
            ci = header[i]
            if ci.is_comment():
                continue

            if False == self.is_valid(ci.name(), ci.type().type_id(), ci.type().inner_type_id(), column):
                return False

            i = i + 1

        return True

    def is_valid(self, column_name, type_id, inner_type_id, value):
        try:
            if CSVTypeId.BOOL == type_id:
                convertValue = int(value)
                if 0 != convertValue and 1 != convertValue:
                    Reporter.error(f'{column_name} 값 {value}는 올바른 bool 값이 아닙니다.')
                    return False
            elif CSVTypeId.INT == type_id or CSVTypeId.UINT == type_id or CSVTypeId.ULONG == type_id:
                convertValue = int(value)
                min = min_value(type_id)
                max = max_value(type_id)
                if convertValue < min or max < convertValue:
                    Reporter.error(f'{column_name} 값 {value}는 {min} ~ {max} 범위에 존재해야 합니다.')
                    return False
            elif CSVTypeId.FLOAT == type_id:
                convertValue = float(value)
            elif CSVTypeId.STRING == type_id:
                pass
            elif CSVTypeId.TIME == type_id:
                if '' == value:
                    return True

                if None == time_format_regex.match(value):
                    Reporter.error(f'{column_name} 값 {value}는 올바른 날짜 형식이 아닙니다.')
                    return False
            elif CSVTypeId.VECTOR3 == type_id:
                if '' == value:
                    return True

                if None == vector_format_regex.match(value):
                    Reporter.error(f'{column_name} 값 {value}는 올바른 Vector3 형식이 아닙니다.')
                    return False
            elif CSVTypeId.VECTOR == type_id:
                if 0 == len(value):
                    return True

                vl = value.split('|')
                for v in vl:
                    if False == self.is_valid(column_name, inner_type_id, CSVTypeId.NONE, v):
                        Reporter.error(f'{column_name} 값 {value}는 정의된 자료형과 다릅니다.')
                        return False
            else:
                return False
        except:
            typename = typeid_to_typename(type_id)
            Reporter.fatal(f'\'{column_name}\' 컬럼의 \'{value}\'를 {typename}로 변환 실패하였습니다.')
            return False

        return True
