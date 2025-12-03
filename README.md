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
- **Chatbot.py**: 
- **common.py**:
- **parallel_function_calling.py**:
- **warning_agent.py**:

<br>

## 🔎 파일별 코드 및 기능 살펴보기

1. [ application.py  ](#-application.py)
2. [characters.py](#-characters.py)
3. [Chatbot.py](#-Chatbot.py)
4. [common.py](#-common.py)
5. [parallel_function_calling.py](#-parallel-function-calling.py)
6. [warning_agent.py](#-warning-agent.py)

<br>
   
## 1. application.py
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
설명들


<br>   

## 4. common.py
설명들


<br>   

## 5. parallel_function_calling.py
설명들


<br>   

## 6. warning_agent.py
설명들


<br>   

## Text Style1

