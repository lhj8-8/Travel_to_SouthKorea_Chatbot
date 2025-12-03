# common.py
import os
from dotenv import load_dotenv
from dataclasses import dataclass
import tiktoken
import pytz
from datetime import datetime, timedelta

from openai import OpenAI

# 환경 변수 로드
load_dotenv()

# 자동으로 초기화 속성으로 사용, 외부 수정 방지
@dataclass(frozen=True)
class Model:
    basic: str = "gpt-4o-mini-2024-07-18"
    advanced: str = "gpt-4o-2024-08-06"

model = Model()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout = 30, max_retries = 1 )

# 한 번에 너무 많은 메시지가 API를 통해 전송되는 것을 막기 위해
# token 양을 체크한 후 임계점을 넘어가면 예외처리
# try~except 외에 임의의 OpenAI API 응답 결과를 만들어서 프로그램 전체가 
# 자연스럽게 흘러가도록 한다.
def makeup_response( message, finish_reason = "ERROR" ):
    return {
        "choices": [
            {
                "finish_reason": finish_reason,
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": message
                }
            }
        ],
        "usage": { "total_tokens": 0 },
    }

# 토큰수 산출 함수
def gpt_num_tokens(messages, model="gpt-4o-mini"):
    encoding = tiktoken.encoding_for_model(model)  # 문자열을 token으로 바꾸는 encoder
    tokens_per_message = 3
    num_tokens = 0

    for message in messages:
        num_tokens += tokens_per_message
        for _, value in message.items():
            # 문자열로 변환 가능한 경우만 인코딩
            if isinstance(value, str):
                num_tokens += len(encoding.encode(value))
            else:
                # value가 None이나 dict인 경우 문자열로 바꿔 encode (안전하게)
                try:
                    num_tokens += len(encoding.encode(str(value)))
                except Exception as e:
                    print(f"[gpt_num_tokens] 인코딩 실패: {value} / 오류: {e}")
    
    num_tokens += 3

    return num_tokens

def today():
    korea = pytz.timezone('Asia/Seoul')  # 한국 시간대를 얻습니다.
    now = datetime.now(korea)  # 현재 시각을 얻습니다.
    return(now.strftime("%Y%m%d"))  # 시각을 원하는 형식의 문자열로 변환합니다.

def yesterday():    
    korea = pytz.timezone('Asia/Seoul')  # 한국 시간대를 얻습니다.
    now = datetime.now(korea)  # 현재 시각을 얻습니다.
    one_day = timedelta(days=1)  # 하루 (1일)를 나타내는 timedelta 객체를 생성합니다.
    yesterday = now - one_day  # 현재 날짜에서 하루를 빼서 어제의 날짜를 구합니다.
    return yesterday.strftime('%Y%m%d')  # 어제의 날짜를 yyyymmdd 형식으로 변환합니다.

def currTime():
    # 한국 시간대를 얻습니다.
    korea = pytz.timezone('Asia/Seoul')
    # 현재 시각을 얻습니다.
    now = datetime.now(korea)
    # 시각을 원하는 형식의 문자열로 변환합니다.
    formatted_now = now.strftime("%Y.%m.%d %H:%M:%S")
    return(formatted_now)