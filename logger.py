from data_loader import *
from utils import Config
import time


class Logger:
    def __init__(self, script_name):
        self.log_dir = Config.LogPath / script_name
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.log_dir / 'history.json'
        self.log_path_current = self.log_dir / 'history_current.json'
        self.log_fw = open(self.log_path_current, 'a', encoding='utf-8')
        self.messages = list()

    def nprint(self, script_name, user, text, debug=False, console=True):
        message = {
            'Script_name': script_name,
            'Name': user,
            'Message': text,
            'Debug': debug,
            'Console': console,
            'TimeTemp': time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        }
        if debug:
            print(message)
        self.messages.append(message)
        self.log_fw.write(json.dumps(message, ensure_ascii=False, indent=1)+'\n')

    def gprint(self, script_name, user, text, template, model, debug=False, console=True):
        message = {
                'Script_name': script_name,
                'Name': user,
                'Message': text,
                'MessageLength': len(text),
                'TokenLength': token_calculate(text),
                'Template': template,
                'ApiModel': model,
                'Debug': debug,
                'Console': console,
                'ForceSummary': Config.force_summary,
                'TimeTemp': time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        }
        if debug:
            print(message)
        self.messages.append(message)
        self.log_fw.write(json.dumps(message, ensure_ascii=False, indent=1)+'\n')

    def close(self):
        self.log_fw.close()
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(self.messages, ensure_ascii=False, indent=1))
