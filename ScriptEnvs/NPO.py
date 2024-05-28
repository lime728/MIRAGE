# 怒海余生
# Raging Sea of Rest Life
# TYPE: Normal Part Open

from ScriptEnvs.BaseEnv import BaseEnv


class NPO(BaseEnv):
    def __init__(self, script_name, script_files):
        super().__init__(script_name, script_files)

    def run(self):
        print("******************************Start******************************")

        # part scripts
        part_scripts = self.scripts
        self.scripts = dict()
        for script_num, part_script in part_scripts.items():
            print('***************{}***************'.format(script_num))
            if self.scripts == dict():
                self.scripts = part_script
                first_turn = True
            else:
                self.add_script(part_script)
                first_turn = False

            # Initial base environment
            print('********************Init Stage********************')
            self.init_stage()
            print('Init Stage Over...')

            if first_turn:
                # self-introduction
                print('********************Self-introduction Stage********************')
                self.self_introduction_stage()
                print('Self-introduction Stage Over...')

            # start converse
            print('********************Converse Stage********************')
            self.converse_stage()
            print('Converse Stage Over...')

        # Vote Stage
        print('********************Vote Stage********************')
        self.vote_stage()
        print('Vote Stage Over...')

        # End stage
        print('********************End Stage********************')
        self.end_stage()
        print('End Stage Over...')

        self.logger.close()
        print("******************************Finish******************************")
