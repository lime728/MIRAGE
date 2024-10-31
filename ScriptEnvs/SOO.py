# 东方之星号游轮事件
# The Eastern Star cruise ship
# TYPE: Single Orthodox Open

from ScriptEnvs.BaseEnv import BaseEnv


class SOO(BaseEnv):
    def __init__(self, script_name, script_files):
        super().__init__(script_name, script_files)
        if self.configs['Language'] == 'Zh':
            self.culprit.append('修经理')
        elif self.configs['Language'] == 'En':
            self.culprit.append('Manager Xiu')
        