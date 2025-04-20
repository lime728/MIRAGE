from pathlib import Path
import sys
import os
import time
import argparse

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]                          # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))                  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

parser = argparse.ArgumentParser()
parser.add_argument("--ScriptNumList", default=[0, 1, 2, 3, 4, 5, 6, 7], nargs="+", type=int, help="Chosen Script Numbers to run (From 0 to 7)  -- LOWER PRIORITY!")
parser.add_argument("--ScriptNum", default=None, type=int, help="Chosen Script Number (From 0 to 7) -- HIGHER PRIORITY!")
parser.add_argument("--Language", default="Zh", type=str, help="Script Language: ['En', 'Zh']")
parser.add_argument("--MaxTurnNum", default=5, type=int, help="Runnable Turn Number")
parser.add_argument("--MaxRetries", default=20, type=int, help="Max Retry in requests")
parser.add_argument("--MaxBaseScriptSummaryToken", default=1500, type=int, help="Max token length of base script summary")
parser.add_argument("--DEBUG", action="store_true", help="Debug Mode (Output all logs)")
parser.add_argument("--Console", action="store_true", help="Console mode (Only output conversation contents)")
parser.add_argument("--force_summary", action="store_true", help="Use force summary or not")
parser.add_argument("--Only_Eval", action="store_true", help="Eval with exist history script")
parser.add_argument("--OE_Path", default=None, type=str, help="Path of exist history script for only evaluation")
parser.add_argument("--LogDir", default=None, type=str, help="Log Dictionary")
parser.add_argument("--force_expose", action="store_true", help="Force to expose the culprits")
parser.add_argument("--Base_Model", default="gpt-4o-2024-08-06", type=str, help="Api-based model for base functionality")
parser.add_argument("--Culprit_Model", default='gpt-4o-2024-08-06', type=str, help="Api-based model for Culprits")
parser.add_argument("--Civilian_Model", default='gpt-4o-2024-08-06', type=str, help="Api-based model for Civilians")
parser.add_argument("--Eval_Model", default='gpt-4-turbo', type=str, help="Api based model for Evaluation")
args = parser.parse_args()


class Config:
    # API
    Small_LLM = [
        'Qwen2-7B-Instruct',
    ]
    ApiData = {
        "OpenAI": {
            "url": "<Your OpenAI URL>",
            "key": "<Your OpenAI KEY>"
        },
        "Qwen2-7B-Instruct": {
            "url": "<Your API URL>",
            "key": "<Your API KEY>"
        }
    }
    
    # Base Directory
    DataDir = ROOT / 'dataset' / args.Language
    PromptDir = ROOT / 'prompts' / args.Language
    if args.LogDir:
        LogDir = ROOT / 'logs' / args.LogDir
    else:
        LogDir = ROOT / 'logs'
    if not os.path.exists(LogDir):
        os.makedirs(LogDir)

    # Truth
    ScriptTruth = DataDir / 'Truth.json'

    # Script Directories
    ScriptDirs = sorted([path for path in DataDir.iterdir() if not path.name.endswith('.json')])
    try:
        # Windows
        ScriptNames = sorted([str(path).split('\\')[2] for path in DataDir.iterdir() if not path.name.endswith('.json')])
    except:
        # Linux
        ScriptNames = sorted([str(path).split('/')[2] for path in DataDir.iterdir() if not path.name.endswith('.json')])
    ScriptPaths = dict()
    for script in ScriptDirs:
        if not script.name.endswith('.json'):
            try:
                # Windows
                ScriptPaths[str(script).split('\\')[2]] = sorted([path for path in script.iterdir()])
            except:
                # Linux
                ScriptPaths[str(script).split('/')[2]] = sorted([path for path in script.iterdir()])
    # Prompt Paths
    PromptPaths = sorted([path for path in PromptDir.iterdir()])

    # Log Paths
    LogPaths = sorted([path for path in LogDir.iterdir()])
    LogPath = LogDir / ('log_' + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())))
    if not os.path.exists(LogPath):
        os.makedirs(LogPath)


for k, v in vars(args).items():
    setattr(Config, k, v)

