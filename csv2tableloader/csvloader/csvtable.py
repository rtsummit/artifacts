
import csv
from .csvtype import *
from .utils import *
from .reporter import Reporter

class CSVColumn:
    def __init__(self, name, type, is_key):
        self._name = name
        self._type = type
        self._is_key = is_key

    def name(self):
        return self._name

    def type(self):
        return self._type

    def is_key(self):
        return self._is_key

    def valid_name(self):
        if '' == self._name or False == self._name.isidentifier() or self.is_comment():
            return False

        return True

    def is_comment(self):
        if '' == self._name:
            return False

        return '#' == self._name[0]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._name + '|' + str(self._type) + '|' + str(self._is_key)

class CSVTable:
    def __init__(self, file_name, name):
        self._file_name = file_name.split('/')[-1]
        self._name = name
        self._header = []
        self._records = []

    def file_name(self):
        return self._file_name

    def name(self):
        return self._name

    def has_header(self):
        return 0 < len(self._header)

    def header(self):
        return self._header

    def records(self):
        return self._records

    def has_key_column(self):
        for column in self._header:
            if column.is_key():
                return True

        return False

    def key_column_type_id(self):
        for column in self._header:
            if column.is_key():
                return column.type().type_id()

        return CSVTypeId.UINT

    def key_column_name(self):
        for column in self._header:
            if column.is_key():
                return column.name()

        return ''

    def has_key(self, key):
        if 0 == len(self._header) or False == self._header[0].is_key():
            Reporter.error(f'{self._name}은 컬럼 키가 지정되어 있지 않습니다.')
            return False

        for record in self._records:
            if record[0] == str(key):
                return True

        return False

    def visit(self, visitor):
        if False == visitor.prologue(self._name, self._header):
            # prologue 메서드에서 False 반환 의미는 검사 실패가 아닌 레코드 검사를 안하겠다는 의미
            return True

        for record in self._records:
            if False == visitor.visit(self._header, record):
                return False

        visitor.epilogue()

        return True

    def is_comment_row(self, row):
        return row[0].startswith('//')

    def is_table_name_row(self, row):
        return row[0].startswith('##')

    def set_header(self, columns):
        for column in columns:
            tokens = column.split('|')

            if False == self.tokens_to_column_info(tokens):
                return False

        return True

    def tokens_to_column_info(self, tokens):
        # {name} | {type} | 'key'
        name = tokens[0]
        type = None
        is_key = False

        i = 0
        for token in tokens:
            if CSVTypeId.NONE != str_to_typeid(token):
                if i != 1:
                    Reporter.error(f'{self._name} 컬럼의 타입은 두 번째에 정의해야 합니다.')
                    return False

                type = str_to_type(token)
            elif token == 'key':
                if i < 1:
                    Reporter.error(f'{self._name} 컬럼의 유니크 설정은 첫 번째에 위치할 수 없습니다.')
                    return False
                is_key = True
            else:
                if i != 0:
                    Reporter.error(f'{self._name} {i} {token} 컬럼 이름은 반드시 첫 번째에 위치해야 합니다.')
                    return False
                name = token

            i = i + 1

        if None == type:
            type = str_to_type('uint')

        if is_key:
            pass

        self._header.append(CSVColumn(name, type, is_key))

        return True

    def append_record(self, record):
        if len(self._header) != len(record):
            Reporter.error(f'{self._name}의 헤더의 컬럼 개수와 일치하지 않습니다.')
            return False

        i = 0
        for column in record:
            if column == '':
                record[i] = get_default_csv_value(self._header[i].type().type_id())
            i = i + 1

        self._records.append(record)

        return True
    
    def header_str(self):
        s = ''
        for ci in self._header:
            if ci.is_key():
                s += '{0}|{1}|key,'.format(ci.name(),type_to_str(ci.type())) 
            elif '' == ci.name():
                s += ''
            else:
                s += '{0}|{1},'.format(ci.name(),type_to_str(ci.type())) 
        
        return s[:-1]
    
    def dump(self):
        for ci in self._header:
            print(ci)

        for record in self._records:
            print(record)
