from langchain_core.tools import tool
from typing import Annotated
import re
import requests
from lxml.html import etree
from duckduckgo_search import DDGS

@tool
def web_search(
    keywords: Annotated[str, "要搜索的关键词，根据你当前的任务目标确定，尽量精确和详细"],
    max_results: Annotated[int, ("最多返回多少条搜索结果. 如果返回的搜索结果没有太多有用信息，可以指定返回更多搜索结果")] = 10
) -> list:
    """网络搜索工具。在搜索引擎上搜索关键词，返回指定数目的搜索结果，每个结果包含网页的标题、链接和开头内容。"""
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(
            keywords=keywords,
            region='cn-zh',
            max_results=max_results)]
        return results



# test the tool
if __name__ == "__main__":
    print(web_search.args_schema.model_json_schema())
    a=web_search.invoke({"keywords": "长沙 景点"})
    print(a)