from pathlib import Path
import sys
import os
import time

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


class Config:
    # Manual Configs
    ScriptNumList = [0, 1, 2, 3, 4, 5, 6, 7]    # Chosen Script Numbers to run (From 0 to 7)
    ScriptNum = 0                               # Chosen Script Number (From 0 to 7)
    MaxTurnNum = 5                              # Runnable Turn Number
    MaxRetries = 20                             # Max Retry in requests
    MaxBaseScriptSummaryToken = 1500            # Max token length of base script summary
    DEBUG = False                               # debug mode
    Console = True                              # console mode
    # Model = 'gpt-3.5-turbo-0125'                # Api-based model
    Model = 'gpt-4-1106-preview'                # Api-based model
    # Model = 'gpt-4-turbo'                       # Api-based model
    # Model = 'gpt-4o'                            # Api-based model
    force_summary = True                        # Use force summary or not
    # Eval Configs
    # Eval_Model = 'gpt-3.5-turbo-0125'           # Eval Api-based model
    Eval_Model = 'gpt-4-1106-preview'           # Eval Api-based model
    # Eval_Model = 'gpt-4-turbo'                  # Eval Api-based model
    # Eval_Model = 'gpt-4o'                       # Eval Api-based model
    Only_Eval = True                            # Eval with exist history script
    # Exist history script for Eval
    OE_Path = ROOT / 'storage' / 'compare_gpt_4' / '东方之星号游轮事件_gpt_4' / 'history.json'

    # Base Directory
    DataDir = ROOT / 'dataset'
    PromptDir = ROOT / 'prompts'
    LogDir = ROOT / 'logs'

    # Truth
    ScriptTruth = DataDir / 'Truth.json'

    # Script Directories
    ScriptDirs = [path for path in DataDir.iterdir() if not path.name.endswith('.json')]
    ScriptNames = [str(path).split('\\')[1] for path in DataDir.iterdir() if not path.name.endswith('.json')]
    ScriptPaths = dict()
    for script in ScriptDirs:
        if not script.name.endswith('.json'):
            ScriptPaths[str(script).split('\\')[1]] = [path for path in script.iterdir()]

    # Prompt Paths
    PromptPaths = [path for path in PromptDir.iterdir()]

    # Log Paths
    LogPaths = [path for path in LogDir.iterdir()]
    LogPath = LogDir / ('log_' + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())))
    if not os.path.exists(LogPath):
        os.makedirs(LogPath)
