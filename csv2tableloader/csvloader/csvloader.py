
import csv
from .csvtype import CSVTypeId, CSVType
from .csvtable import CSVColumn, CSVTable
from .reporter import Reporter
from .utils import *

class CSVLoader:
    @staticmethod
    def load(path, file_name):
        tables = CSVLoader.load_by_encoding(path, file_name, 'utf-8-sig')
        if tables is None:
            tables = CSVLoader.load_by_encoding(path, file_name, 'euc-kr')
            if tables is None:
                tables = []

        return tables

    @staticmethod
    def load_by_encoding(path, file_name, codeset):
        tables = []

        try:
            with open(CSVLoader.full_path_name(path, file_name), encoding=codeset, newline='') as csv_file:
                csv_reader = csv.reader(csv_file)

                table = None

                for row in csv_reader:
                    if '' == row or CSVLoader.is_comment_row(row):
                        continue

                    if CSVLoader.is_table_name_row(row):
                        if None != table:
                            tables.append(table)

                        table_name = row[0][2:]
                        table = CSVTable(file_name, table_name)
                    else:
                        if False == table.has_header():
                            if False == table.set_header(row):
                                return tables
                        else:
                            if False == table.append_record(row):
                                return tables

                if table not in tables:
                    tables.append(table)
        except Exception as e:
            Reporter.fatal(e)
            return None

        return tables

    @staticmethod
    def full_path_name(path, file_name):
        path_name = ''
        if path == '':
            path_name = file_name
        else:
            path_name = path + '/' + file_name

        return path_name

    @staticmethod
    def is_comment_row(row):
        return row[0].startswith('//')

    @staticmethod
    def is_table_name_row(row):
        return row[0].startswith('##')
