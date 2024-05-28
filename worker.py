from ScriptEnvs import NFO, NFC, NPO, NPC, AFO, AFC, APO, APC
from utils import Config
import time
from data_loader import *


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
        print("Running Environment 《{}》...".format(self.ScriptName))
        st_time = time.time()
        self.ScriptEnv.run()
        ed_time = time.time()
        time_used = calculate_time_used(st_time, ed_time)
        print('Time used: {}'.format(time_used))

    def eval_env(self):
        print("Evaluation Step...")
        self.ScriptEnv.eval()
