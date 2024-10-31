from pathlib import Path
import sys
import os
import time

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]                          # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))                  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


class Config:
    # Manual Configs
    ScriptNumList = [0, 1, 2, 3, 4, 5, 6, 7]    # Chosen Script Numbers to run (From 0 to 7)  -- LOWER PRIORITY!
    ScriptNum = None                            # Chosen Script Number (From 0 to 7 and None) -- HIGHER PRIORITY!
    Language = 'Zh'                             # Script Language: ['En', 'Zh']
    MaxTurnNum = 5                              # Runnable Turn Number
    MaxRetries = 20                             # Max Retry in requests
    MaxBaseScriptSummaryToken = 1500            # Max token length of base script summary
    DEBUG = False                               # debug mode (Output all logs)
    Console = True                              # console mode (Only output conversation contents)
    force_summary = True                        # Use force summary or not
    Only_Eval = False                           # Eval with exist history script
    force_expose = False                        # Force to expose the culprits

    # Models
    '''
    Small Model:
        Qwen2-7B-Instruct
        Qwen1.5-7B-Chat
        Qwen-7B-Chat
        glm-4-9b-chat
        Yi-1.5-9B-Chat
    OpenAI Model:
        gpt-4-turbo
        gpt-3.5-turbo
        gpt-4o
    '''
    Base_Model = 'Qwen2-7B-Instruct'            # Api-based model
    Culprit_Model = 'Qwen2-7B-Instruct'         # Api-based model
    Civilian_Model = 'Qwen2-7B-Instruct'        # Api-based model

    # Eval Models
    # Eval_Model = 'gpt-4-turbo'                  # Eval Api-based model
    Eval_Model = 'Qwen2-7B-Instruct'                  # Eval Api-based model

    # API
    Small_LLM = [
        'Qwen2-7B-Instruct',
        'Qwen1.5-7B-Chat',
        'Qwen-7B-Chat',
        'glm-4-9b-chat',
        'Yi-1.5-9B-Chat'
    ]
    ApiData = {
        "OpenAI": {
            "url": "<Your Url>",
            "key": "<Your Key>"
        },
        "Qwen2-7B-Instruct": {
            "url": "<Your Url>",
            "key": "<Your Key>"
        }
    }

    # Exist history script for Eval
    OE_Path = None

    # Base Directory
    DataDir = ROOT / 'dataset' / Language
    PromptDir = ROOT / 'prompts' / Language
    LogDir = ROOT / 'logs'
    if not os.path.exists(LogDir):
        os.makedirs(LogDir)

    # Truth
    ScriptTruth = DataDir / 'Truth.json'

    # Script Directories
    ScriptDirs = [path for path in DataDir.iterdir() if not path.name.endswith('.json')]
    try:
        # Windows
        ScriptNames = [str(path).split('\\')[2] for path in DataDir.iterdir() if not path.name.endswith('.json')]
    except:
        # Linux
        ScriptNames = [str(path).split('/')[2] for path in DataDir.iterdir() if not path.name.endswith('.json')]
    ScriptPaths = dict()
    for script in ScriptDirs:
        if not script.name.endswith('.json'):
            try:
                # Windows
                ScriptPaths[str(script).split('\\')[2]] = [path for path in script.iterdir()]
            except:
                # Linux
                ScriptPaths[str(script).split('/')[2]] = [path for path in script.iterdir()]
    # Prompt Paths
    PromptPaths = [path for path in PromptDir.iterdir()]

    # Log Paths
    LogPaths = [path for path in LogDir.iterdir()]
    LogPath = LogDir / ('log_' + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())))
    if not os.path.exists(LogPath):
        os.makedirs(LogPath)
