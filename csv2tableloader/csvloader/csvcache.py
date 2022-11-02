
class CSVCacheEntry:
    def __init__(self):
        self._csv_tables = { }

    def set(self, table_name, table):
        self._csv_tables[table_name] = table

    def get(self, table_name):
        table = None
        try:
            table = self._csv_tables[table_name]
        except KeyError as e:
            print(e)

        return table

class CSVCache:
    _entries = { }

    @staticmethod
    def clear():
        CSVCache._entries.clear()

    @staticmethod
    def set(file_name, table_name, table):
        if file_name in CSVCache._entries:
            CSVCache._entries[file_name].set(table_name, table)
        else:
            entry = CSVCacheEntry()
            entry.set(table_name, table)
            CSVCache._entries[file_name] = entry

    @staticmethod
    def get(file_name, table_name):
        try:
            entry = CSVCache._entries[file_name]
            return entry.get(table_name)
        except KeyError as e:
            print(e)

        return None
