# Reference: https://langchain-ai.github.io/langgraph/tutorials/introduction/#part-2-enhancing-the-chatbot-with-tools
from langgraph.graph import StateGraph, START
from states.state import PublicState
from langgraph.prebuilt import ToolNode, tools_condition
from prompts.main import agent_prompt_template
from tools import *

def create_graph(model_name, is_async=True):
    graph = StateGraph(PublicState)
    tools = [web_search,
             get_location_coordinate,
             get_attractions_information,
             route_planning,
             search_nearby_poi,
             save_info_and_clear_history,
            ]

    if is_async:
        from agents.agents import AsyncAgent as MainAgent

    travel_agent = MainAgent(
        model_name=model_name,
        temperature=0,
        prompt_template=agent_prompt_template,
        tools=tools)
    # Pass the "__call__" function in the ChatterAgent class to add_node. This function will be called when the node is invoked.
    # The function should be able to use extractor's 'llm' and 'prompt_template' attributes as they have been initialized when created
    # the extractor instance.
    graph.add_node("agent", travel_agent)

    tool_node = ToolNode(tools)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)  # Will either direct to a specific tool in tools or to the END node
    graph.add_edge("tools", "agent")
    return graph

def init_app(model_name, is_async=True):
    graph = create_graph(model_name, is_async)
    from langgraph.checkpoint.memory import InMemorySaver
    memory = InMemorySaver()
    print('memory:',memory,dir(memory))
    app = graph.compile(checkpointer=memory)
    return app



"""
代码结构说明：
1. 状态图工作流：
   Agent -> 条件判断 -> 工具执行（如需要）-> 返回Agent -> ... 循环直至结束

2. 关键节点：
   - agent: 负责决策和生成响应
   - tools: 负责执行具体工具操作

3. 状态管理：
   - 使用PublicState在各节点间传递状态
   - 通过InMemorySaver实现状态持久化

注意事项：
1. 路径依赖：
   - 需要确保agents.agents、states.state等模块路径正确
   - 工具函数需要正确定义在tools模块中

2. 异步模式：
   - 当is_async=True时需要使用支持异步执行的LLM
   - 需要整个运行时环境支持异步操作

3. 工具调用：
   - 工具函数需要符合langgraph的ToolNode调用规范
   - 每个工具应有明确的输入输出类型定义

4. 提示工程：
   - agent_prompt_template需要合理设计以引导代理正确使用工具
   - 建议在提示词中包含工具使用说明和格式要求
   
"""

