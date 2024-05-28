# 大明星最后的演出
# The final performance of a big star
# TYPE: Normal Part Close

from ScriptEnvs.BaseEnv import *


class NPC(BaseEnv):
    def __init__(self, script_name, script_files):
        super().__init__(script_name, script_files)
        self.candidate_list = [
            '黄迪', '李察德', '周雄', '王纱', '吕智', '强尼', '齐思'
        ]

        self.prompt_converse_raw = read_txt(Config.DataDir / script_name / 'self_prompts' / 'prompt_converse.txt')
        self.prompt_select_raw = read_txt(Config.DataDir / script_name / 'self_prompts' / 'prompt_select.txt')

    def converse_stage(self):
        while self.turns < Config.MaxTurnNum:
            # converse
            print('**********Turn {}**********'.format(self.turns + 1))
            for name, background in self.env_summary.items():
                prompt_converse = self.prompt_converse_raw.format(
                    name=name,
                    description=background,
                    self_clues=self.role_parameter[name]['self_clues'],
                    history=self.history_introduction+self.history,
                    last_action=self.role_parameter[name]['last_action'][-1],
                    characters=list(self.scripts.keys()),
                )
                while True:
                    try:
                        response = Api(Config.Model).run_api(prompt_converse)
                        history_converse = response.split('### RESPONSE:')[1].strip()
                        item = re.findall('】【(.*?)】：', history_converse, re.DOTALL)[0]
                        break
                    except:
                        self.fail_num += 1
                self.save_log('Env', prompt_converse, template='prompt_converse')
                self.save_log(name, response, template='prompt_converse')

                ask_content = re.findall('】：(.*)', history_converse, re.DOTALL)[0]
                task_history = self.ask(item, name, background, self.history_introduction, self.history, ask_content)
                self.role_parameter[name]['last_action'].append(response + '\n' + name + '：' + task_history)
                self.history += name + '：' + history_converse + '\n'
                self.history += name + '：' + task_history + '\n'
                self.history = self.token_check(self.history)
            self.turns += 1

    def select(self):
        for name, background in self.env_summary.items():
            while True:
                prompt_select = self.prompt_select_raw.format(
                    name=name,
                    description=background,
                    self_clues=self.role_parameter[name]['self_clues'],
                    history=self.history_introduction+self.history,
                    last_action=self.role_parameter[name]['last_action'][-1],
                    address=list(self.clues.keys())
                )
                while True:
                    try:
                        response = Api(Config.Model).run_api(prompt_select)
                        history_converse = response.split('### RESPONSE:')[1].strip()
                        item = re.findall('】【(.*?)】：', history_converse, re.DOTALL)[0]
                        break
                    except:
                        self.fail_num += 1
                if item not in self.clues.keys():
                    continue
                else:
                    break
            self.save_log('Env', prompt_select, template='prompt_converse')
            self.save_log(name, response, template='prompt_converse')

            clue, task_history = self.get_clue(item)
            if Config.Console:
                print(task_history + '\n')

            self.role_parameter[name]['last_action'].append(response + '\n' + name + '：' + task_history)
            self.history += name + '：' + history_converse + '\n'
            self.history += name + '：' + task_history + '\n'
            self.history = self.token_check(self.history)

    def run(self):
        print("******************************Start******************************")

        # NPC self-settings
        public_clue_1 = self.clues.pop('公开线索1')[0]
        public_clue_2 = self.clues.pop('公开线索2')[0]
        public_clue_3 = self.clues.pop('公开线索3')[0]

        # part scripts
        part_scripts = self.scripts
        self.scripts = dict()
        for script_num, part_script in part_scripts.items():
            print('***************{}***************'.format(script_num))
            if self.scripts == dict():
                self.scripts = part_script
            else:
                self.add_script(part_script)

            # self-setting
            if script_num == '第一幕':
                for name, content in self.scripts.items():
                    self.scripts[name]['人物剧本'] += ('\n公开线索1：\n' + public_clue_1)
                    self.scripts[name]['人物剧本'] += ('\n公开线索2：\n' + public_clue_2)
            elif script_num == '第四幕':
                for name, content in self.scripts.items():
                    self.scripts[name]['人物剧本'] += ('\n公开线索3：\n' + public_clue_3)
            else:
                pass

            # Initial base environment
            print('********************Init Stage********************')
            self.init_stage()
            print('Init Stage Over...')

            # change candidates
            self.candidates = dict()
            for name in self.candidate_list:
                self.candidates[name] = {
                    'query': 0
                }

            # add introduction
            for name, summary in self.env_summary.items():
                self.role_parameter[name]['last_action'].append(summary)

            # start converse
            print('********************Converse Stage********************')
            self.converse_stage()
            self.select()
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