# 博物馆奇妙夜
# Night at the Museum
# TYPE: Single Orthodox Close

from ScriptEnvs.BaseEnv import BaseEnv


class SUC(BaseEnv):
    def __init__(self, script_name, script_files):
        super().__init__(script_name, script_files)
        if self.configs['Language'] == 'Zh':
            self.culprit.append('撒干事')
        elif self.configs['Language'] == 'En':
            self.culprit.append('Manager Sa')
