from langchain_openai import ChatOpenAI

class LLMFactory:
    @staticmethod
    def get_llm(model=None, temperature=None):
        if model is None or temperature is None:
            raise ValueError("Both 'model' and 'temperature' must be specified.")

        if model.startswith('gpt'):
            return ChatOpenAI(model=model, temperature = temperature, streaming=True)

        # elif model.startswith('text-davinci'):
        #     return

        raise ValueError(f"Model {model} is not supported.")

"""
1. LLMFactory类
LLMFactory 是一个工厂类，用于根据传入的参数创建和返回相应的语言模型实例。

2. get_llm 静态方法
get_llm 是一个静态方法，用于根据传入的 model和temperature参数创建并返回相应的语言模型实例。
参数：
model: 字符串类型，指定要使用的语言模型的名称（例如 "gpt-3.5-turbo"）。
temperature: 浮点数类型，控制生成文本的随机性。值越高，生成的文本越随机；值越低，生成的文本越确定。

代码逻辑：
    参数检查:
    如果model或temperature为None，则抛出ValueError异常，提示必须指定这两个参数。
    模型匹配:
    如果model以"gpt"开头(例如"gpt-3.5-turbo"或 "gpt-4")，则使用ChatOpenAI类创建一个OpenAI的聊天模型实例。
    ChatOpenAI是langchain_openai模块中的一个类，用于与OpenAI的聊天模型进行交互。
    创建实例时，传入的参数包括：
        model: 模型名称。
        temperature: 控制生成文本的随机性。
        streaming=True: 启用流式输出（即逐块生成响应，而不是一次性生成完整响应）。
    不支持的模型:
    如果传入的model不是以"gpt"开头，则抛出ValueError异常，提示该模型不受支持。
"""
