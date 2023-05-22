import json
import os


class BaseInterpreter(object):

    def __init__(self):
        pass

    def _load_request_template(self, file_name: str, invoke_file=None, abs_path: str = None,
                               replace_map: dict = None) -> list:
        if not file_name:
            raise Exception('Invalid params: file_name is empty')

        if invoke_file:
            file_path = self._get_current_path(invoke_file, file_name)
        else:
            if not abs_path:
                file_path = file_name
            elif abs_path[-1] == '/':
                file_path = f"{abs_path}{file_name}"
            else:
                file_path = f"{abs_path}/{file_name}"

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if replace_map:
                for key in replace_map.keys():
                    content = content.replace(key, replace_map[key])
            data = json.loads(content)

        return data

    @staticmethod
    def _get_current_path(invoke_file, file_name) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(invoke_file)), file_name)
