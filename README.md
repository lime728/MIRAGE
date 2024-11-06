# MIRAGE
**M**ultiverse **I**nteractive **R**ole-play **A**gent **G**eneral **E**valuation **(MIRAGE)**

## Introduction
We provide a simulation for LLMs-Based-Agents to evaluate their behavior in a complex role-playing game such as in a mystery murder game.

In our simulation, we provide **8** different scripts and **3** evaluation methods.

Here is a table of information of our scripts:

| ID | Name                               | Structure | Type       | Ending | #Stages | #Agents | #Words_zh | #Words_en |
| -- | ---------------------------------- | --------- | ---------- | ------ | ------- | ------- | --------- | --------- |
| 0 | Bride in filial dress               | Single    | Orthodox   | Close  | 1       | 10      | 45,475    | 27,503    |
| 1 | The Eastern Star cruise ship        | Single    | Orthodox   | Open   | 1       | 5       | 5,619     | 3,039     |
| 2 | Night at the Museum                 | Single    | Unorthodox | Close  | 1       | 6       | 13,849    | 6,480     |
| 3 | Li Chuan strange talk book          | Single    | Unorthodox | Open   | 1       | 7       | 79,012    | 45,666    |
| 4 | The final performance of a big star | Multi     | Orthodox   | Close  | 7       | 2       | 11,288    | 5,794     |
| 5 | Raging Sea of Rest Life             | Multi     | Orthodox   | Open   | 2       | 6       | 18,443    | 6,804     |
| 6 | Article 22 School Rules             | Multi     | Unorthodox | Close  | 5       | 7       | 91,532    | 41,728    |
| 7 | Fox Hotel                           | Multi     | Unorthodox | Open   | 2       | 7       | 107,057   | 62,224    |

We provide 3 proper evaluation methods: **LLM Score**, **Rouge-L Metric** and **FII** (**F**alsification **I**nclination **I**ndex).

Here is a average result of Script **The Eastern Star cruise ship** based on **GPT-4-Turbo** for evaluation:

| Base-Model | LLM-Score | Rouge-L | FII     |
| ---------- | --------- | ------- | ------- |
| GPT-3.5    | 78.2      | 0.253   | 0.472   |
| GPT-4      | 76.4      | 0.259   | 0.246   |
| GPT-4o     | 77.0      | 0.161   | 0.503   |

All configs can be found in [config.py](./config.py)

## Attention
The cost of **Context** Tokens of Script **The Eastern Star cruise ship** is 716,440->7.1644 USD.

The cost of **Completion** Tokens of Script **The Eastern Star cruise ship** is 53,630->1.6089 USD.

Take **GPT-4** as an example, 8 Scripts costs about **600** USD.

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
