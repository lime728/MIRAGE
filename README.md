# MIRAGE: Exploring How Large Language Models Perform in Complex Social Interactive Environments
**M**ultiverse **I**nteractive **R**ole-play **A**bility **G**eneral **E**valuation **(MIRAGE)**

## 🎉 Introduction
We provide a simulation for LLMs-Based-Agents to evaluate their behavior in a complex role-playing game such as in a mystery murder game.

In our simulation, we provide **8** different scripts and **4** evaluation methods.

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

We provide 4 proper evaluation methods: **TII** (**T**rust **I**nclination **I**ndex), **CIC** (**C**lue **I**nvestigation **C**apability), **ICI** (**I**nteractivity **C**apability **I**ndex) and **SCI** (**S**cript **C**ompliance **I**ndex).

More experimental content and analysis can be found in the paper [MIRAGE: Exploring How Large Language Models Perform in Complex Social Interactive Environments]().

All configs can be found in [config.py](./config.py)

## 🔥 Updates
* 2025/01/02: We released the first version of our [paper](https://arxiv.org/abs/2406.10621).

## 💡 Leaderboard
Below

## ⚙️ Quick Start
### Requirements
First, Install requirements:
```bash
pip install -r requirements.txt
```
Second, Add your Api Url and Api Key at [config.py](./config.py)

Finally, Start simulation:
```bash
bash run.sh
```
