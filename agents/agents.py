from states.state import PublicState
from langchain_core.tools import StructuredTool
from models.factory import LLMFactory
from langchain_core.messages import HumanMessage, ToolMessage
from utils.helper import get_current_local_datetime

class Agent:
    def __init__(self, model_name: str, temperature: float, prompt_template: str, tools: list[StructuredTool]):
        """在图初始化中创建代理时才初始化LLM,因此，我们不需要在每次调用代理时创建它"""
        self.llm = LLMFactory.get_llm(model=model_name, temperature=temperature)
        if tools:
            self.llm = self.llm.bind_tools(tools)
        self.prompt_template = prompt_template



## 异步调用语言模型
class AsyncAgent(Agent):
    async def __call__(self, state: PublicState):
        """first_prompt等于系统提示+第一条用户消息"""
        first_prompt = HumanMessage(self.prompt_template.format(
            current_time=get_current_local_datetime(),
            first_user_message=state['messages'][0].content
        ))
        prompt = [first_prompt] + state['messages'][1:]
        response = await self.llm.ainvoke(prompt)
        return {'messages': [response]}


## 同步调用语言模型
class SyncAgent(Agent):
    def __call__(self, state: PublicState):
        first_prompt = HumanMessage(self.prompt_template.format(
            current_time=get_current_local_datetime(),
            first_user_message=state['messages'][0].content
        ))
        prompt = [first_prompt] + state['messages'][1:]
        response = self.llm.invoke(prompt)
        return {'messages': [response]}

"""
1. Agent类
Agent 类是一个基类，用于初始化语言模型（LLM）和相关的工具。
__init__ 方法:
    model_name: 指定要使用的语言模型的名称。
    temperature: 控制生成文本的随机性，值越高生成的文本越随机。
    prompt_template: 提示模板，用于生成系统提示和用户消息的组合。
    tools: 一个包含 StructuredTool 对象的列表，这些工具可以绑定到语言模型上。
在初始化时，Agent类通过LLMFactory.get_llm方法获取指定的语言模型，
并将其绑定到提供的工具上（如果有的话）。prompt_template 也被存储在实例变量中，供后续使用。

2. AsyncAgent类
AsyncAgent 类继承自 Agent，并实现了异步调用语言模型的功能。
__call__ 方法:
state: 一个 PublicState 对象，包含了当前的状态信息，通常包括用户的消息列表。
该方法首先构造一个first_prompt，它是系统提示和第一个用户消息的组合。由于某些语言模型（如 Gemini）不支持系统提示，因此通过这种方式来绕过限制。
first_prompt 是通过格式化 prompt_template 生成的，其中包含了当前时间和第一个用户消息。
然后,prompt列表被构造first_prompt加上剩余的用户消息。最后，使用self.llm.ainvoke方法异步调用语言模型，并返回包含模型响应的字典。


3. SyncAgent类
SyncAgent类也继承自Agent，但实现了同步调用语言模型的功能。
__call__ 方法:
state: 一个PublicState对象，包含了当前的状态信息，通常包括用户的消息列表。
与AsyncAgent类似，SyncAgent 也构造了一个first_prompt，并将其与剩余的用户消息组合成 prompt列表。
然后，使用 self.llm.invoke 方法同步调用语言模型，并返回包含模型响应的字典。


4. 其他依赖
PublicState: 一个状态类，用于存储和管理当前的状态信息。
LLMFactory: 一个工厂类，用于根据模型名称和温度参数获取相应的语言模型。
StructuredTool: 一个工具类，用于定义可以与语言模型绑定的工具。
HumanMessage和ToolMessage: 用于构造和传递消息的类。
get_current_local_datetime: 一个辅助函数，用于获取当前的本地时间。
"""