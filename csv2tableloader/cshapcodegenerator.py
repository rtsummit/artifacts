
import os
import shutil
import filecmp

from templatemanager import TemplateManager

from csvloader.csvtable import CSVTable, CSVColumn
from csvloader.csvtype import *
from util import *

class CShapCodeGenerator:
    UNIT_TAB = '    '
    def __init__(self, output_path, table):
        self._output_path = output_path
        self._table = table
        self._message_name = self.to_message_name(self._table.name())
        self._class_name = self._message_name + 'Table'
        self._file_name = f'CSV{self._class_name}.cs'
        self._curr_indent = 0

    def curr_tabs(self):
        return self.UNIT_TAB * self._curr_indent

    def prologue(self):
        self._output = open(self._file_name, 'w')

    def epilogue(self):
        self._output.close()

        if 0 < len(self._output_path):
            if False == file_compare(self._file_name, self._output_path):
                file_move(self._file_name, self._output_path)
                print('copied !')

    def generate(self):
        has_key_column = self._table.has_key_column()
        key_column_name = self._table.key_column_name()

        csv_columns_to_data_class_definition_code = ''
        csv_columns_to_data_import_code = ''
        i = 0
        for column in self._table.header():
            if not column.is_comment():
                self._curr_indent = 2
                csv_columns_to_data_class_definition_code += f'{self.curr_tabs()}{self.convert_column_to_definition(column)};\n'
                self._curr_indent = 4
                csv_columns_to_data_import_code += self.convert_column_to_import_code(column, i)
            i += 1

        call_proto_key_field = f'ctx.{self.to_message_field_name(key_column_name)}' if has_key_column else ''

        csv_file_message_name = self.to_bytes_layout_name(self._table.file_name())
        csv_table_field_name = self.to_message_field_name(self._table.name()) + 'Data'

        self._output.write(TemplateManager.get_cshap_template(has_key_column).format(
            className=self._class_name, 
            messageName=self._message_name, 
            keyType=self.csvtype_to_cshaptype(self._table.key_column_type_id()), 
            fileName=self._table.file_name() if '.seg.csv' not in self._table.file_name() else self._table.name() + '.csv', 
            fileNameWithoutEXT=self._table.file_name().split('.')[0], 
            tableName=self._table.name(), 
            dataClassDefinitionCode=csv_columns_to_data_class_definition_code,
            csvColumnImportCode=csv_columns_to_data_import_code, 
            csvHeader=self._table.header_str(),
            dataToCsvColumnsFields='', 
            callProtoKeyField=call_proto_key_field, 
            csvFileMessageName=csv_file_message_name, 
            csvTableFieldName=csv_table_field_name
        ))

    def to_bytes_layout_name(self, file_name):
        return 'CSV' + self.to_message_name(file_name.split('.')[0]) + 'File'

    def to_message_name(self, name):
        tokens = name.split('_')

        name = ''
        for token in tokens:
            name += token[0].upper() + token[1:]

        return name

    def to_message_field_name(self, name):
        tokens = name.split('_')

        name = ''
        for token in tokens:
            if 0 == len(name):
                name = token[0].upper() + token[1:]
            else:
                name += token[0].upper() + token[1:]

        return name

    def csvtype_to_cshaptype(self, type_id, inner_type_id = CSVTypeId.NONE):
        if (type_id == CSVTypeId.VECTOR):
            return f'List<{self.csvtype_to_cshaptype(inner_type_id)}>'
            
        if type_id == CSVTypeId.BOOL:
            return 'bool'
        elif type_id == CSVTypeId.INT:
            return 'int'
        elif type_id == CSVTypeId.UINT:
            return 'uint'
        elif type_id == CSVTypeId.ULONG:
            return 'ulong'
        elif type_id == CSVTypeId.FLOAT:
            return 'float'
        elif type_id == CSVTypeId.STRING:
            return 'string'
        elif type_id == CSVTypeId.TIME:
            return 'uint'
        elif type_id == CSVTypeId.VECTOR3:
            return 'Common.TableVector3'

        return 'uint'

    def convert_column_to_definition(self, column):
        if column.type().is_vector():
            return 'public {0} {1} = new()'.format(
                self.csvtype_to_cshaptype(column.type().type_id(), column.type().inner_type_id()),
                self.to_message_field_name(column.name()))
        else:
            return 'public {0} {1}'.format(
                self.csvtype_to_cshaptype(column.type().type_id()),
                self.to_message_field_name(column.name()))
        
    def convert_column_to_import_code(self, column, i):
        if column.is_comment():
            return f'{self.curr_tabs()}// ignore column {column.name()}\n'

        if False == column.valid_name():
            return ''

        code = ''
        if column.type().is_vector():
            type_id = column.type().inner_type_id()
            type_name = self.csvtype_to_cshaptype(type_id)

            code = f'{self.curr_tabs()}if (row.Count >= {i + 1})\n'
            code += f'{self.curr_tabs()}{{\n'
            self._curr_indent += 1
            code += f'{self.curr_tabs()}string[] parts = string.Format("{{0}}", row[{i}]).Split(\'|\');\n'
            code += f'{self.curr_tabs()}for (int v = 0, vcount = parts.Length; v < vcount; v++)\n'
            code += f'{self.curr_tabs()}{{\n'
            self._curr_indent += 1
            code += f'{self.curr_tabs()}if (0 == parts[v].Length) continue;\n'

            if CSVTypeId.BOOL == type_id:
                code += f'{self.curr_tabs()}ctx.{self.to_message_field_name(column.name())}.Add(0 < uint.Parse(parts[v]) ? true : false);\n'
            elif CSVTypeId.INT == type_id or CSVTypeId.UINT == type_id or CSVTypeId.ULONG == type_id:
                code += f'{self.curr_tabs()}ctx.{self.to_message_field_name(column.name())}.Add({type_name}.Parse(parts[v]));\n'
            elif CSVTypeId.TIME == type_id:
                code += f'{self.curr_tabs()}ctx.{self.to_message_field_name(column.name())}.Add(({type_name})new System.DateTimeOffset(System.Convert.ToDateTime(parts[v]), new System.TimeSpan(0)).ToUnixTimeSeconds());\n'
            elif CSVTypeId.FLOAT == type_id:
                code += f'{self.curr_tabs()}ctx.{self.to_message_field_name(column.name())}.Add({type_name}.Parse(parts[v]));\n'
            elif CSVTypeId.STRING == type_id:
                code += f'{self.curr_tabs()}ctx.{self.to_message_field_name(column.name())}.Add(parts[v]);\n'
            elif CSVTypeId.VECTOR3 == type_id:
                code += f'{self.curr_tabs()}ctx.{self.to_message_field_name(column.name())}.Add(UnityUtil.Vector3FromCsvString(parts[v]));\n'
            else:
                code = f'{self.curr_tabs()}// NOT IMPLEMENTED\n'

            self._curr_indent -= 1
            code += f'{self.curr_tabs()}}}\n'
            self._curr_indent -= 1
            code += f'{self.curr_tabs()}}}\n'
        else:
            type_id = column.type().type_id()
            type_name = self.csvtype_to_cshaptype(type_id)

            if CSVTypeId.BOOL == type_id:
                code = f'{self.curr_tabs()}if (row.Count >= {i + 1}) {{ uint temp = 0; uint.TryParse(string.Format("{{0}}", row[{i}]), out temp); ctx.{self.to_message_field_name(column.name())} = ((0 < temp) ? true : false); }}\n'
            elif CSVTypeId.INT == type_id or CSVTypeId.UINT == type_id or CSVTypeId.ULONG == type_id:
                code = f'{self.curr_tabs()}if (row.Count >= {i + 1}) {{ {type_name} temp = 0; {type_name}.TryParse(string.Format("{{0}}", row[{i}]), out temp); ctx.{self.to_message_field_name(column.name())} = temp; }}\n'
            elif CSVTypeId.TIME == type_id:
                code = f'{self.curr_tabs()}if (row.Count >= {i + 1}) {{ {type_name} temp = 0; try {{temp = ({type_name})new System.DateTimeOffset(System.Convert.ToDateTime(row[{i}]), System.TimeSpan.FromHours(9)).ToUnixTimeSeconds(); }} catch (System.Exception) {{ temp = 0; }} ctx.{self.to_message_field_name(column.name())} = temp; }}\n'
            elif CSVTypeId.FLOAT == type_id:
                code = f'{self.curr_tabs()}if (row.Count >= {i + 1}) {{ {type_name} temp = 0.0f; {type_name}.TryParse(string.Format("{{0}}", row[{i}]), out temp); ctx.{self.to_message_field_name(column.name())} = temp; }}\n'
            elif CSVTypeId.STRING == type_id:
                code = f'{self.curr_tabs()}ctx.{self.to_message_field_name(column.name())} = (row.Count >= {i + 1}) ? string.Format("{{0}}", row[{i}]) : "";\n'
            elif CSVTypeId.VECTOR3 == type_id:
                code = f'{self.curr_tabs()}if (row.Count >= {i + 1}) {{ {type_name} temp; UnityUtil.Vector3FromCsvString(string.Format("{{0}}", row[{i}]), out temp); ctx.{self.to_message_field_name(column.name())} = temp; }}\n'
            else:
                code = f'{self.curr_tabs()}// NOT IMPLEMENTED\n'

        return code
