
import os
import sys
import argparse

from csvloader.reporter import Reporter
from csvloader.csvloader import CSVLoader

from protocodegenerator import ProtoCodeGenerator, DummyProtoCodeGenerator
from cppcodegenerator import CPPCodeGenerator, CPPCodeGenerator_ItemType, CPPCodeGenerator_UnlockType
from cshapcodegenerator import CShapCodeGenerator

from templatemanager import TemplateManager

def parse_command_arguments(argv):
    argv_parser = argparse.ArgumentParser()
    argv_parser.add_argument('-input_path', required=False, default='./')
    argv_parser.add_argument('-input', nargs=argparse.REMAINDER)
    argv_parser.add_argument('-cshap_output_path', required=False, default='')

    return argv_parser.parse_args()

def get_csv_files(path):
    csv_files = []

    files = os.listdir(path)
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(file)

    return csv_files

def generate_code(code_generator):
    code_generator.prologue()
    code_generator.generate()
    code_generator.epilogue()

def generate_cshap_codes(options, table):
    generate_code(CShapCodeGenerator(options.cshap_output_path, table))

def main(argv):
    TemplateManager.set_home_path(os.path.abspath(os.path.dirname(argv[0])))

    Reporter.init()

    options = parse_command_arguments(argv)

    file_names = options.input if options.input is not None and 0 < len(options.input) else get_csv_files(options.input_path)
    for file_name in file_names:
        print(file_name, 'parsing ...')

        tables = CSVLoader.load('', options.input_path + '/' + file_name)
        for table in tables:
            generate_cshap_codes(options, table)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
