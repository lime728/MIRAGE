# 孝衣新娘
# Bride in filial dress
# TYPE: Normal Full Close

from ScriptEnvs.BaseEnv import *


class NFC(BaseEnv):
    def __init__(self, script_name, script_files):
        super().__init__(script_name, script_files)

        # Load Scripts
        for path in script_files:
            if str(path).endswith('线索.json'):
                self.clues = read_json(path)
                self.clues_memory = self.clues.pop('陈均梦的回忆')

    def check_memory(self, history):
        memoery_keys = list(self.clues_memory.keys())
        for memory_item in memoery_keys:
            if memory_item in history:
                memory = self.clues_memory.pop(memory_item)
                self.role_parameter['陈均梦']['self_clues'] += memory_item + '：' + memory + '\n'
            else:
                pass

    def self_introduction_stage(self):
        for name, background in self.env_summary.items():
            prompt_introduction = self.prompt_introduction_raw.format(
                name=name,
                description=background,
                self_clues=self.role_parameter[name]['self_clues']
            )
            while True:
                try:
                    response = Api(Config.Model).run_api(prompt_introduction)
                    introduction = response.split('### RESPONSE:')[1].strip()
                    break
                except:
                    self.fail_num += 1
            self.save_log('Env', prompt_introduction, template='prompt_introduction')
            self.save_log(name, response, template='prompt_introduction')

            self.role_parameter[name]['last_action'].append(response)

            # query
            self.query(self.history_introduction, '', name, introduction, self.candidates)

            if "self_introduction" not in self.role_parameter[name].keys():
                self.role_parameter[name]['self_introduction'] = introduction
            self.history_introduction += name + '：【自我介绍】：' + introduction + '\n'

            self.check_memory(self.history_introduction)

        self.history_introduction = self.token_check(self.history_introduction) + '\n'

    def converse_stage(self):
        while self.turns < Config.MaxTurnNum:
            # converse
            print('**********Turn {}**********'.format(self.turns + 1))
            for name, background in self.env_summary.items():
                ls_address = self.address[name]
                if name in self.address[name]:
                    ls_address.remove(name)
                prompt_converse = self.prompt_converse_raw.format(
                    name=name,
                    description=background,
                    self_clues=self.role_parameter[name]['self_clues'],
                    history=self.history_introduction+self.history,
                    last_action=self.role_parameter[name]['last_action'][-1],
                    characters=list(self.scripts.keys()),
                    address=ls_address
                )
                while True:
                    try:
                        response = Api(Config.Model).run_api(prompt_converse)
                        history_converse = response.split('### RESPONSE:')[1].strip()
                        action = re.findall('【(.*?)】【', history_converse, re.DOTALL)[0]
                        item = re.findall('】【(.*?)】：', history_converse, re.DOTALL)[0]
                        if action == '询问' and item not in self.env_summary.keys():
                            continue
                        elif action == '调查' and item not in self.clues.keys():
                            continue
                        elif action not in ['调查', '询问']:
                            raise ValueError('Unaccepted action!')
                        else:
                            break
                    except:
                        self.fail_num += 1
                self.save_log('Env', prompt_converse, template='prompt_converse')
                self.save_log(name, response, template='prompt_converse')

                self.query(self.history_introduction, self.history, name, history_converse, self.candidates)

                if action == '调查':
                    clue, task_history = self.get_clue(item)
                    if Config.Console:
                        print(task_history + '\n')
                elif action == '询问':
                    ask_content = re.findall('】：(.*)', history_converse, re.DOTALL)[0]
                    task_history = self.ask(item, name, background, self.history_introduction, self.history, ask_content)
                    self.query(self.history_introduction, self.history, item, task_history, self.candidates)
                else:
                    raise ValueError('Unaccepted action!')
                self.role_parameter[name]['last_action'].append(response + '\n' + name + '：' + task_history)
                self.history += name + '：' + history_converse + '\n'
                self.history += name + '：' + task_history + '\n'
                self.check_memory(self.history)
                self.history = self.token_check(self.history)
            self.turns += 1
