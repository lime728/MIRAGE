# 基类
# BaseEnv
# TYPE: Base class

from data_loader import *
from utils import Api
from utils import Config
from logger import Logger
from pathlib import Path


class BaseEnv:
    def __init__(self, script_name, script_files):
        # global configs
        self.configs = dict()
        for k, v in Config.__dict__.items():
            if '__' in k:
                continue
            if isinstance(v, Path):
                self.configs[k] = str(v)
            elif type(v) == list and len(v) > 0:
                if isinstance(v[0], Path):
                    str_v = list()
                    for ls in v:
                        str_v.append(str(ls))
                    self.configs[k] = str_v
            elif type(v) == dict:
                str_v = dict()
                for d_k, d_v in v.items():
                    d_str_v = list()
                    for ls in d_v:
                        d_str_v.append(str(ls))
                    str_v[d_k] = d_str_v
                self.configs[k] = str_v
            else:
                self.configs[k] = v

        # Base config
        self.words_num = Config.MaxBaseScriptSummaryToken
        self.logger = Logger(script_name)
        self.debug = Config.DEBUG
        self.console = Config.Console
        self.turns = 0
        self.script_name = script_name
        self.fail_num = 0
        self.truth = read_json(Config.ScriptTruth)[script_name]

        # Base Env
        self.env_summary = dict()
        self.role_parameter = dict()
        self.candidates = dict()
        self.history_introduction = str()
        self.history = str()
        self.address = dict()
        self.culprit = list()

        # Load Scripts
        for path in script_files:
            if str(path).endswith('人物剧本.json') or str(path).endswith('script.json'):
                self.scripts = read_json(path)
            elif str(path).endswith('线索.json') or str(path).endswith('clues.json'):
                self.clues = read_json(path)

        # Load prompts
        self.prompt_script_summarize_raw = read_txt(Config.PromptDir / 'prompt_script_summarize.txt')
        self.prompt_history_summarize_raw = read_txt(Config.PromptDir / 'prompt_history_summarize.txt')
        self.prompt_summary_raw = read_txt(Config.PromptDir / 'prompt_base_summary.txt')
        self.prompt_converse_raw = read_txt(Config.PromptDir / 'prompt_converse.txt')
        self.prompt_ask_raw = read_txt(Config.PromptDir / 'prompt_ask.txt')
        self.prompt_introduction_raw = read_txt(Config.PromptDir / "prompt_introduction.txt")
        self.prompt_query = read_txt(Config.PromptDir / 'prompt_query.txt')
        self.prompt_belief = read_txt(Config.PromptDir / 'prompt_belief.txt')
        self.prompt_vote = read_txt(Config.PromptDir / 'prompt_vote.txt')
        self.prompt_eval = read_txt(Config.PromptDir / 'prompt_eval.txt')
        self.prompt_eval_rouge = read_txt(Config.PromptDir / 'prompt_eval_rouge.txt')

    def add_script(self, scripts):
        for name, script in scripts.items():
            for k, v in script.items():
                if k == 'Story' or 'Script':
                    self.scripts[name][k] += v

    def token_check(self, text):
        raw_length = token_calculate(text)
        if raw_length > Config.MaxBaseScriptSummaryToken:
            return self.summarize(text)
        else:
            return text

    def del_logs_with_template(self, logs, template):
        if logs is not None:
            if logs[0]['Template'] == template:
                while logs[0]['Template'] == template:
                    del logs[0]
        return logs

    def summarize(self, text):
        if Config.force_summary and token_calculate(text) <= Config.MaxBaseScriptSummaryToken:
            return text
        else:
            prompt_summarize = self.prompt_history_summarize_raw.format(
                text=text
            )
            while True:
                try:
                    response = Api(Config.Base_Model).run_api(prompt_summarize)
                    result = response.split('### RESPONSE:')[1].strip()
                    break
                except:
                    self.fail_num += 1
            self.save_log('Env', prompt_summarize, template='prompt_history_summarize')
            self.save_log('Env', response, template='prompt_history_summarize')
            return result

    def get_clue(self, item):
        clue = self.clues[item].pop()
        clue_history = '【Clue】【{item}】: {clue}'.format(
            item=item,
            clue=clue
        )
        self.save_log('【Clue】【{item}】'.format(item=item), clue, template='clue')
        if len(self.clues[item]) == 0:
            self.clues.pop(item)
        return clue, clue_history

    def ask(self, item, name, background,history_introduction, history, ask_content, logs):
        prompt_ask = self.prompt_ask_raw.format(
            name=item,
            description=background,
            self_clues=self.role_parameter[name]['self_clues'],
            history=history_introduction+history,
            ask_name=name,
            ask_content=ask_content
        )
        if logs is None:
            while True:
                try:
                    if item in self.culprit:
                        response = Api(Config.Culprit_Model).run_api(prompt_ask)
                    else:
                        response = Api(Config.Civilian_Model).run_api(prompt_ask)
                    ask_response = response.split('### RESPONSE:')[1].strip()
                    break
                except:
                    self.fail_num += 1
        else:
            logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
            prompt_ask_ = logs.pop(0)['Message']
            response = logs.pop(0)['Message']
            ask_response = response.split('### RESPONSE:')[1].strip()
        if Config.force_expose and item in self.culprit:
            ask_response = "I'm the Culprit. " + ask_response
        self.save_log('Env', prompt_ask, template='prompt_ask')
        if item in self.culprit:
            self.save_log(item, response, template='prompt_ask', model=Config.Culprit_Model)
        else:
            self.save_log(item, response, template='prompt_ask', model=Config.Civilian_Model)
        return ask_response

    def query(self, history_introduction, history, other_name, content, candidates):
        # 怀疑度评估，怀疑度[0, 1, 2]
        history = self.token_check(history)
        prompt_query = self.prompt_query.format(
            history=history_introduction+history,
            other_name=other_name,
            content=content
        )
        while True:
            try:
                if other_name in self.culprit:
                    response = Api(Config.Culprit_Model).run_api(prompt_query)
                else:
                    response = Api(Config.Civilian_Model).run_api(prompt_query)
                query_response = response.split('### RESPONSE:')[1].strip()
                candidates[other_name]['query'] += int(query_response)
                break
            except:
                self.fail_num += 1
        candidates[other_name]['query_all'] += 2
        candidates[other_name]['query_value'] += int(query_response)
        self.save_log('Env', prompt_query, template='prompt_query')
        if other_name in self.culprit:
            self.save_log('Agent', response, template='prompt_query', model=Config.Culprit_Model)
        else:
            self.save_log('Agent', response, template='prompt_query', model=Config.Civilian_Model)

    def belief(self, history_introduction, history, other_name, content, candidates):
        # 信任度评估，信任度[-2, -1, 0]
        history = self.token_check(history)
        prompt_belief = self.prompt_belief.format(
            history=history_introduction+history,
            other_name=other_name,
            content=content
        )
        while True:
            try:
                if other_name in self.culprit:
                    response = Api(Config.Culprit_Model).run_api(prompt_belief)
                else:
                    response = Api(Config.Civilian_Model).run_api(prompt_belief)
                belief_response = response.split('### RESPONSE:')[1].strip()
                candidates[other_name]['query'] -= int(belief_response)
                break
            except:
                self.fail_num += 1
        candidates[other_name]['belief_all'] += 2
        candidates[other_name]['belief_value'] += int(belief_response)
        self.save_log('Env', prompt_belief, template='prompt_belief')
        if other_name in self.culprit:
            self.save_log('Agent', response, template='prompt_belief', model=Config.Culprit_Model)
        else:
            self.save_log('Agent', response, template='prompt_belief', model=Config.Civilian_Model)

    def script_summarize(self, name, content, logs):
        summarized_content = dict()
        for k, v in content.items():
            if 500 < token_calculate(v) < 4000:
                prompt_script_summarize = self.prompt_script_summarize_raw.format(
                    name=name,
                    item=k,
                    content=v
                )
                if logs is None:
                    while True:
                        try:
                            response = Api(Config.Base_Model).run_api(prompt_script_summarize)
                            summarized_content[k] = response.split('### RESPONSE:')[1].strip()
                            break
                        except:
                            self.fail_num += 1
                else:
                    logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                    prompt_script_summarize_ = logs.pop(0)['Message']
                    response = logs.pop(0)['Message']
                    summarized_content[k] = response.split('### RESPONSE:')[1].strip()
                self.save_log('Env', prompt_script_summarize, template='prompt_script_summarize')
                self.save_log('Env', response, template='prompt_script_summarize')
            elif token_calculate(v) > 4000:
                print('Summarizing Super-Long Script 《{}》——{}——{}...'.format(self.script_name, name, k))
                s_content = v
                splited_summarized_content = list()
                while token_calculate(s_content) > 0:
                    prompt_script_summarize = self.prompt_script_summarize_raw.format(
                        name=name,
                        item=k,
                        content=s_content[:4000]
                    )
                    if logs is None:
                        while True:
                            try:
                                response = Api(Config.Base_Model).run_api(prompt_script_summarize)
                                splited_summarized_content.append(response.split('### RESPONSE:')[1].strip())
                                break
                            except:
                                self.fail_num += 1
                    else:
                        logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                        prompt_script_summarize_ = logs.pop(0)['Message']
                        response = logs.pop(0)['Message']
                        splited_summarized_content.append(response.split('### RESPONSE:')[1].strip())
                    self.save_log('Env', prompt_script_summarize, template='prompt_script_summarize')
                    self.save_log('Env', response, template='prompt_script_summarize')
                    s_content = s_content[4000:]
                sp_content = str()
                for part in splited_summarized_content:
                    sp_content += part
                prompt_script_summarize = self.prompt_script_summarize_raw.format(
                    name=name,
                    item=k,
                    content=sp_content
                )
                if logs is None:
                    while True:
                        try:
                            response = Api(Config.Base_Model).run_api(prompt_script_summarize)
                            summarized_content[k] = response.split('### RESPONSE:')[1].strip()
                            break
                        except:
                            self.fail_num += 1
                else:
                    logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                    prompt_script_summarize_ = logs.pop(0)['Message']
                    response = logs.pop(0)['Message']
                    summarized_content[k] = response.split('### RESPONSE:')[1].strip()
                self.save_log('Env', prompt_script_summarize, template='prompt_script_summarize')
                self.save_log('Env', response, template='prompt_script_summarize')
            else:
                summarized_content[k] = v
        return summarized_content

    def init_stage(self, logs):
        self.turns = 0
        for name, content in self.scripts.items():
            prompt_summary = self.prompt_summary_raw.format(
                name=name,
                background=content['Story'],
                script=content['Script'],
                relation=content['Relationship'],
                expression=content['Performance'],
                mission=content['Purpose'],
                others=content['Ability']
            )
            if token_calculate(prompt_summary) > Config.MaxBaseScriptSummaryToken * 2:
                summarized_content = self.script_summarize(name, content, logs)
                prompt_summary = self.prompt_summary_raw.format(
                    name=name,
                    background=summarized_content['Story'],
                    script=summarized_content['Script'],
                    relation=summarized_content['Relationship'],
                    expression=summarized_content['Performance'],
                    mission=summarized_content['Purpose'],
                    others=summarized_content['Ability']
                )
            if logs is None:
                while True:
                    try:
                        response = Api(Config.Base_Model).run_api(prompt_summary)
                        summary_text = response.split('### RESPONSE:')[1].strip()
                        break
                    except:
                        self.fail_num += 1
            else:
                logs = self.del_logs_with_template(logs, template='prompt_history_summarize')
                prompt_summary_ = logs.pop(0)['Message']
                response = logs.pop(0)['Message']
                summary_text = response.split('### RESPONSE:')[1].strip()
            self.save_log('Env', prompt_summary, template='prompt_base_summary')
            self.save_log(name, response, template='prompt_base_summary')

            # init script and background
            self.env_summary[name] = summary_text
            # init parameter
            self.role_parameter[name] = {
                'self_clues': '',
                'last_action': ['']
            }
            self.candidates[name] = {
                'query': 0,
                'query_value': 0,
                'query_all': 0,
                'query_probability': 0,
                'belief_value': 0,
                'belief_all': 0,
                'belief_probability': 0
            }
            self.address[name] = list(self.clues.keys())

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
                if logs[0]['Template'] == 'prompt_introduction':
                    prompt_introduction_ = logs.pop(0)['Message']
                    response = logs.pop(0)['Message']
                    introduction = response.split('### RESPONSE:')[1].strip()
                else:
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

        self.history_introduction = self.token_check(self.history_introduction) + '\n'

    def converse_stage(self, logs):
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
                if Config.force_expose and name in self.culprit:
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
                self.history = self.token_check(self.history)
            self.turns += 1

    def vote_stage(self):
        for name, description in self.env_summary.items():
            prompt_vote = self.prompt_vote.format(
                name=name,
                description=description,
                self_clues=self.role_parameter[name]['self_clues'],
                history=self.history_introduction+self.history,
                role_list=str(list(self.candidates.keys())),
            )
            while True:
                try:
                    if name in self.culprit:
                        response = Api(Config.Culprit_Model).run_api(prompt_vote)
                    else:
                        response = Api(Config.Civilian_Model).run_api(prompt_vote)
                    vote_response = response.split('### RESPONSE:')[1].strip()
                    try:
                        self.candidates[vote_response]['query'] += len(self.env_summary.keys()) * 1
                    except:
                        vote_character = re.findall('(.*?)\n', vote_response, re.DOTALL)[0]
                        self.candidates[vote_character]['query'] += len(self.env_summary.keys()) * 1
                    break
                except:
                    self.fail_num += 1
            self.save_log('Env', prompt_vote, template='prompt_vote')
            if name in self.culprit:
                self.save_log(name, response, template='prompt_vote', model=Config.Culprit_Model)
            else:
                self.save_log(name, response, template='prompt_vote', model=Config.Civilian_Model)

    def end_stage(self):
        query = dict()
        for name, para in self.candidates.items():
            query[name] = para['query']
        sorted_query = sorted(query.items(), key=lambda d: d[1], reverse=True)
        print('Doubt Ranking：')
        self.save_n_log('Env', 'Doubt Ranking：')
        for tp in sorted_query:
            print('{}：{}'.format(tp[0], tp[1]))
            self.save_n_log('Env', '{}：{}'.format(tp[0], tp[1]))
        print('\nVoted Culprit: {}。'.format(sorted_query[0][0]))
        self.save_n_log('Env', 'Voted Culprit: {}。'.format(sorted_query[0][0]))

        # fail num
        print('\nFailure Number of Parsing: {}'.format(self.fail_num))
        self.save_n_log('Env', '\nFailure Number of Parsing: {}'.format(self.fail_num))

        # query/belief probability
        for name in self.candidates:
            self.candidates[name]['query_probability'] = self.candidates[name]['query_value'] / self.candidates[name]['query_all']
            self.candidates[name]['belief_probability'] = self.candidates[name]['belief_value'] / self.candidates[name]['belief_all']
            print('Query Probability of 【{}】: {}'.format(name, self.candidates[name]['query_probability']))
            print('Belief Probability of 【{}】: {}'.format(name, self.candidates[name]['belief_probability']))
            self.save_n_log('Env', 'Query Probability of 【{}】: {}'.format(name, self.candidates[name]['query_probability']))
            self.save_n_log('Env', 'Belief Probability of 【{}】: {}'.format(name, self.candidates[name]['belief_probability']))

    def run(self, path):
        if path is None:
            logs = None
        else:
            logs = read_json(path)
        print("******************************Start******************************")

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

        # End Stage
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

    def save_log(self, user, text, template, model=Config.Base_Model):
        if Config.Console:
            if user != 'Env' and 'query' not in template and 'clue' not in template and 'belief' not in template:
                if 'eval' in template:
                    model = Config.Eval_Model
                if 'eval' in template and 'rouge' not in template:
                    print(user + ': ' + text.split('### RESPONSE:')[0].strip() + '\n')
                elif 'eval' in template and 'rouge' in template:
                    print(user + ': ' + text.split('### RESPONSE:')[0][12:].strip() + '\n')

                if 'rouge' in template:
                    print(user + ': ' + str(self.role_parameter[user]['eval_rouge']['f']) + '\n')
                else:
                    print(user + ': ' + text.split('### RESPONSE:')[1].replace('\n', '').strip() + '\n')
        if 'clue' in template:
            model = None
        self.logger.gprint(
            script_name=self.script_name,
            user=user,
            text=text,
            template=template,
            model=model,
            debug=self.debug,
            console=self.console
        )

    def save_n_log(self, user, text):
        self.logger.nprint(
            script_name=self.script_name,
            user=user,
            text=text,
            debug=self.debug,
            console=self.console
        )

    def llms_eval(self):
        print('LLMs Evaluation...')
        for name, background in self.env_summary.items():
            actions = ''
            for action in self.role_parameter[name]['last_action']:
                actions += action + '\n'
            prompt_eval = self.prompt_eval.format(
                name=name,
                description=self.env_summary[name],
                self_clues=self.role_parameter[name]['self_clues'],
                history=self.history_introduction+self.history,
                actions=actions,
                role_list=list(self.scripts.keys()),
                truth=self.truth,
            )
            while True:
                try:
                    response = Api(Config.Eval_Model).run_api(prompt_eval)
                    thought = response.split('### RESPONSE:')[0].strip()
                    score = int(response.split('### RESPONSE:')[1].strip())
                    break
                except:
                    self.fail_num += 1
            self.role_parameter[name]['eval_thought'] = thought
            self.role_parameter[name]['score'] = score

            self.save_log('Env', prompt_eval, template='prompt_eval')
            self.save_log(name, response, template='prompt_eval')

    def rouge_eval(self):
        print('Rouge Evaluation...')
        for name, background in self.env_summary.items():
            actions = ''
            for action in self.role_parameter[name]['last_action']:
                actions += action + '\n'
            prompt_eval_rouge = self.prompt_eval_rouge.format(
                name=name,
                history=self.history_introduction + self.history,
                actions=actions,
                role_list=list(self.scripts.keys()),
            )
            while True:
                try:
                    response = Api(Config.Eval_Model).run_api(prompt_eval_rouge)
                    thought = response.split('### RESPONSE:')[0].strip()
                    description = response.split('### RESPONSE:')[1].strip()
                    break
                except:
                    self.fail_num += 1
            self.role_parameter[name]['eval_thought_rouge'] = thought
            self.role_parameter[name]['eval_description'] = description
            self.role_parameter[name]['eval_rouge'] = cal_rouge_l(description, self.env_summary[name])

            self.save_log('Env', prompt_eval_rouge, template='prompt_eval_rouge')
            self.save_log(name, response, template='prompt_eval_rouge')

    def save_config(self):
        message = dict()
        if Config.DEBUG:
            print(message)
        for k, v in self.__dict__.items():
            if not isinstance(v, Logger):
                message[k] = v
        self.logger.messages.append(message)
        self.logger.log_fw.write(json.dumps(message, ensure_ascii=False, indent=1) + '\n')
