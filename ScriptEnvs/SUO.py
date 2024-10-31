# 漓川怪谈簿
# Li Chuan strange talk book
# TYPE: Single Unorthodox Open

from ScriptEnvs.BaseEnv import BaseEnv


class SUO(BaseEnv):
    def __init__(self, script_name, script_files):
        super().__init__(script_name, script_files)
        if self.configs['Language'] == 'Zh':
            self.culprit.append('衣衫褴褛的老人')
        elif self.configs['Language'] == 'En':
            self.culprit.append('Elderly in Tattered')
