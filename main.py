from utils import *


def main():
    if Config.Only_Eval:
        worker = EvalWorker()
        worker.run_env(Config.OE_Path)
    else:
        if Config.ScriptNum is not None:
            worker = MainWorker(Config.ScriptNum)
            worker.run_env(path=None)
        elif Config.ScriptNumList is not None:
            for worker_num in Config.ScriptNumList:
                worker = MainWorker(worker_num)
                worker.run_env(path=None)
        else:
            raise ValueError("'ScriptNum' or 'ScriptNumList' should be settled!")


if __name__ == '__main__':
    main()
