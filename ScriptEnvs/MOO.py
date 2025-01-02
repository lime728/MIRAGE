# 怒海余生
# Raging Sea of Rest Life
# TYPE: Multi Orthodox Open

from ScriptEnvs.BaseEnv import BaseEnv
from data_loader import *


class MOO(BaseEnv):
    def __init__(self, script_name, script_files):
        super().__init__(script_name, script_files)
        if self.configs['Language'] == 'Zh':
            self.culprit.append('约翰')
        elif self.configs['Language'] == 'En':
            self.culprit.append('John')

    def run(self, path):
        if path is None:
            logs = None
        else:
            logs = read_json(path)
        print("******************************Start******************************")

        # part scripts
        part_scripts = self.scripts
        self.scripts = dict()
        for script_num, part_script in part_scripts.items():
            print('***************{}***************'.format(script_num))
            if self.scripts == dict():
                self.scripts = part_script
                first_turn = True
            else:
                self.add_script(part_script)
                first_turn = False

            # Initial base environment
            print('********************Init Stage********************')
            self.init_stage(logs)
            print('Init Stage Over...')

            if first_turn:
                # self-introduction
                print('********************Self-introduction Stage********************')
                self.self_introduction_stage(logs)
                print('Self-introduction Stage Over...')

            # start converse
            print('********************Converse Stage********************')
            self.converse_stage(logs)
            print('Converse Stage Over...')

        # Vote Stage
        print('********************Vote Stage********************')
        self.vote_stage()
        print('Vote Stage Over...')

        # End stage
        print('********************End Stage********************')
        self.end_stage()
        print('End Stage Over...')

        # Eval Stage
        print('********************Eval Stage********************')
        self.rouge_eval()
        self.llms_eval()
        print('Evaluation Stage Over...')

        self.save_result()
        self.save_config()
        self.logger.close()
        print("******************************Finish******************************")
