
import os

class TemplateManager:
    _home_path = './'

    @staticmethod
    def set_home_path(path_name:str):
        TemplateManager._home_path = path_name

    @staticmethod
    def get_template(file_name:str):
        template = ''
        with open(TemplateManager._home_path + '/template/' + file_name, 'r') as f:
            template = f.read()

        return template

    @staticmethod
    def get_cshap_template(has_key:bool):
        return TemplateManager.get_template('csharp')
