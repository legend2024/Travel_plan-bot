from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class PublicState(TypedDict):
    messages: Annotated[list, add_messages]


"""
TypedDict:
    来自typing模块，用于定义具有特定字段和类型的字典。
    它允许你明确指定字典中每个字段的名称和类型，类似于定义一个类，但更轻量级。
Annotated:
    来自typing模块，用于为字段添加额外的元数据（注解）。
    它允许你在类型注解的基础上附加其他信息，这些信息可以被工具或框架使用。
add_messages:
    来自langgraph.graph.message模块，是一个函数或工具，用于处理消息列表。

PublicState类
PublicState是一个类型化字典（TypedDict），用于表示一个包含消息列表的状态对象。
字段：
    messages:
        类型为list，表示一个消息列表。
        使用 Annotated对messages字段进行了注解，附加了add_messages函数。
        这意味着messages字段不仅是一个普通的列表，还带有额外的元数据或行为(由add_messages提供)。
        例如，add_messages可能用于在向messages 列表中添加消息时执行某些操作（如验证、格式化或记录）。
"""
