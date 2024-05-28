# 狐狸旅馆
# Fox Hotel
# TYPE: Abnormal Part Open

from ScriptEnvs.BaseEnv import *


class APO(BaseEnv):
    def __init__(self, script_name, script_files):
        super().__init__(script_name, script_files)

        self.show = str()
        self.fox_clue = str()

        # Load Scripts
        for path in script_files:
            if str(path).endswith('人物剧本.json'):
                self.scripts = read_json(path)
                self.show = self.scripts.pop('show')
            elif str(path).endswith('线索.json'):
                self.clues = read_json(path)
                self.fox_clue = self.clues.pop('小暖')

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
                if k == '人物故事' or '人物剧本':
                    self.scripts[name][k] += v

    def run(self):
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
                    if name == '小狐狸':
                        self.scripts[name]['人物剧本'] = self.show + '\n' + content['人物剧本'] + '\n' + self.fox_clue
                    else:
                        self.scripts[name]['人物剧本'] = self.show + '\n' + content['人物剧本']
            else:
                self.add_script(part_script)

            # Switch clues
            self.clues = part_clues[script_num]

            # Initial base environment
            print('********************Init Stage********************')
            self.init_stage()
            print('Init Stage Over...')

            # self-introduction
            print('********************Self-introduction Stage********************')
            self.self_introduction_stage()
            print('Self-introduction Stage Over...')

            # start converse
            print('********************Converse Stage********************')
            self.converse_stage()
            print('Converse Stage Over...')

        # Vote Stage
        print('********************Vote Stage********************')
        self.vote_stage()
        print('Vote Stage Over...')

        # End stage
        print('********************End Stage********************')
        self.end_stage()
        print('End Stage Over...')

        self.logger.close()
        print("******************************Finish******************************")
