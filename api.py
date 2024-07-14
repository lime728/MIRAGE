import time
from openai import OpenAI
import requests
import json
from config import Config
from zhipuai import ZhipuAI

ApiData = {
    "OhMyGPT": {
        "url": "https://cn2us02.opapi.win/v1/",
        "key": "<Your Api Key Here>"
    },
    "GLM": {
        "url": "https://open.bigmodel.cn/api/paas/v4/",
        "key": "<Your Api Key Here>"
    },
    "Support": {
        "url": "https://api.pumpkinaigc.online/v1",
        "key": "<Your Api Key Here>"
    }
}

'''
OhMyGPT:
[
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-4-32k-0613",
    "gpt-4-1106-preview",
    "gpt-4-vision-preview",
    "text-davinci-003",
    "text-davinci-002",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
    "text-embedding-ada-002",
    "text-search-ada-doc-001",
    "dall-e",
    "text-davinci-edit-001",
    "code-davinci-edit-001",
    "whisper-1",
    "claude-2-web"
]
ChatGLM:
[
    "glm-4",
    "glm-4v",
    "glm-3-turbo"
]
'''


class Api:
    def __init__(
            self,
            model='gpt-4-1106-preview',
            output_console=False
    ):
        self.model = model
        if 'glm' in self.model:
            self.url = ApiData['GLM']['url']
            self.key = ApiData['GLM']['key']
            self.client = ZhipuAI(
                base_url=self.url,
                api_key=self.key
            )
        else:
            self.url = ApiData['Support']['url']
            self.key = ApiData['Support']['key']
            # self.url = ApiData['OhMyGPT']['url']
            # self.key = ApiData['OhMyGPT']['key']
            self.client = OpenAI(
                base_url=self.url,
                api_key=self.key
            )
        self.gpt_params = {
            "temperature": 0.8,
            "top_p": 1,
            "stream": False,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": None
        }
        self.messages = list()
        self.output_console = output_console

    def run_api(self, message):
        if self.model in ['GPT3.5', 'GPT4', 'GPT4-turbo', 'Embedding']:
            return self.run_with_request(message)
        else:
            return self.run_with_client(message)

    def run_with_request(self, message):
        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )
        payload = {
            "messages": self.messages
        }
        payload.update(self.gpt_params)
        retry = 0
        while retry < Config.MaxRetries:
            try:
                response = requests.post(
                    url=self.url,
                    headers=self.headers,
                    data=json.dumps(payload)
                )
            except:
                retry += 1
                time.sleep(5 * retry)
                continue
            try:
                result = json.loads(response.text)['choices'][0]['message']['content']
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": result
                    }
                )
                break
            except Exception as e:
                print('Api Failed with Exception {}'.format(e))
                try:
                    print(response.text)
                except:
                    pass
                retry += 1
                time.sleep(5 * retry)
        if retry >= Config.MaxRetries:
            raise Exception('Over Max Retries!')
        return result

    def run_with_client(self, message, stream=False):
        self.gpt_params['stream'] = stream
        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )
        retry = 0
        while retry < Config.MaxRetries:
            try:
                if 'glm' in self.model:
                    completion = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages,
                        temperature=self.gpt_params["temperature"],
                        stream=self.gpt_params["stream"],
                        stop=self.gpt_params["stop"]
                    )
                else:
                    completion = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages,
                        temperature=self.gpt_params["temperature"],
                        top_p=self.gpt_params["top_p"],
                        stream=self.gpt_params["stream"],
                        frequency_penalty=self.gpt_params["frequency_penalty"],
                        presence_penalty=self.gpt_params["presence_penalty"],
                        stop=self.gpt_params["stop"]
                    )
            except:
                retry += 1
                time.sleep(5 * retry)
                continue
            try:
                if self.gpt_params["stream"]:
                    stream_result = ''
                    for chunk in completion:
                        if (chunk.choices[0].delta.content == None or chunk.choices[0].delta.content == '') and stream_result != '':
                            return stream_result
                        stream_result += chunk.choices[0].delta.content
                        if self.output_console:
                            print(chunk.choices[0].delta.content.replace("\n", "\\n"), end='', flush=True)
                result = completion.choices[0].message.content
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": result
                    }
                )
                break
            except Exception as e:
                print('Api Failed with Exception {}'.format(e))
                retry += 1
                time.sleep(5 * retry)
        if retry >= Config.MaxRetries:
            raise Exception('Over Max Retries!')
        return result


if __name__ == "__main__":
    message = 'Hello! How are you?'
    # model_request = 'GPT4-turbo'
    model_client_1 = 'gpt-4o'
    model_client_2 = 'glm-4'
    # Test run_with_request
    # request_response = Api(model_request).run_with_request(message)
    # print('\n{} request output: {}\n'.format(model_request, request_response))
    # Test run_with_client
    client_response_1 = Api(model_client_1).run_with_client(message)
    print('\n{} client output: {}\n'.format(model_client_1, client_response_1))
    client_response_2 = Api(model_client_2).run_with_client(message)
    print('\n{} client output: {}\n'.format(model_client_2, client_response_2))
