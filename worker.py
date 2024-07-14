from ScriptEnvs import NFO, NFC, NPO, NPC, AFO, AFC, APO, APC, BaseEnv
from utils import Config
from logger import Logger
from pathlib import Path
from data_loader import *
import time


class MainWorker:
    def __init__(self, script_num=None):
        if script_num is not None:
            self.ScriptName = Config.ScriptNames[script_num]
        else:
            self.ScriptName = Config.ScriptNames[Config.ScriptNum]
        self.ScriptFiles = Config.ScriptPaths[self.ScriptName]
        # ScriptNum 0
        if self.ScriptName == "东方之星号游轮事件":
            self.ScriptEnv = NFO.NFO(self.ScriptName, self.ScriptFiles)
        # ScriptNum 1
        elif self.ScriptName == "博物馆奇妙夜":
            self.ScriptEnv = AFC.AFC(self.ScriptName, self.ScriptFiles)
        # ScriptNum 2
        elif self.ScriptName == "大明星最后的演出":
            self.ScriptEnv = NPC.NPC(self.ScriptName, self.ScriptFiles)
        # ScriptNum 3
        elif self.ScriptName == "孝衣新娘":
            self.ScriptEnv = NFC.NFC(self.ScriptName, self.ScriptFiles)
        # ScriptNum 4
        elif self.ScriptName == "怒海余生":
            self.ScriptEnv = NPO.NPO(self.ScriptName, self.ScriptFiles)
        # ScriptNum 5
        elif self.ScriptName == "漓川怪谈簿":
            self.ScriptEnv = AFO.AFO(self.ScriptName, self.ScriptFiles)
        # ScriptNum 6
        elif self.ScriptName == "狐狸旅馆":
            self.ScriptEnv = APO.APO(self.ScriptName, self.ScriptFiles)
        # ScriptNum 7
        elif self.ScriptName == "第二十二条校规":
            self.ScriptEnv = APC.APC(self.ScriptName, self.ScriptFiles)
        else:
            raise ValueError('Unaccepted ScriptName')

    def run_env(self):
        st_time = time.time()

        # Run Step
        print("Running Environment 《{}》...".format(self.ScriptName))
        self.ScriptEnv.run()

        ed_time = time.time()
        time_used = calculate_time_used(st_time, ed_time)
        print('Time used: {}'.format(time_used))


class EvalWorker(BaseEnv.BaseEnv):
    def __init__(self):
        pass

    def run_env(self, path):
        # global configs
        self.configs = dict()
        for k, v in Config.__dict__.items():
            if '__' in k:
                continue
            if isinstance(v, Path):
                self.configs[k] = str(v)
            elif type(v) == list and isinstance(v[0], Path):
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

        # init by load
        log_history, configs = load_log(path)
        for k, v in configs.items():
            setattr(self, k, v)
        self.logger = Logger(self.script_name)
        self.logger.messages = log_history

        st_time = time.time()

        # Run Step
        print("Evaluating Environment 《{}》 from Path:\"{}\"...".format(self.script_name, path))
        self.llms_eval()
        self.rouge_eval()
        self.save_config()
        self.logger.close()
        print('Evaluation Finished...')

        ed_time = time.time()
        time_used = calculate_time_used(st_time, ed_time)
        print('Time used: {}'.format(time_used))
