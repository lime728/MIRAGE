# 狐狸旅馆
# Fox Hotel
# TYPE: Multi Unorthodox Open

from ScriptEnvs.BaseEnv import *


class MUO(BaseEnv):
    def __init__(self, script_name, script_files):
        super().__init__(script_name, script_files)
        if self.configs['Language'] == 'Zh':
            self.culprit.append('滑头鬼')
            self.culprit.append('桐生一郎（滑头鬼）')
        elif self.configs['Language'] == 'En':
            self.culprit.append('Nopperabo')
            self.culprit.append('Ichiro Kiryu (Nopperabo)')

        self.show = str()
        self.fox_clue = str()

        # Load Scripts
        for path in script_files:
            if str(path).endswith('人物剧本.json') or str(path).endswith('script.json'):
                self.scripts = read_json(path)
                self.show = self.scripts.pop('show')
            elif str(path).endswith('线索.json') or str(path).endswith('clues.json'):
                self.clues = read_json(path)
                if self.configs['Language'] == 'Zh':
                    self.fox_clue = self.clues.pop('小暖')
                elif self.configs['Language'] == 'En':
                    self.fox_clue = self.clues.pop('Xiao Nuan')

    def add_script(self, scripts):
        self.candidates = dict()
        self.env_summary = dict()
        old_scripts = self.scripts
        self.scripts = dict()
        for name, script in scripts.items():
            for old_name, old_script in old_scripts.items():
                if old_name in name:
                    self.scripts[name] = old_scripts[old_name]
            for k, v in script.items():
                if k == 'Story' or 'Script':
                    self.scripts[name][k] += v

    def run(self, path):
        if path is None:
            logs = None
        else:
            logs = read_json(path)
        print("******************************Start******************************")

        # part scripts
        part_scripts = self.scripts
        self.scripts = dict()
        part_clues = self.clues
        for script_num, part_script in part_scripts.items():
            print('***************{}***************'.format(script_num))
            if self.scripts == dict():
                self.scripts = part_script
                for name, content in self.scripts.items():
                    if name == '小狐狸' or name == 'Little Fox':
                        self.scripts[name]['Script'] = self.show + '\n' + content['Script'] + '\n' + self.fox_clue
                    else:
                        self.scripts[name]['Script'] = self.show + '\n' + content['Script']
            else:
                self.add_script(part_script)

            # Switch clues
            self.clues = part_clues[script_num]

            # Initial base environment
            print('********************Init Stage********************')
            self.init_stage(logs)
            print('Init Stage Over...')

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
