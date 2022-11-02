
import sys
from .csvtable import *
from .utils import *
from .reporter import Reporter

class ColumnKeyVerifier:
    def __init__(self):
        self.keys = {}

    def prologue(self, table_name, header):
        if 0 == len(header):
            return False

        # 키는 첫번째 컬럼에만 설정 가능하다.
        return header[0].is_key()

    def epilogue(self):
        pass

    def visit(self, header, columns):
        key = int(columns[0])
        if key in self.keys:
            Reporter.error(f'중복된 키({key})가 존재합니다.')

        self.keys[key] = True

        return True
