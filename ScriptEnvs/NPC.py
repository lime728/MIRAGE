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
        self.prompt_query = read_txt(Config.DataDir / script_name / 'self_prompts' / 'prompt_query.txt')
        self.prompt_belief = read_txt(Config.DataDir / script_name / 'self_prompts' / 'prompt_belief.txt')

    def converse_stage(self, logs):
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
                if logs is None:
                    while True:
                        try:
                            if name in self.culprit:
                                response = Api(Config.Culprit_Model).run_api(prompt_converse)
                            else:
                                response = Api(Config.Civilian_Model).run_api(prompt_converse)
                            history_converse = response.split('### RESPONSE:')[1].strip()
                            action = re.findall('【(.*?)】【', history_converse, re.DOTALL)[0]
                            item = re.findall('】【(.*?)】：', history_converse, re.DOTALL)[0]
                            if action == '询问' and item not in self.env_summary.keys():
                                raise ValueError('Unacceptable name!')
                            elif action not in ['询问']:
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
                        item = re.findall('】【(.*?)】：', history_converse, re.DOTALL)[0]
                        if action == '询问' and item not in self.env_summary.keys():
                            raise ValueError('Unacceptable name!')
                        elif action not in ['询问']:
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
                                item = re.findall('】【(.*?)】：', history_converse, re.DOTALL)[0]
                                if action == '询问' and item not in self.env_summary.keys():
                                    raise ValueError('Unacceptable name!')
                                elif action not in ['询问']:
                                    raise ValueError('Unaccepted action!')
                                else:
                                    break
                            except:
                                self.fail_num += 1
                self.save_log('Env', prompt_converse, template='prompt_converse')
                self.save_log(name, response, template='prompt_converse')

                ask_content = re.findall('】：(.*)', history_converse, re.DOTALL)[0]
                task_history = self.ask(item, name, background, self.history_introduction, self.history, ask_content, logs)
                self.role_parameter[name]['last_action'].append(response + '\n' + name + '：' + task_history)
                self.history += name + '：' + history_converse + '\n'
                self.history += name + '：' + task_history + '\n'
                self.history = self.token_check(self.history)

                # query & belief Eval
                logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                logs = self.del_logs_with_template(logs, template='prompt_query')
                for candidate_name in self.candidate_list:
                    self.self_query(self.history_introduction, self.history, candidate_name, self.candidates)
                    self.self_belief(self.history_introduction, self.history, candidate_name, self.candidates)
            self.turns += 1

    def self_query(self, history_introduction, history, other_name, candidates):
        # 怀疑度评估，怀疑度[0, 1, 2]
        history = self.token_check(history)
        prompt_query = self.prompt_query.format(
            history=history_introduction+history,
            other_name=other_name,
        )
        while True:
            try:
                response = Api(Config.Base_Model).run_api(prompt_query)
                query_response = response.split('### RESPONSE:')[1].strip()
                candidates[other_name]['query'] += int(query_response)
                break
            except:
                self.fail_num += 1
        self.save_log('Env', prompt_query, template='prompt_query')
        self.save_log('Agent', response, template='prompt_query')

    def self_belief(self, history_introduction, history, other_name, candidates):
        # 信任度评估，信任度[-2, -1, 0]
        history = self.token_check(history)
        prompt_belief = self.prompt_belief.format(
            history=history_introduction+history,
            other_name=other_name,
        )
        while True:
            try:
                response = Api(Config.Base_Model).run_api(prompt_belief)
                belief_response = response.split('### RESPONSE:')[1].strip()
                candidates[other_name]['query'] -= int(belief_response)
                break
            except:
                self.fail_num += 1
        self.save_log('Env', prompt_belief, template='prompt_belief')
        self.save_log('Agent', response, template='prompt_belief')

    def select(self, logs):
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
                if logs is None:
                    while True:
                        try:
                            if name in self.culprit:
                                response = Api(Config.Culprit_Model).run_api(prompt_select)
                            else:
                                response = Api(Config.Civilian_Model).run_api(prompt_select)
                            history_converse = response.split('### RESPONSE:')[1].strip()
                            action = re.findall('【(.*?)】【', history_converse, re.DOTALL)[0]
                            item = re.findall('】【(.*?)】：', history_converse, re.DOTALL)[0]
                            if action == '调查' and item not in self.clues.keys():
                                raise ValueError('Unacceptable place!')
                            elif action not in ['调查']:
                                raise ValueError('Unaccepted action!')
                            else:
                                break
                        except:
                            self.fail_num += 1
                else:
                    try:
                        logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                        prompt_select_ = logs.pop(0)['Message']
                        response = logs.pop(0)['Message']
                        history_converse = response.split('### RESPONSE:')[1].strip()
                        action = re.findall('【(.*?)】【', history_converse, re.DOTALL)[0]
                        item = re.findall('】【(.*?)】：', history_converse, re.DOTALL)[0]
                        if action == '调查' and item not in self.clues.keys():
                            raise ValueError('Unacceptable place!')
                        elif action not in ['调查']:
                            raise ValueError('Unaccepted action!')
                        else:
                            break
                    except:
                        while True:
                            try:
                                if name in self.culprit:
                                    response = Api(Config.Culprit_Model).run_api(prompt_select)
                                else:
                                    response = Api(Config.Civilian_Model).run_api(prompt_select)
                                history_converse = response.split('### RESPONSE:')[1].strip()
                                action = re.findall('【(.*?)】【', history_converse, re.DOTALL)[0]
                                item = re.findall('】【(.*?)】：', history_converse, re.DOTALL)[0]
                                if action == '调查' and item not in self.clues.keys():
                                    raise ValueError('Unacceptable place!')
                                elif action not in ['调查']:
                                    raise ValueError('Unaccepted action!')
                                else:
                                    break
                            except:
                                self.fail_num += 1
                if item not in self.clues.keys():
                    continue
                else:
                    break
            self.save_log('Env', prompt_select, template='prompt_converse')
            self.save_log(name, response, template='prompt_converse')

            logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
            logs = self.del_logs_with_template(logs, template='clue')
            if item in self.clues.keys():
                clue, task_history = self.get_clue(item)
            else:
                clue = '没有这条线索，你浪费了一次发言机会。'
                task_history = '【线索】【{item}】：{clue}'.format(
                    item=item,
                    clue=clue
                )
            if Config.Console:
                print(task_history + '\n')

            self.role_parameter[name]['last_action'].append(response + '\n' + name + '：' + task_history)
            self.history += name + '：' + history_converse + '\n'
            self.history += name + '：' + task_history + '\n'
            self.history = self.token_check(self.history)

            # query & belief Eval
            logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
            logs = self.del_logs_with_template(logs, template='prompt_query')
            for candidate_name in self.candidate_list:
                self.self_query(self.history_introduction, self.history, candidate_name, self.candidates)
                self.self_belief(self.history_introduction, self.history, candidate_name, self.candidates)

    def run(self, path):
        if path is None:
            logs = None
        else:
            logs = read_json(path)
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
            self.init_stage(logs)
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
            self.converse_stage(logs)
            self.select(logs)
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

        self.save_config()
        self.logger.close()
        print("******************************Finish******************************")