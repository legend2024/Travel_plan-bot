import os
from langchain_core.tools import tool
from typing import Annotated, List, Dict
import requests
from dotenv import load_dotenv, find_dotenv

@tool
def get_location_coordinate(
        location: Annotated[str, "要获取经纬度的地点名称"],
        city: Annotated[str, "要获取经纬度的地点所在的城市名称，必须是地级市，不能是县级市或村镇。如果能确定的话填写，不能确定可以不填"] = ""
) -> List[Dict[str, str]]:
    """位置获取工具。根据地点名称和城市名称获取该地点的经纬度。由于可能存在同名地点，所以返回的是一个包含所有同名地点详细地址和经纬度的列表"""

    _ = load_dotenv(find_dotenv())
    amap_key = os.getenv("AMAP_API_KEY")
    base_url = "https://restapi.amap.com/v3/geocode/geo?"
    url = f"{base_url}key={amap_key}&address={location}&city={city}"
    r = requests.get(url)
    result = r.json()
    print('result：', result)

    if result['status'] == '0':
        error_msg = f"获取以下地点坐标失败：{location}。错误信息: {result['info']}。请检查参数格式是否符合规范（经度在前、纬度在后），地点和城市名称是否正确，或者考虑该名称是否是俗称，能否推断出其正式名称。"
        return error_msg
    location_coordinates = []
    for item in result['geocodes']:
        location_coordinates.append({
            "address": item['formatted_address'],
            "coordinate": item['location'],
            "citycode": item['citycode']
        })
    return location_coordinates


# test the tool
if __name__ == "__main__":
    print(get_location_coordinate.args_schema.model_json_schema())
    a = get_location_coordinate.invoke({"location": "岳阳楼", "city": "岳阳"})
    print(a)

