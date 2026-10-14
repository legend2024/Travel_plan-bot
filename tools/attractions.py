import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from langchain_core.tools import tool
from typing import Annotated
from dotenv import load_dotenv, find_dotenv

def InitWebDriver():
    # 设置日志等级
    LOGGER.setLevel(logging.WARNING)
    # 使用chrome开发者模式
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 禁用启用Blink运行时的功能
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Selenium执行cdp命令  再次覆盖window.navigator.webdriver的值
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        })
                      """
    })
    return driver

def fetch_page_with_selenium(driver, url):
    driver.get(url)
    # 等待页面完全加载
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2)
    page_content = driver.page_source
    return page_content

def get_destination_overview(soup):
    overview_element = soup.find('span', {'id': 'mdd_poi_desc'})
    if overview_element:
        return overview_element.text.strip()
    else:
        return "Overview not found."

def get_scenic_spots(driver, soup):
    spots = []
    # 获取景点列表
    spot_elements = soup.find_all('ul', class_='scenic-list clearfix')
    for spot in spot_elements[:1]:  # 只取第一页
        for item in spot.find_all('li'):
            spot_name = item.find('h3').text.strip()
            spot_url = item.find('a')['href']
            spot_details = get_scenic_spot_details(driver, "https://www.mafengwo.cn" + spot_url, spot_name)
            spots.append(spot_details)
    return spots

def get_scenic_spot_details(driver, url, spot_name):
    page_content = fetch_page_with_selenium(driver, url)
    soup = BeautifulSoup(page_content, 'html.parser')
    
    summary = soup.find('div', class_='summary').text.strip() if soup.find('div', class_='summary') else "No summary available."
    duration = soup.find('li', class_='item-time').find('div', class_='content').text.strip() if soup.find('li', class_='item-time') else "No duration info."

    open_time = "No open time info."
    for dt in soup.find_all('dt'):
        if "开放时间" in dt.text:
            open_time = dt.find_next('dd').text.strip()
            break

    return {
        'name': spot_name,
        'summary': summary,
        'duration': duration,
        'open_time': open_time
    }


@tool
def get_attractions_information(
    destination: Annotated[str, "目的地名称，必须是一个明确的城市或村镇名称"]
) -> dict:
    """景点搜索工具。获取目的地概览和景点信息列表"""
    _ = load_dotenv(find_dotenv())
    driver = InitWebDriver()
    base_search_url = 'https://www.mafengwo.cn/search/q.php'
    search_url = f"{base_search_url}?q={destination}"
    print('search_url：',search_url)
    soup = BeautifulSoup(fetch_page_with_selenium(driver, search_url), 'html.parser')
    more_link = soup.find('a', text='查看更多相关旅行地>>')['href']
    print(more_link)

    # 提取 mddid 并拼接目标链接
    mddid = more_link.split('mddid=')[1].split('&')[0]
    destination_url = f'https://www.mafengwo.cn/jd/{mddid}/gonglve.html'

    destination_page = fetch_page_with_selenium(driver, destination_url)
    soup = BeautifulSoup(destination_page, 'html.parser')

    overview = get_destination_overview(soup)
    print('overview:',overview)
    scenic_spots = get_scenic_spots(driver, soup)
    print('scenic_spots:',scenic_spots)

    result = {
        'overview': overview,
        'scenic_list': scenic_spots
    }
    driver.quit()
    return result


# test the tool
if __name__ == '__main__':
    print(get_attractions_information.args_schema.model_json_schema())
    a=get_attractions_information.invoke({"destination": "长沙"})
    print(a)
