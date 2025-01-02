import time
from openai import OpenAI
from config import Config


class Api:
    def __init__(
            self,
            model='gpt-4-turbo',
            api='OpenAI',
            output_console=False
    ):
        self.model = model
        if model in Config.Small_LLM:
            api = model
        self.url = Config.ApiData[api]['url']
        self.key = Config.ApiData[api]['key']
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
        return self.run_with_client(message)

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
    model_client_1 = 'gpt-4o'
    model_client_2 = 'glm-4'
    # Test run_with_client
    # client_response_1 = Api(model_client_1).run_with_client(message)
    # print('\n{} client output: {}\n'.format(model_client_1, client_response_1))
    # client_response_2 = Api(model_client_2).run_with_client(message)
    # print('\n{} client output: {}\n'.format(model_client_2, client_response_2))
    print(Api(model='Qwen2-7B-Instruct',api='Qwen2').run_with_client(message))
    # print(Api(model='glm-4-9b-chat',api='glm4').run_with_client(message))
    # print(Api(model='Yi-1.5-9B-Chat',api='Yi1.5').run_with_client(message))
