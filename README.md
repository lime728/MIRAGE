# MPIRD-LLMA
Multiverse Phantasm Interactive Role-play Dataset for Large Language Model Agents

## Introduction
We provide a simulation for LLMs-Based-Agents to evaluate their behavior in a complex role-playing game such as in a mystery murder game.

In our simulation, we provide **8** different scripts and **2** evaluation methods.

Here is a table of information of our scripts:

| ID | Name                               | Structure | Type       | Ending | #Stages | #Agents | #Words_zh |
| -- | ---------------------------------- | --------- | ---------- | ------ | ------- | ------- | --------- |
| 0 | Bride in filial dress               | Full      | Orthodox   | Close  | 1       | 10      | 45,475    |
| 1 | The Eastern Star cruise ship        | Full      | Orthodox   | Open   | 1       | 5       | 5,619     |
| 2 | Night at the Museum                 | Full      | Unorthodox | Close  | 1       | 6       | 13,849    |
| 3 | Li Chuan strange talk book          | Full      | Unorthodox | Open   | 1       | 7       | 79,012    |
| 4 | The final performance of a big star | Staged    | Orthodox   | Close  | 7       | 2       | 11,288    |
| 5 | Raging Sea of Rest Life             | Staged    | Orthodox   | Open   | 2       | 6       | 18,443    |
| 6 | Article 22 School Rules             | Staged    | Unorthodox | Close  | 5       | 7       | 91,532    |
| 7 | Fox Hotel                           | Staged    | Unorthodox | Open   | 2       | 7       | 107,057   |

We provide 2 proper evaluation methods: **LLM_Score** and **Rouge_L**.

Here is a average result of Script **The Eastern Star cruise ship** based on **GPT-4-Turbo** for evaluation:

| Base_Model | LLM_Score | Rouge_L |
| ---------- | --------- | ------- |
| GPT-3.5    | 78.2      | 0.253   |
| GPT-4      | 76.4      | 0.259   |
| GPT-4o     | 77.0      | 0.161   |

All configs can be found in [config.py](./config.py)

## Attention
The cost of **Context** Tokens of Script **The Eastern Star cruise ship** is 716,440->7.1644 USD.

The cost of **Completion** Tokens of Script **The Eastern Star cruise ship** is 53,630->1.6089 USD.

Take **GPT-4** as an example, it costs about **8.7733** USD.

## Quick Start
### Requirements
First, Install requirements:
```bash
pip install -r requirements.txt
```
Second, Add your Api Key at [api.py](./api.py)

Finally, Start simulation:
```bash
python main.py
```
