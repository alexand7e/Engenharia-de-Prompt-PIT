import time
import requests
import PIL.Image
import os
from io import BytesIO

# google generative dependence
import google.generativeai as genai
from google.api_core.exceptions import InternalServerError
from google.ai.generativelanguage import HarmCategory
from google.ai.generativelanguage import SafetySetting
from google.api_core.exceptions import DeadlineExceeded, InternalServerError
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API do ambiente
api_key = os.getenv('GEMINI_API_KEY')

class GeminiAnalyzer:
    def __init__(self):
        genai.configure(api_key=api_key)#"=os.getenv("GEMINI_API_KEY"))
        self.client = genai.GenerativeModel('gemini-1.5-pro')
        self.client_image = genai.GenerativeModel('gemini-pro-vision')

        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        }

        self.candidate_count = 1
        # self.define_explain()

    def generate_google_response(self, messages):

        try:
            response = self.client.generate_content(
                messages,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=self.candidate_count,
                    temperature=0.2,
                    max_output_tokens=15000,
                ),
                safety_settings=self.safety_settings
            )
        except InternalServerError:
            time.sleep(60)
            response = self.client.generate_content(
                messages,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=self.candidate_count,
                    temperature=0,
                ),
                safety_settings=self.safety_settings
            )
        try:
            return response.text, response
        except IndexError:
            print("Erro em response.text")
            return None, None
        

    def generate_image_analysis(self, image_data, prompt):
        try:
            response = self.client_image.generate_content(
                [prompt, image_data]
            )
        except InternalServerError:
            time.sleep(60)  # Aguarda um minuto antes de tentar novamente
            return self.generate_image_analysis(image_data, prompt)  # Tentativa recursiva
        except DeadlineExceeded:
            time.sleep(60)  # Aguarda um minuto antes de tentar novamente
            return self.generate_image_analysis(image_data, prompt)  # Tentativa recursiva

        return response.text
    


    def initialize_chat(self):
        global chat
        chat = self.client.start_chat(history=[])


    def generate_chat_response(self, messages, temperature=0.0):
        global chat
        try:
            response = chat.send_message(
                messages,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=self.candidate_count,
                    temperature=temperature,
                ),
                safety_settings=self.safety_settings
            )
        except InternalServerError:
            time.sleep(60)
            response = chat.send_message(
                messages,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=self.candidate_count,
                    temperature=temperature,
                ),
                safety_settings=self.safety_settings
            )
        try:
            return response.text, response
        except IndexError:
            print("Erro em response.text")
            return None, None
    