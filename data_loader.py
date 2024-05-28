import json
import tiktoken
import re
from datetime import datetime


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


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=1))


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


def load_log(path, debug=False, console=True):
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


if __name__ == '__main__':
    log_path = '.\storage\log_2024_03_20_17_59_15_gpt_4_turbo\东方之星号游轮事件\history.json'
    load_log(log_path, debug=False, console=True)
    # calculate_token(log_path)
