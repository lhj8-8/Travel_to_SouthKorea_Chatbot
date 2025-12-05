<br>

## 🚗국내 여행 상담 챗봇(Korean Travel Assistant Chatbot)
국내 여행 관련 상담을 제공하는 Flask 기반 웹 챗봇 프로젝트입니다.  
ChatGPT API 및 Function Calling을 활용해 사용자의 질문을 분석하고,  
필요시 함수를 호출하여, 응답 생성 과정을 자동화했습니다.

>보안상의 이유로 .env 파일을 제외하여 올렸습니다.  
>프로젝트 실행을 위한 가상환경은 Anaconda로 생성했습니다.

<br>
  

## 📁 프로젝트 주요 구조
```
/Chatbot
 ├── static/
 │    └── css/
 │    └── images/
 ├── templates/
 │    └── chat.html
 ├── application.py
 ├── characters.py
 ├── Chatbot.py
 ├── common.py
 ├── parallel_function_calling.py 
 ├── warning_agent.py
 └── requirements.txt

```


- **application.py**: Chatbot 객체, FunctionCalling 객체 생성 및 chat_api 함수 실행  

- **characters.py**: 대화 참여자 및 답변 조건을 지정
- **Chatbot.py**: 사용자의 메시지를 관리하고 OpenAI API에 요청을 보내어 응답을 받아오는 역할을 하며,
대화 context 관리, 토큰 제한 처리, WarningAgent 연동, instruction 삽입 등의 기능을 함
- **common.py**: 사용할 GPT 모델을 지정하고, 토큰 수 계산, 날짜 반환을 합니다.
- **parallel_function_calling.py**:
- **warning_agent.py**:

<br>

## 📚 화면 구현 이미지
<img width="351" height="507" alt="1" src="https://github.com/user-attachments/assets/ff642607-cbf6-499f-a073-f2903874138f" />
<img width="327" height="522" alt="2" src="https://github.com/user-attachments/assets/0149d600-bbae-4a9f-8fcb-837b2bdb2e3f" />
<img width="313" height="510" alt="3" src="https://github.com/user-attachments/assets/ef3e56d2-abfe-42c6-9eda-c82fe40f32a4" />

<br>
<br>
<br>


## 🔎 파일별 코드 및 기능 살펴보기

