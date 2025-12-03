from flask import Flask, render_template, request


from Chatbot import Chatbot
from common import model
from characters import system_role, instruction
from parallel_function_calling import FunctionCalling, tools

# Chatbot 객체 생성
chatbot = Chatbot(
    use_model=model.basic,
    system_role=system_role,
    instruction=instruction,
    user = "우리 나비님",
    assistant = "나빌레라"
    )

#FunctionCalling 객체 생성
func_calling = FunctionCalling(model=model.basic)

application = Flask(__name__)

@application.route("/")
def chat_app():
    return render_template("chat.html")

# chat_api 함수 정의
@application.route("/chat-api", methods=['POST'])
def chat_api():
    # 에코 동작만 추가
    # print(f'request.json : {request.json}')
    # return {"response_message": "나도 " + request.json['request_message']}

    # 사용자 입력 내용
    print(f'request.json : {request.json}')
    user_input = request.json['request_message']

    # Chatbot 객체를 이용하여 ChatGPT에 요청 및 응답 수신
    chatbot.add_user_message(user_input)  # 사용자 메시지 추가

    #ChatGPT 에게 함수 사양을 토대로 사용자 메시지에 호응하는 함수 정보 분석 요청
    analyzed, analyzed_dict = func_calling.analyze(user_input, tools)

    #ChatGPT 가 함수 호출이 필요하다고 분석했는지 여부 체크
    if analyzed_dict.get("tool_calls"):
        # ChatGPT 가 분석해 준 함수 호출
        response = func_calling.run(analyzed, analyzed_dict, chatbot.context[:])
        chatbot.add_response_message(response)  # 응답 메시지 context에 추가
    else:
        response = chatbot.send_request()  # API 요청
        chatbot.add_response_message(response)  # 응답 메시지 context에 추가

    # 응답 결과 출력
    response_message = chatbot.get_last_response()   # 응답 출력
    chatbot.handle_token_limit(response)  # 토큰 수 제어 메서드 실행
    chatbot.clear_context()  # instruction 삭제
    print(f'response_message : {response_message}')

    return {"response_message": response_message}

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080, debug=True)