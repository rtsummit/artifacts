
import sys
import re
from .csvtype import CSVTypeId
from .csvtable import *
from .utils import *
from .reporter import Reporter

column_name_regex = re.compile('^[_a-z]+[_a-z0-9]*$')

class ColumnNameVerifier:
    def __init__(self):
        pass

    def prologue(self, table_name, header):
        for ci in header:
            name = ci.name()
            if '' == name or '#' == name[0]:
                continue

            if False == self.valid_name(name):
                Reporter.warning(f'컬럼 이름 \'{name}\' 이 규약에 맞지 않습니다.')
                #return False

        return False

    def epilogue(self):
        pass

    def visit(self, header, columns):
        return True

    def valid_name(self, name):
        return None != column_name_regex.match(name)