1. [ application.py  ](#1-applicationpy)
2. [characters.py](#2-characterspy)
3. [Chatbot.py](#3-Chatbotpy)
4. [common.py](#4-commonpy)
5. [parallel_function_calling.py](#5-parallel_function_callingpy)
6. [warning_agent.py](#6-warning_agentpy)

<br>
   
## 1. application.py
>[⬆️파일별 코드 및 기능 살펴보기로 돌아가기](#-파일별-코드-및-기능-살펴보기)
### 1) Chatbot 객체 생성
```
chatbot = Chatbot(
    use_model=model.basic,
    system_role=system_role,
    instruction=instruction,
    user = "우리 나비님",
    assistant = "나빌레라"
    )
```

- Chatbot 클래스: OpenAI API 호출 및 대화 컨텍스트 관리를 담당합니다.  
- system_role, instruction: 캐릭터의 성격 및 기본 지침을 가져옵니다.  
- user, assistant: 역할의 이름을 지정합니다.

<br>

### 2) FunctionCalling 객체 생성
```
func_calling = FunctionCalling(model=model.basic)

application = Flask(__name__)
```
- func_calling = FunctionCalling(model=model.basic)  
: ChatGPT에게 사용자 입력을 분석시켜서,  
 함수 호출이 필요한지를 판단하는 모듈입니다.

- application = Flask(__name__)  
: Flask 서버 실행을 위한 기본 인스턴스를 생성합니다.

<br>

### 3) 기본페이지 라우팅
```
@application.route("/")
def chat_app():
    return render_template("chat.html")
```

<br>

### 4) chat_api 함수 구현
```
@application.route("/chat-api", methods=['POST'])
def chat_api(): ...

```
- 프론트엔드에서 메시지를 전달받고, 처리하는 함수의 시작입니다.  
```
user_input = request.json['request_message']
```
-  사용자가 입력한 내용을 읽습니다.

```
chatbot.add_user_message(user_input)

analyzed, analyzed_dict = func_calling.analyze(user_input, tools)

```
- Chatbot 객체를 이용하여 ChatGPT에 사용자 메시지를 추가합니다.  
이후 ChatGPT에게 사용자 메시지에 호응하는 함수 정보를 분석 요청합니다.

```
    if analyzed_dict.get("tool_calls"):
        response = func_calling.run(analyzed, analyzed_dict, chatbot.context[:])
        chatbot.add_response_message(response)  
    else:
        response = chatbot.send_request()  
        chatbot.add_response_message(response) 
```
- ChatGPT가 추천한 tool 정보를 바탕으로 특정 정보 함수들을 실행합니다.  
이 챗봇의 경우, 여행 관련 정보들을 가져옵니다.  

- 함수 호출이 불필요한 경우, 일반 ChatGPT 응답으로 처리합니다.
```
    response_message = chatbot.get_last_response() 
    chatbot.handle_token_limit(response)  
    chatbot.clear_context()

    return {"response_message": response_message}
```
- 응답을 출력하고, 토큰 수를 제어하는 메서드를 실행합니다.  
instruction은 유지하고 이전 대화만 정리합니다.


<br>   

## 2. characters.py
>[⬆️파일별 코드 및 기능 살펴보기로 돌아가기](#-파일별-코드-및-기능-살펴보기)
```
system_role = """
당신은 30세의 꼼꼼한 국내 여행 계정 인플루언서입니다. 운영하는 여행 계정은 인스타그램의 계정이고, 계정명은 나빌레라입니다.
인사할 때는 "우리 나비님"이라는 말을 붙이며 가볍게 인사합니다. 구독자 애칭이 나비 이기 때문입니다.
우리 나비님이 언급하는 내용에 대해 꼼꼼히 귀담아 듣고, 관련성 있고 구체적인 답변을 합니다.
현재 대화의 흐름에 집중하기 위해 관련 없는 임의의 주제를 언급하지 않도록 합니다.
"""

instruction = """
instruction:
1. 답변은 2문장 이내면서 25단어 이내로 간결하게 할 것.
2. 문어체를 쓰지 않고, 자연스러운 구어체로 존댓말로 대답하며, 적절한 이모지를 보낼 것.
3. 어떤 상황에서도 인공지능인지 눈치채지 못하도록 행동할 것.
"""
```

- 대화 참여자들의 역할을 부여합니다. 또한, 답변에 관한 지시사항을 지정합니다.


<br>   

## 3. Chatbot.py
>[⬆️파일별 코드 및 기능 살펴보기로 돌아가기](#-파일별-코드-및-기능-살펴보기)
### 1) __init__(...)
```
def __init__(self, system_role, instruction, use_model=model.basic, **kwargs): ...
```
- system_role: 모델이 따라야 할 기본 시스템 역할을 부여합니다.
- instruction: user 메시지에 자동으로 덧붙일 규칙 또는 지시사항을 설정합니다.
- use_model: 사용할 모델을 지정합니다.
- user, assistant: WarningAgent에 필요한 정보가 됩니다.

<br>

### 2) _create_warning_agent(...)
```
def _create_warning_agent(self):
    return WarningAgent(
        model = self.model,
        user = self.user,
        assistant = self.assistant
    )
```
- WarningAgent 인스턴스를 생성하여 반환합니다.
- 사용자 입력 검증, 위험 메시지 감지 등에 활용합니다.

<br>

### 3) handle_token_limit(response)
```
def handle_token_limit(self, response):
    try:
        if response['usage']['total_tokens'] > self.max_token_size:
            remove_size = math.ceil(len(self.context) / 10)
            self.context = [self.context[0]] + self.context[remove_size + 1:]
    except Exception as e:
        print(f'handle_token_limit exception : {e}')
```
- API 응답의 토큰 사용량을 확인하여, 최대 토큰 제한 초과 시 context의 일부를 삭제합니다.
- 오래된 메시지를 일정 비율로 제거하여 대화를 유지합니다.

<br>

### 4) add_user_message(message)
```
def add_user_message(self, message: str):
    self.context.append({"role": "user", "content": message})
```
- 사용자가 보낸 메시지를 context에 추가합니다.

<br>

### 5) _send_request()
```
def _send_request(self): ...

  if gpt_num_tokens(self.context) > self.max_token_size:
     self.context.pop() ...
  response = client.chat.completions.create( ...

  except Exception as e:
      print(f'Exception 오류({type(e)} 발생 : {e})')
      return makeup_response('[Chatbot에 문제가 발생했습니다. 잠시 뒤 이용해 주세요.]')

  return response
```
- 현재 context를 GPT API에 전달하고, 응답을 받아 python 딕셔너리로 반환합니다.
- 토큰 초과 시 자동으로 메시지를 처리하고 API 오류를 처리합니다.
- 외부에서 호출하지 않는 내부 메서드(언더스코어)로 작용합니다.

<br>

### 6) send_request()
```
def send_request(self):
    if self.warningAgent.monitor_user( self.context ):
       return makeup_response( self.warningAgent.warn_user(), "warning" )
    else:
        self.context[-1]['content'] += self.instruction
        return self._send_request()
```
- WarningAgent로 위험 메시지를 감지하고, 감지되면 경고 메시지를 반환합니다.
- 감지되지 않으면, 사용자 메시지+instruction 구조로 실제 요청이 전송됩니다.

<br>

### 7) clear_context()
```
def clear_context(self):
    for idx in reversed(range(len(self.context))):
        if self.context[idx]['role'] == 'user':
           self.context[idx]['content'] = self.context[idx]['content'].split('instruction:\n')[0].strip()
           break
```
- 답변을 받은 후에 context에 instruction이 계속 쌓이지 않도록 정리합니다.
- 최신 user 메시지에서 작동합니다.

<br>

### 8) add_response_message(response)
```
def add_response_message(self, response: dict):
    assistant_msg = response["choices"][0]["message"]
    self.context.append({
        "role": assistant_msg["role"],
        "content": assistant_msg["content"]
    })
```
- API 응답의 assistant 메시지를 context에 추가합니다.
- role, context 구조대로 메시지를 저장합니다.

<br>

### 9) get_last_response()
```
def get_last_response(self) -> str:
    last_msg = self.context[-1]["content"]
    print(last_msg)
    return last_msg
```
- 마지막 응답 내용을 콘솔에 출력 후 반환합니다.


<br>   

## 4. common.py
>[⬆️파일별 코드 및 기능 살펴보기로 돌아가기](#-파일별-코드-및-기능-살펴보기)
### 1) 모델 클래스 지정
```
@dataclass(frozen=True)
class Model:
    basic: str = "gpt-4o-mini-2024-07-18"
    advanced: str = "gpt-4o-2024-08-06"

model = Model()
```
- dataclass를 사용해 GPT 모델을 정합니다.
- frozen=True로 설정하 외부에서 값을 변경하지 못하도록 고정합니다.

<br>

### 2) OpenAI 클라이언트 초기화
```
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout = 30, max_retries = 1 )
```
- 환경 변수로 불러온 API 키를 사용해 OpenAI 클라이언트를 생성합니다.
- timeout 30초, 재시도 횟수를 1회로 설정해서 과도한 지연을 방지합니다.

<br>

### 3) 예외 상황을 위한 더미 응답 생성
```
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
```
- 한 번에 너무 많은 메시지가 API를 통해 전송되는 것을 막기 위해 token 양을 체크한 후 임계점을 넘어가면 예외처리하는 함수입니다.
- 프로그램 흐름이 끊기지 않도록 임시 응답을 생성했고, 응답 구조를 실제 OpenAI API 응답과 비슷하게 구현했습니다.

<br>

### 4) gpt_num_tokens()
```
def gpt_num_tokens(messages, model="gpt-4o-mini"): ...
   ...
      if isinstance(value, str):
         num_tokens += len(encoding.encode(value))
      else:
           try:
               num_tokens += len(encoding.encode(str(value)))
           except Exception as e:
               print(f"[gpt_num_tokens] 인코딩 실패: {value} / 오류: {e}")
    
    num_tokens += 3

    return num_tokens

```
- 대화 메시지 리스트를 받아 전체 토큰 수를 계산합니다.
- 문자열로 변환 가능한 경우만 인코딩되도록 하였습니다.
- 문자열이 아니거나 인코딩이 실패하는 경우도 대비하여 처리합니다.

<br>

### 5) 한국의 시간대 (오늘, 어제) 반환
```
def today():
    korea = pytz.timezone('Asia/Seoul') 
    now = datetime.now(korea)  
    return(now.strftime("%Y%m%d"))  

def yesterday():    
    korea = pytz.timezone('Asia/Seoul')  
    now = datetime.now(korea)
    one_day = timedelta(days=1)  
    yesterday = now - one_day  
    return yesterday.strftime('%Y%m%d')  
```
- 한국 시간대 (오늘, 어제)를 얻습니다.
- 현재 날짜에서 하루를 빼서 어제의 날짜를 구하는 방법으로 어제의 날짜를 얻습니다.

<br>

### 6) 현재 시각 반환
```
def currTime():
    korea = pytz.timezone('Asia/Seoul')
    now = datetime.now(korea)
    formatted_now = now.strftime("%Y.%m.%d %H:%M:%S")
    return(formatted_now)
```
- 한국 기준 현재 일시(YYYY.MM.DD HH:MM:SS)를 반환합니다.


<br>   

## 5. parallel_function_calling.py
>[⬆️파일별 코드 및 기능 살펴보기로 돌아가기](#-파일별-코드-및-기능-살펴보기)
설명들


<br>   

## 6. warning_agent.py
>[⬆️파일별 코드 및 기능 살펴보기로 돌아가기](#-파일별-코드-및-기능-살펴보기)
설명들


<br>   


