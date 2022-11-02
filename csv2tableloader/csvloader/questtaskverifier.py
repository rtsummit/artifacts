
import sys
from .csvcache import CSVCache 
from .csvtable import *
from .utils import *
from .reporter import Reporter

class QuestTaskVerifier:
    def __init__(self):
        self._prev_quest_id = 0
        self._prev_task_level = 0
        self._prev_single_zone = 0

    def prologue(self, table_name, header):
        if 'quest_task' != table_name:
            return False

        # 태스크의 퀘스트 식별 번호가 퀘스트 테이블에 존재하는지 검사하기 위해 필요
        self._quest_table = CSVCache.get('quest.csv', 'quest')

        self.set_column_indices_into_cache(header)
        return True

    def epilogue(self):
        pass

    def visit(self, header, columns):
        quest_id = int(columns[self._questid_column_index])
        task_level = int(columns[self._tasklevel_column_index])
        single_zone = int(columns[self._singlezone_column_index])

        if self._prev_quest_id != quest_id:
            if 0 < self._prev_quest_id and 0 < self._prev_single_zone:
                Reporter.error(f'퀘스트 태스크 마지막은 싱글존 설정하면 안됩니다. quest_id:{self._prev_quest_id}, task_level:{self._prev_task_level}, switch_single_zone:{self._prev_single_zone}')
                return False

            if False == self._quest_table.has_key(quest_id):
                Reporter.error(f'quest.csv에 quest_id:{quest_id} 가 존재하지 않습니다.')
                return False

            self._prev_quest_id = quest_id
            self._prev_task_level = task_level
            self._prev_single_zone = single_zone

            if self._prev_task_level != 1:
                Reporter.error(f'퀘스트 태스크 레벨은 반드시 1부터 시작해야합니다. quest_id:{self._prev_quest_id}, task_level:{self._prev_task_level}')
                return False

            return True

        if self._prev_task_level + 1 != task_level:
            Reporter.error(f'퀘스트 태스크 레벨 흐름이 올바르지 않습니다. quest_id:{quest_id}, task_level:{task_level}')
            return False

        self._prev_task_level = self._prev_task_level + 1

        if 0 < self._prev_single_zone:
            """
            if 0 < single_zone and single_zone != self._prev_single_zone:
                Reporter.error(f'퀘스트 태스크 싱글존이 바로 이전 태스크와 다릅니다. quest_id:{quest_id}, task_level:{task_level}, 현재 싱글존:{single_zone}, 이전 싱글존:{self._prev_single_zone}')
                return False
            """
            if 0 == single_zone:
                Reporter.error(f'퀘스트 태스크 싱글존이 바로 이전 태스크와 다릅니다. quest_id:{quest_id}, task_level:{task_level}, 현재 싱글존:{single_zone}, 이전 싱글존:{self._prev_single_zone}')
                return False

        self._prev_single_zone = single_zone

        return True

    def set_column_indices_into_cache(self, header):
        i = 0
        for ci in header:
            if ci.name() == 'quest_id':
                self._questid_column_index = i
            elif ci.name() == 'task_level':
                self._tasklevel_column_index = i
            elif ci.name() == 'switch_single_zone':
                self._singlezone_column_index = i

            i = i + 1
