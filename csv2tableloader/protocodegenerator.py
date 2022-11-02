
import os
import shutil
import filecmp

from csvloader.csvtable import CSVTable, CSVColumn
from csvloader.csvtype import CSVTypeId, CSVType
from util import *

class DummyProtoCodeGenerator:
    def __init__(self):
        pass

    def prologue(self):
        pass

    def epilogue(self):
        pass

    def generate(self, table):
        pass

    def generate_bytes_layout(self, file_name, tables):
        pass

class ProtoCodeGenerator:
    def __init__(self, output_path):
        self._output_path = output_path
        self._table_names = {}
        self._bytes_file_names = {}

    def prologue(self):
        self._output = open('common_table.proto', 'w')

        self._output.write('// Generated by the Ares CSV2TableLoader.\n// !!! DO NOT EDIT !!!\n\n')
        self._output.write('syntax="proto2";\n')
        self._output.write('package Ares.Common;\n\n')
        self._output.write('option go_package = ".generated";\n')
        self._output.write('option java_package = "kr.co.seconddive.ares.message";\n\n')
        self._output.write('message TableVector3 {\n')
        self._output.write('\toptional float x = 1;\n')
        self._output.write('\toptional float y = 2;\n')
        self._output.write('\toptional float z = 3;\n')
        self._output.write('}\n\n')

    def epilogue(self):
        self._output.close()

        if 0 < len(self._output_path):
            if False == file_compare('common_table.proto', self._output_path):
                file_move('common_table.proto', self._output_path)
                print('copied !')

    def generate(self, table):
        file_name = table.file_name()
        table_name = self.to_message_name(table.name())

        if table_name in self._table_names:
            self._output.write(f'// {file_name} -> {table_name} skipped !!! \n\n\n')
            return

        self._table_names[table_name] = file_name

        self._output.write(f'// {file_name}\n')
        self._output.write(f'message Table_{table_name}Data {{\n')
        self._output.write('\tmessage Record {\n')

        field_index = 1

        header = table.header()
        for column in header:
            if False == column.valid_name():
                continue

            field_type = self.to_proto_type(column.type())
            field_name = self.to_field_name(column.name())

            self._output.write(f'\t\t{field_type} {field_name} = {field_index};\n')

            field_index += 1

        self._output.write('\t}\n')
        self._output.write('\trepeated Record records = 1;\n')
        self._output.write('}\n\n')

    def generate_bytes_layout(self, file_name, tables):
        file_name_without_ext = self.to_bytes_layout_name(file_name)

        if file_name_without_ext in self._bytes_file_names:
            return

        self._bytes_file_names[file_name_without_ext] = file_name

        self._output.write(f'message {file_name_without_ext} {{\n')
        i = 1
        for table in tables:
            self._output.write(f'\toptional Table_{self.to_message_name(table.name())}Data {self.to_field_name(table.name())}Data = {i};\n')
            i += 1
        self._output.write('}\n\n')

    def to_bytes_layout_name(self, file_name):
        return 'CSV' + self.to_message_name(file_name.split('.')[0]) + 'File'

    def to_message_name(self, name):
        tokens = name.split('_')

        name = ''
        for token in tokens:
            name += token[0].upper() + token[1:]

        return name

    def to_field_name(self, name):
        tokens = name.split('_')

        name = ''
        for token in tokens:
            if 0 < len(name):
                token = token[0].upper() + token[1:]
            else:
                token = token[0].lower() + token[1:]

            name += token

        return name

    def to_proto_type(self, type):
        type_name = ''
        if type.is_vector():
            type_name = 'repeated ' + self.csvtype_to_prototype(type.inner_type_id())
        else:
            type_name = 'optional ' + self.csvtype_to_prototype(type.type_id())

        return type_name

    def csvtype_to_prototype(self, type_id):
        if type_id == CSVTypeId.BOOL:
            return 'bool'
        elif type_id == CSVTypeId.INT:
            return 'sint32'
        elif type_id == CSVTypeId.UINT:
            return 'uint32'
        elif type_id == CSVTypeId.ULONG:
            return 'uint64'
        elif type_id == CSVTypeId.FLOAT:
            return 'float'
        elif type_id == CSVTypeId.STRING:
            return 'string'
        elif type_id == CSVTypeId.TIME:
            return 'uint32'
        elif type_id == CSVTypeId.VECTOR3:
            return 'TableVector3'

        return 'uint32'
