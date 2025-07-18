# 孝衣新娘
# Bride in filial dress
# TYPE: Single Orthodox Close

from ScriptEnvs.BaseEnv import *


class SOC(BaseEnv):
    def __init__(self, script_name, script_files):
        super().__init__(script_name, script_files)
        if self.configs['Language'] == 'Zh':
            self.culprit.append('方医生')
        elif self.configs['Language'] == 'En':
            self.culprit.append('Doctor Fang')

        # Load Scripts
        for path in script_files:
            if str(path).endswith('线索.json') or str(path).endswith('clues.json'):
                self.clues = read_json(path)
                if self.configs['Language'] == 'Zh':
                    self.clues_memory = self.clues.pop('陈均梦的回忆')
                elif self.configs['Language'] == 'En':
                    self.clues_memory = self.clues.pop('Memory of Junmeng Chen')

    def check_memory(self, history):
        memoery_keys = list(self.clues_memory.keys())
        for memory_item in memoery_keys:
            if memory_item in history:
                memory = self.clues_memory.pop(memory_item)
                if self.configs['Language'] == 'Zh':
                    self.role_parameter['陈均梦']['self_clues'] += memory_item + ': ' + memory + '\n'
                elif self.configs['Language'] == 'En':
                    self.role_parameter['Junmeng Chen']['self_clues'] += memory_item + ': ' + memory + '\n'
            else:
                pass

    def self_introduction_stage(self, logs):
        for name, background in self.env_summary.items():
            prompt_introduction = self.prompt_introduction_raw.format(
                name=name,
                description=background,
                self_clues=self.role_parameter[name]['self_clues']
            )
            if logs is None:
                while True:
                    try:
                        if name in self.culprit:
                            response = Api(Config.Culprit_Model).run_api(prompt_introduction)
                        else:
                            response = Api(Config.Civilian_Model).run_api(prompt_introduction)
                        introduction = response.split('### RESPONSE:')[1].strip()
                        break
                    except:
                        self.fail_num += 1
            else:
                logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                prompt_introduction_ = logs.pop(0)['Message']
                response = logs.pop(0)['Message']
                introduction = response.split('### RESPONSE:')[1].strip()
            if name in self.culprit and Config.force_expose:
                introduction = "I'm the Culprit. " + introduction
            self.save_log('Env', prompt_introduction, template='prompt_introduction')
            if name in self.culprit:
                self.save_log(name, response, template='prompt_introduction', model=Config.Culprit_Model)
            else:
                self.save_log(name, response, template='prompt_introduction', model=Config.Civilian_Model)

            self.role_parameter[name]['last_action'].append(response)

            # query & belief Eval
            logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
            logs = self.del_logs_with_template(logs, template='prompt_query')
            self.query(self.history_introduction, '', name, introduction, self.candidates)
            self.belief(self.history_introduction, '', name, introduction, self.candidates)

            if "self_introduction" not in self.role_parameter[name].keys():
                self.role_parameter[name]['self_introduction'] = introduction
            self.history_introduction += name + ':【Self-Introduction】: ' + introduction + '\n'

            self.check_memory(self.history_introduction)

        self.history_introduction = self.token_check(self.history_introduction) + '\n'

    def converse_stage(self, logs):
        while self.turns < Config.MaxTurnNum:
            # converse
            print('**********Turn {}**********'.format(self.turns + 1))
            for name, background in self.env_summary.items():
                ls_address = self.address[name]
                if name in self.address[name]:
                    ls_address.remove(name)
                characters = list()
                for c in list(self.scripts.keys()):
                    if c != name:
                        characters.append(c)
                prompt_converse = self.prompt_converse_raw.format(
                    name=name,
                    description=background,
                    self_clues=self.role_parameter[name]['self_clues'],
                    history=self.history_introduction+self.history,
                    last_action=self.role_parameter[name]['last_action'][-1],
                    characters=characters,
                    address=ls_address
                )
                if logs is None:
                    while True:
                        try:
                            if name in self.culprit:
                                response = Api(Config.Culprit_Model).run_api(prompt_converse)
                            else:
                                response = Api(Config.Civilian_Model).run_api(prompt_converse)
                            history_converse = response.split('### RESPONSE:')[1].strip()
                            action = re.findall('【(.*?)】【', history_converse, re.DOTALL)[0]
                            item = re.findall('】【(.*?)】:', history_converse, re.DOTALL)[0]
                            ask_content = re.findall('】:(.*)', history_converse, re.DOTALL)[0]
                            if (action == '询问' or action == 'Ask') and item not in self.env_summary.keys():
                                raise ValueError('Unacceptable name!')
                            elif (action == '调查' or action == 'Investigate') and item not in self.clues.keys():
                                raise ValueError('Unacceptable place!')
                            elif action not in ['调查', '询问', 'Ask', 'Investigate']:
                                raise ValueError('Unaccepted action!')
                            else:
                                break
                        except:
                            self.fail_num += 1
                else:
                    try:
                        logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                        prompt_converse_ = logs.pop(0)['Message']
                        response = logs.pop(0)['Message']
                        history_converse = response.split('### RESPONSE:')[1].strip()
                        action = re.findall('【(.*?)】【', history_converse, re.DOTALL)[0]
                        item = re.findall('】【(.*?)】:', history_converse, re.DOTALL)[0]
                        ask_content = re.findall('】:(.*)', history_converse, re.DOTALL)[0]
                        if (action == '询问' or action == 'Ask') and item not in self.env_summary.keys():
                            raise ValueError('Unacceptable name!')
                        elif (action == '调查' or action == 'Investigate') and item not in self.clues.keys():
                            raise ValueError('Unacceptable place!')
                        elif action not in ['调查', '询问', 'Ask', 'Investigate']:
                            raise ValueError('Unaccepted action!')
                    except:
                        while True:
                            try:
                                if name in self.culprit:
                                    response = Api(Config.Culprit_Model).run_api(prompt_converse)
                                else:
                                    response = Api(Config.Civilian_Model).run_api(prompt_converse)
                                history_converse = response.split('### RESPONSE:')[1].strip()
                                action = re.findall('【(.*?)】【', history_converse, re.DOTALL)[0]
                                item = re.findall('】【(.*?)】:', history_converse, re.DOTALL)[0]
                                ask_content = re.findall('】:(.*)', history_converse, re.DOTALL)[0]
                                if (action == '询问' or action == 'Ask') and item not in self.env_summary.keys():
                                    raise ValueError('Unacceptable name!')
                                elif (action == '调查' or action == 'Investigate') and item not in self.clues.keys():
                                    raise ValueError('Unacceptable place!')
                                elif action not in ['调查', '询问', 'Ask', 'Investigate']:
                                    raise ValueError('Unaccepted action!')
                                else:
                                    break
                            except:
                                self.fail_num += 1
                if name in self.culprit and Config.force_expose:
                    ask_content = "I'm the Culprit. " + ask_content
                self.save_log('Env', prompt_converse, template='prompt_converse')
                if name in self.culprit:
                    self.save_log(name, response, template='prompt_converse', model=Config.Culprit_Model)
                else:
                    self.save_log(name, response, template='prompt_converse', model=Config.Civilian_Model)

                # query & belief Eval
                logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                logs = self.del_logs_with_template(logs, template='prompt_query')
                self.query(self.history_introduction, self.history, name, history_converse, self.candidates)
                self.belief(self.history_introduction, self.history, name, history_converse, self.candidates)

                if action == '调查' or action == 'Investigate':
                    logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                    logs = self.del_logs_with_template(logs, template='clue')
                    if item in self.clues.keys():
                        clue, task_history = self.get_clue(item)
                    else:
                        clue = 'Without this clue, you have wasted an opportunity to speak.'
                        task_history = '【Clue】【{item}】: {clue}'.format(
                            item=item,
                            clue=clue
                        )
                    if Config.Console:
                        print(task_history + '\n')
                    self.clue_count += 1
                elif action == '询问' or action == 'Ask':
                    task_history = self.ask(item, name, background, self.history_introduction, self.history, ask_content, logs)

                    # query & belief Eval
                    logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                    logs = self.del_logs_with_template(logs, template='prompt_query')
                    self.query(self.history_introduction, self.history, item, task_history, self.candidates)
                    self.belief(self.history_introduction, self.history, item, task_history, self.candidates)
                else:
                    raise ValueError('Unaccepted action!')
                self.role_parameter[name]['last_action'].append(response + '\n' + name + '：' + task_history)
                self.history += name + ':【' + action + '】【' + item + '】: ' + ask_content + '\n'
                self.history += name + ': ' + task_history + '\n'
                self.check_memory(self.history)
                self.history = self.token_check(self.history)
            self.turns += 1
