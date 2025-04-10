import json
import tiktoken
from datetime import datetime
import pickle
from rouge_chinese import Rouge
import jieba, re


def cal_rouge_l(predict, truth):
    if predict == '' or truth == '':
        return 0
    else:
        predict_ = ' '.join(jieba.cut(predict))
        truth_ = ' '.join(jieba.cut(truth))
        return Rouge().get_scores(predict_, truth_)[0]['rouge-l']['f']


def read_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    if '<promptcontent>###</promptcontent>' in data:
        data = data.split('<promptcontent>###</promptcontent>')[1].strip()
    return data


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    return data


def read_pickle(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=1))


def write_pickle(path, data):
    with open(path,'wb') as f:
        pickle.dump(data, f)


def token_calculate(text, model_name='gpt-4'):
    encoding = tiktoken.encoding_for_model(model_name)
    token_length = len(encoding.encode(text))
    return token_length


def calculate_time_used(st_time, ed_time):
    time1 = datetime.fromtimestamp(st_time)
    time2 = datetime.fromtimestamp(ed_time)
    time_used = time2 - time1
    hours, remainder = divmod(time_used.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours < 10:
        hours = '0' + str(hours)
    if minutes < 10:
        minutes = '0' + str(minutes)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return "{}:{}:{}".format(hours, minutes, seconds)


def load_log(path):
    try:
        logs = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                logs.append(json.loads(line))
    except:
        logs = read_json(path)
    log_history = list()
    configs = logs.pop(-1)
    for sentence in logs:
        if 'Template' in sentence.keys():
            if 'eval' in sentence['Template']:
                continue
        log_history.append(sentence)
    return log_history, configs


def print_log(path, debug=False, console=True):
    try:
        logs = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                logs.append(json.loads(line))
    except:
        logs = read_json(path)
    for dialog in logs:
        if debug:
            print('{name}: \n{message}'.format(
                name=dialog['Name'],
                message=dialog['Message']
            ))
        elif console:
            if dialog == logs[-1]:
                continue
            if 'Failure' in dialog['Message']:
                print('{name}: {message}'.format(
                    name=dialog['Name'],
                    message=dialog['Message'].strip()
                ))
            if dialog['Name'] == 'Env':
                continue
            if '线索' in dialog['Name']:
                print('{name}: {message}'.format(
                    name=dialog['Name'],
                    message=dialog['Message'].strip()
                ))
            else:
                print('{name}: {message}'.format(
                    name=dialog['Name'],
                    message=dialog['Message'].split('### RESPONSE:')[1].strip()
                ))
        else:
            pass


def calculate_token(path):
    try:
        logs = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                logs.append(json.loads(line))
    except:
        logs = read_json(path)

    env_token_num = 0
    user_token_num = 0
    env_num = 0
    user_num = 0
    for dialog in logs:
        if 'TokenLength' in dialog.keys():
            if dialog['Name'] == 'Env':
                env_token_num += dialog['TokenLength']
                env_num += 1
            else:
                user_token_num += dialog['TokenLength']
                user_num += 1
    print('**********{}**********'.format('Token Calculation'))
    print('Env Token: {}'.format(env_token_num))
    print('Env Num: {}'.format(env_num))
    print('User Token: {}'.format(user_token_num))
    print('User Num: {}'.format(user_num))
