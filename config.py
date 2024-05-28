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
    Model = 'gpt-3.5-turbo-16k-0613'                # Api-based GPT model
    # Model = 'glm-4'                             # Api-based GLM model
    force_summary = True                        # Use force summary or not

    # Base Directory
    DataDir = ROOT / 'dataset'
    PromptDir = ROOT / 'prompts'
    LogDir = ROOT / 'logs'

    # Script Directories
    ScriptDirs = [path for path in DataDir.iterdir()]
    ScriptNames = [str(path).split('\\')[1] for path in DataDir.iterdir()]
    ScriptPaths = dict()
    for script in ScriptDirs:
        ScriptPaths[str(script).split('\\')[1]] = [path for path in script.iterdir()]

    # Prompt Paths
    PromptPaths = [path for path in PromptDir.iterdir()]

    # Log Paths
    LogPaths = [path for path in LogDir.iterdir()]
    LogPath = LogDir / ('log_' + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())))
    if not os.path.exists(LogPath):
        os.makedirs(LogPath)
