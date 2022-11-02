
import sys
from pathlib import Path

from .csvcache import CSVCache
from .csvloader import CSVLoader
from .reporter import Reporter
from .columnnameverifier import ColumnNameVerifier
from .columnkeyverifier import ColumnKeyVerifier
from .typevalueverifier import TypeValueVerifier
from .questtaskverifier import QuestTaskVerifier

def get_verifiers():
    return [ ColumnNameVerifier(), ColumnKeyVerifier(), TypeValueVerifier(), QuestTaskVerifier() ]

def verify(path_name):
    Reporter.init()

    file_names = []

    paths = Path(path_name).glob('**/*.csv')
    for path in paths:
        # because path is object not string
        file_names.append(str(path))

    for file_name in file_names:
        tables = CSVLoader.load('', file_name)
        if 0 == len(tables):
            continue

        for table in tables:
            verifiers = get_verifiers()

            table_name = table.name()
            Reporter.info(f'{file_name} - {table_name} 테이블 검사 중...')

            for verifier in verifiers:
                """
                if False == table.visit(verifier):
                    return False
                """
                table.visit(verifier)

            tokens = file_name.split('\\')

            CSVCache.set(tokens[-1], table_name, table)

    CSVCache.clear()

    Reporter.info('데이터 검증이 완료되었습니다.')

    Reporter.close()

    return True
