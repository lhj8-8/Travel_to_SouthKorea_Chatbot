from common import client, model, makeup_response
import json
import requests
from pprint import pprint
from tavily import TavilyClient
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# 국내 지역 위도, 경도
global_lat_lon = {
    '서울': [37.57, 126.98], '강원도': [37.86, 128.31], '경기도': [37.44, 127.55],
    '경상남도': [35.44, 128.24], '경상북도': [36.63, 128.96], '광주': [35.16, 126.85],
    '대구': [35.87, 128.60], '대전': [36.35, 127.38], '부산': [35.18, 129.08],
    '세종시': [36.48, 127.29], '울산': [35.54, 129.31], '전라남도': [34.90, 126.96],
    '전라북도': [35.69, 127.24], '제주도': [33.43, 126.58], '충청남도': [36.62, 126.85],
    '충청북도': [36.79, 127.66], '인천': [37.46, 126.71]
}

# 지역별 대표 음식
regional_foods = {
    "서울": ["평양냉면", "불고기", "갈비"],
    "강원도": ["감자옹심이", "막국수", "황태구이"],
    "경기도": ["왕갈비", "국수", "부천 족발"],
    "경상남도": ["아구찜", "밀면", "멸치국수"],
    "경상북도": ["안동찜닭", "문어숙회", "대게"],
    "광주": ["상추튀김", "홍어회", "떡갈비"],
    "대구": ["막창", "대구 따로국밥", "납작만두"],
    "대전": ["성심당 빵", "칼국수", "두부두루치기"],
    "부산": ["돼지국밥", "밀면", "어묵"],
    "세종시": ["약초백숙", "두부요리"],
    "울산": ["언양불고기", "고래고기"],
    "전라남도": ["꼬막정식", "전어회", "광양불고기"],
    "전라북도": ["비빔밥", "모주", "오징어불고기"],
    "제주도": ["흑돼지", "고기국수", "갈치조림"],
    "충청남도": ["꽃게장", "게국지", "홍성 한우"],
    "충청북도": ["올갱이해장국", "충주 사과요리"],
    "인천": ["짜장면", "닭강정", "해산물"]
}

# 지역별 관광명소
regional_spots = {
    "서울": ["경복궁", "남산타워", "명동"],
    "강원도": ["설악산", "경포해변", "대관령"],
    "경기도": ["에버랜드", "물의정원", "수원 화성"],
    "경상남도": ["동피랑", "해금강", "진해 군항제"],
    "경상북도": ["불국사", "하회마을", "호미곶"],
    "광주": ["국립아시아문화전당", "무등산", "양림동"],
    "대구": ["팔공산", "동성로", "수성못"],
    "대전": ["엑스포과학공원", "한밭수목원", "유성온천"],
    "부산": ["해운대", "광안리", "태종대"],
    "세종시": ["세종호수공원", "국립세종수목원"],
    "울산": ["대왕암공원", "간절곶", "태화강 국가정원"],
    "전라남도": ["여수 밤바다", "순천만", "죽녹원"],
    "전라북도": ["전주 한옥마을", "내소사", "덕유산"],
    "제주도": ["성산일출봉", "한라산", "협재해수욕장"],
    "충청남도": ["태안 해안국립공원", "공산성", "대천해수욕장"],
    "충청북도": ["청남대", "월악산", "충주호"],
    "인천": ["송도 센트럴파크", "차이나타운", "월미도"]
}

# 온도 조회 API
def get_celsius_temperature(**kwargs):
    location = kwargs['location']
    lat_lon = global_lat_lon.get(location)
    if not lat_lon:
        return "지역 정보가 없습니다."

    lat, lon = lat_lon
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    temperature = data['current_weather']['temperature']
    return temperature

# 인터넷 검색
def search_internet(**kwargs):
    query = kwargs['search_query']
    answer = tavily.search(query=query, include_answer=True)['answer']
    return answer

# 지역 음식 조회
def get_local_foods(**kwargs):
    region = kwargs["region"]
    foods = regional_foods.get(region, ["해당 지역 음식 정보 없음"])
    return foods

# 관광명소 조회
def get_tourist_spots(**kwargs):
    region = kwargs["region"]
    spots = regional_spots.get(region, ["해당 지역 관광지 정보 없음"])
    return spots

# Function Calling Tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_celsius_temperature",
            "description": "지정된 위치의 현재 섭씨 기온 조회",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "지역명 예: 서울, 부산"}
                },
                "required": ["location"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "search_internet",
            "description": "인터넷 검색 필요 시 사용",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_query": {"type": "string", "description": "검색어"}
                },
                "required": ["search_query"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_local_foods",
            "description": "해당 지역의 유명 음식 목록",
            "parameters": {
                "type": "object",
                "properties": {
                    "region": {"type": "string", "description": "서울, 부산, 제주도 등"}
                },
                "required": ["region"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_tourist_spots",
            "description": "해당 지역의 대표 관광지 목록",
            "parameters": {
                "type": "object",
                "properties": {
                    "region": {"type": "string", "description": "광역시도 또는 지역명"}
                },
                "required": ["region"],
            },
        },
    }
]

# FunctionCalling Class
class FunctionCalling:

    def __init__(self, model):
        self.available_functions = {
            "get_celsius_temperature": get_celsius_temperature,
            "search_internet": search_internet,
            "get_local_foods": get_local_foods,
            "get_tourist_spots": get_tourist_spots
        }
        self.model = model

    def analyze(self, user_message, tools):
        try:
            response = client.chat.completions.create(
                model=model.basic,
                messages=[{"role": "user", "content": user_message}],
                tools=tools,
                tool_choice="auto"
            )
            message = response.choices[0].message
            message_dict = message.model_dump()
            pprint(("message_dict=>", message_dict))
            return message, message_dict
        except Exception as e:
            print("Error occurred(analyze):", e)
            return makeup_response("[analyze 오류입니다]")

    def run(self, analyzed, analyzed_dict, context):
        context.append(analyzed)
        tool_calls = analyzed_dict["tool_calls"]

        for tool_call in tool_calls:
            function = tool_call["function"]
            func_name = function["name"]
            func_to_call = self.available_functions[func_name]

            try:
                func_args = json.loads(function["arguments"])
                func_response = func_to_call(**func_args)

                context.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": func_name,
                    "content": str(func_response)
                })

            except Exception as e:
                print("Error occurred(run):", e)
                return makeup_response("[run 오류입니다]")

        return client.chat.completions.create(model=self.model, messages=context).model_dump()