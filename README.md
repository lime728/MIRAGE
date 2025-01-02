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
Below is the Total Average Results for a single simulation in each MIRAGE scenario.
**Env Tokens** refer to the number of environment input tokens, and **Envs** represent the total requests, including all environment-related actions.
**User Tokens** denote the number of LLM output tokens, and **Users** represent completions excluding summarization or clue investigation.
**Victory** shows the MRR score of the result of voting.
**TII**, **CIC**, **ICI** and **SCI** respectively represent the **TII**, **CIC**, **ICI** and **SCI** scores of LLMs during the games.
| **Model**        | **Env Tokens** / **Envs** | **User Tokens** / **Users** | **Victory** | **TII**   | **CIC**   | **ICI**   | **SCI**   |
|------------------|----------------------------|------------------------------|-------------|-----------|-----------|-----------|-----------|
| GPT-3.5          | 2,719,895 / 883            | 121,378 / 580                | 29.11       | 47.13     | 27.46     | 70.06     | 49.10     |
| GPT-4            | 2,431,142 / 759            | 172,128 / 587                | 34.69       | 76.32     | 19.01     | 76.54     | 50.42     |
| GPT-4o           | 6,252,580 / 1,328          | 204,772 / 574                | 47.01       | **78.69** | **35.92** | **76.80** | **51.29** |
| Qwen-2-7B       | 2,204,029 / 743            | 192,158 / 588                | **51.81**   | 75.78     | 18.66     | 74.92     | 50.57     |
| GLM-4-9B        | 4,071,805 / 1,328          | 204,772 / 574                | 31.89       | 53.85     | 20.07     | 71.60     | 48.13     |


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
