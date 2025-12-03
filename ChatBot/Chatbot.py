# Chatbot.py
from dis import Instruction
from common import model, client, gpt_num_tokens, makeup_response
import math
from warning_agent import WarningAgent


class Chatbot:
    def __init__(self, system_role, instruction, use_model=model.basic, **kwargs):   #파라미터에도 instruction
        """context 초기화 및 시스템 역할 설정"""
        self.model = use_model
        self.context = [
            {"role": "system", "content": system_role}
        ]
        self.instruction = instruction   # 지시 추가
        self.max_token_size = 16 * 1024  # 최대 토큰 수(보통 2의 배수로 써준다)
        # WarningAgent 파라미터 추가
        self.kwargs = kwargs
        self.user = kwargs["user"]
        self.assistant = kwargs["assistant"]
        self.warningAgent = self._create_warning_agent()
    
    def _create_warning_agent(self):
        return WarningAgent(
            model = self.model,
            user = self.user,
            assistant = self.assistant
        )

    def handle_token_limit(self, response):
        # 누적 token 수가 임계점을 넘지 않도록 제어
        try:
            if response['usage']['total_tokens'] > self.max_token_size:
                remove_size = math.ceil(len(self.context) / 10)
                self.context = [self.context[0]] + self.context[remove_size + 1:]
        except Exception as e:
            print(f'handle_token_limit exception : {e}')

    def add_user_message(self, message: str):
        """사용자 메시지를 context에 추가"""
        self.context.append({"role": "user", "content": message})

    def _send_request(self):  # _ : 내장 메서드(외부에서 접근 불가)
        """현재 context를 API에 전송하고 응답 받기"""
        try:
            # 현재 context의 token 크기가 정해진 최대 크기를 벗어날 때 처리
            if gpt_num_tokens(self.context) > self.max_token_size:
                self.context.pop()
                return makeup_response('메시지를 조금 짧게 보내 줄래?')

            response = client.chat.completions.create(
                model=self.model,
                messages=self.context,
                temperature=0.5,
                top_p=1,
                max_tokens=256,
                frequency_penalty=0,
                presence_penalty=0
            ).model_dump()
        except Exception as e:
            print(f'Exception 오류({type(e)} 발생 : {e})')
            return makeup_response('[Chatbot에 문제가 발생했습니다. 잠시 뒤 이용해 주세요.]')

        return response
    
    #API 요청 전에 context 마지막에 instruction 추가 
    def send_request(self):
        if self.warningAgent.monitor_user( self.context ):
            return makeup_response( self.warningAgent.warn_user(), "warning" )
        else:  # 요청전 context 마지막에 instruction 추가
            self.context[-1]['content'] += self.instruction
            return self._send_request()
 
    #답변 받은 후에 context에 있는 instruction 삭제 함수
    def clear_context(self):
        for idx in reversed(range(len(self.context))):
            if self.context[idx]['role'] == 'user':
               self.context[idx]['content'] = self.context[idx]['content'].split('instruction:\n')[0].strip()
               break

    def add_response_message(self, response: dict):
        """응답 메시지를 context에 추가"""
        assistant_msg = response["choices"][0]["message"]
        self.context.append({
            "role": assistant_msg["role"],
            "content": assistant_msg["content"]
        })

    def get_last_response(self) -> str:
        """마지막 응답 내용을 콘솔에 출력 후 반환"""
        last_msg = self.context[-1]["content"]
        print(last_msg)
        return last_msg