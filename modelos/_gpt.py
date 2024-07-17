import os
import re
import ast
from openai import OpenAI

# Carregar as variáveis de ambiente do arquivo .env

class GPTAnalyzer:
    def __init__(self):
        self.token_limit = 1224
        self.max_timeout = 200
        self.current_model = "gpt-3.5-turbo-0613"
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def answer_generate(self, messages, temperature = 0.3):
        response = self.client.chat.completions.create(
            model=self.current_model, 
            messages=messages,
            max_tokens=self.token_limit,
            temperature=temperature, 
            timeout=self.max_timeout,
        )
        return [response.choices[0].message.content, response.usage]

    # falta melhorar essa função por um meio de tokenizar
    def limitar_texto(self, texto, limite=7000):
        if len(texto) <= limite:
            return texto
        else:
            return texto[:limite]
        
    def extract_numbered_lines(self, text):
        lines = text.split('\n')
        numbered_lines = [line.strip() for line in lines if re.match(r'^\d+\.', line.strip())]
        return numbered_lines

    def dict_generate(self, text):
        try:
            # text = text.replace('null', '""')
            return ast.literal_eval(text)
        except (SyntaxError, ValueError):
            return None
        
    def ask_generate(self, comando, mensagem):
        mensagens = [
                {"role": "system", "content": f"{comando}"},
                {"role": "user", "content": {mensagem}}
        ]
        return mensagens
    
    def generate_chat(self):
        conversation = []

        while True:
            user_input = input("Você: ")
            conversation.append({"role": "user", "content": user_input})

            ai_text, response = self.answer_generate(messages=conversation)
            
            print(f"GPT: {ai_text}")

            conversation.append({"role": "assistant", "content": ai_text})

            if user_input.lower() == "sair":
                break

