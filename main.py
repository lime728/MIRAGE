from utils import *


def main():
    if Config.ScriptNum is not None:
        worker = MainWorker(Config.ScriptNum)
        worker.run_env()
        worker.eval_env()
    elif Config.ScriptNumList is not None:
        for worker_num in Config.ScriptNumList:
            worker = MainWorker(worker_num)
            worker.run_env()
            worker.eval_env()
    else:
        raise ValueError("'ScriptNum' or 'ScriptNumList' should be settled!")


if __name__ == '__main__':
    main()
