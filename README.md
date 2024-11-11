# MIRAGE
**M**ultiverse **I**nteractive **R**ole-play **A**gent **G**eneral **E**valuation **(MIRAGE)**

## Introduction
We provide a simulation for LLMs-Based-Agents to evaluate their behavior in a complex role-playing game such as in a mystery murder game.

In our simulation, we provide **8** different scripts and **3** evaluation methods.

Here is a table of information of our scripts:

| ID | Name                               | Structure | Type       | Ending | #Stages | #Agents | #Clues | #Words_zh | #Words_en |
| -- | ---------------------------------- | --------- | ---------- | ------ | ------- | ------- | ------ | --------- | --------- |
| 0 | Bride in filial dress               | Single    | Orthodox   | Close  | 1       | 10      | 39     | 45,475    | 27,503    |
| 1 | The Eastern Star cruise ship        | Single    | Orthodox   | Open   | 1       | 5       | 42     | 5,619     | 3,039     |
| 2 | Night at the Museum                 | Single    | Unorthodox | Close  | 1       | 6       | 82     | 13,849    | 6,480     |
| 3 | Li Chuan strange talk book          | Single    | Unorthodox | Open   | 1       | 7       | 14     | 79,012    | 45,666    |
| 4 | The final performance of a big star | Multi     | Orthodox   | Close  | 7       | 2       | 17     | 11,288    | 5,794     |
| 5 | Raging Sea of Rest Life             | Multi     | Orthodox   | Open   | 2       | 6       | 27     | 18,443    | 6,804     |
| 6 | Article 22 School Rules             | Multi     | Unorthodox | Close  | 5       | 7       | 17     | 91,532    | 41,728    |
| 7 | Fox Hotel                           | Multi     | Unorthodox | Open   | 2       | 7       | 46     | 107,057   | 62,224    |

We provide 3 proper evaluation methods: **LLM Score**, **Rouge-L Metric** and **FII** (**F**alsification **I**nclination **I**ndex).

Here is a complete result of All Scripts:

| Base Model         | Judge Model        | Culprit Model      | Civilian Model      | Eval Model  | Env Tokens / Envs | User Tokens / Users | #Failure | #Clues | Culprit Victory | LLM-Score | Rouge-L | FII   |
| ------------------ | ------------------ | ------------------ | ------------------- | ----------- | ----------------- | ------------------- | -------- | ------ | --------------- | --------- | ------- | ----- |
| gpt-3.5-turbo-0125 | gpt-3.5-turbo-0125 | gpt-3.5-turbo-0125 | gpt-3.5-turbo-0125  | gpt-4-turbo | 2,356,042 / 876   | 97,863 / 542        | 5.4      | 7.0    | 87.50 / 84.94   | 78.7      | 0.242   | 0.459 |
| gpt-4-turbo        | gpt-4-turbo        | gpt-4-turbo        | gpt-4-turbo         | gpt-4-turbo | 2,085,857 / 723   | 204,997 / 544       | 6.4      | 5.6    | 100.00 / 84.94  | 83.9      | 0.244   | 0.204 |
| Qwen2-7B-Instruct  | Qwen2-7B-Instruct  | Qwen2-7B-Instruct  | Qwen2-7B-Instruct   | gpt-4-turbo | 1,664,279 / 684   | 183,536 / 548       | 7.3      | 3.7    | 87.50 / 84.94   | 83.8      | 0.251   | 0.116 |
| glm-4-9b-chat      | glm-4-9b-chat      | glm-4-9b-chat      | glm-4-9b-chat       | gpt-4-turbo | 2,978,766 / 1,153 | 150,108 / 544       | 24.4     | 5.7    | 75.00 / 84.94   | 84.0      | 0.218   | 0.411 |
| Qwen2-7B-Instruct  | Qwen2-7B-Instruct  | Qwen2-7B-Instruct  | Qwen-7B-Chat        | gpt-4-turbo | /                 | /                   | 180.1    | /      | /               | 82.1      | 0.234   | 0.217 |
| Qwen2-7B-Instruct  | Qwen2-7B-Instruct  | Qwen2-7B-Instruct  | Qwen1.5-7B-Instruct | gpt-4-turbo | /                 | /                   | 41.1     | /      | /               | 84.6      | 0.233   | 0.210 |
| Qwen2-7B-Instruct  | Qwen2-7B-Instruct  | Qwen2-7B-Instruct  | Yi-1.5-9B-Chat      | gpt-4-turbo | /                 | /                   | 57.8     | /      | /               | 82.4      | 0.233   | 0.230 |
| Qwen2-7B-Instruct  | Qwen2-7B-Instruct  | Qwen2-7B-Instruct  | glm-4-9b-chat       | gpt-4-turbo | /                 | /                   | 17.3     | /      | /               | 82.4      | 0.247   | 0.243 |
| Qwen2-7B-Instruct  | /                  | Qwen2-7B-Instruct  | Qwen-7B-Chat        | gpt-4-turbo | /                 | /                   | 218.9    | /      | /               | 80.9      | 0.247   | 0.385 |
| Qwen2-7B-Instruct  | /                  | Qwen2-7B-Instruct  | Qwen1.5-7B-Instruct | gpt-4-turbo | /                 | /                   | 94.3     | /      | /               | 85.2      | 0.240   | 0.219 |
| Qwen2-7B-Instruct  | /                  | Qwen2-7B-Instruct  | Yi-1.5-9B-Chat      | gpt-4-turbo | /                 | /                   | 1481.0   | /      | /               | 84.1      | 0.248   | 0.369 |
| Qwen2-7B-Instruct  | /                  | Qwen2-7B-Instruct  | glm-4-9b-chat       | gpt-4-turbo | /                 | /                   | 51.4     | /      | /               | 82.6      | 0.237   | 0.307 |

Here is an average result of Script **The Eastern Star cruise ship** based on **gpt-4-turbo** for evaluation:

| Model              | LLM-Score | Rouge-L | FII     |
| ------------------ | --------- | ------- | ------- |
| gpt-3.5-turbo-0125 | 78.2      | 0.253   | 0.472   |
| gpt-4              | 76.4      | 0.259   | 0.246   |
| gpt-4o             | 77.0      | 0.161   | 0.503   |

All configs can be found in [config.py](./config.py)

## Quick Start
### Requirements
First, Install requirements:
```bash
pip install -r requirements.txt
```
Second, Add your Api Key at [config.py](./config.py)

Finally, Start simulation:
```bash
python main.py
```
