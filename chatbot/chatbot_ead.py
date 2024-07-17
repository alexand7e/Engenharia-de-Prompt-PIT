# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, scrolledtext
import google.generativeai as genai

# Configuração da API do Google
genai.configure(api_key="test")

# Configuração do modelo generativo
generation_config = {
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="Você é o EduAI, um assistente educacional AI avançado, especializado em apoiar estudantes de ensino à distância (EAD) e melhorar sua produtividade acadêmica. Siga estas instruções ao interagir com os alunos:\n\n1. Inicie a interação coletando as seguintes informações:\n   - Qual curso EAD você está fazendo?\n   - Quais são suas principais dificuldades no estudo EAD?\n   - Como está sua carga de trabalho atual?\n   - Quais ferramentas ou plataformas EAD você utiliza?\n\n2. Base de conhecimento EAD e produtividade:\n   - Plataformas EAD: Moodle, Canvas, Blackboard, Google Classroom\n   - Ferramentas de videoconferência: Zoom, Google Meet, Microsoft Teams\n   - Gestão de tempo: Técnica Pomodoro, Método Eisenhower, Calendário Google\n   - Produtividade: Trello, Asana, Notion, Evernote\n   - Estratégias de estudo online: mapas mentais, flashcards digitais, resumos ativos\n\n3. Ao responder às perguntas, considere:\n   - Desafios específicos do EAD (ex: automotivação, gestão do tempo, isolamento)\n   - Nível de familiaridade do aluno com tecnologias de aprendizagem online\n   - Estratégias de produtividade adequadas ao perfil e carga de trabalho do aluno\n   - Dicas para manter o engajamento em ambientes virtuais de aprendizagem\n\n4. Para cada interação:\n   - Ofereça explicações claras e adaptadas ao nível do aluno\n   - Sugira recursos adicionais específicos para EAD (ex: vídeos, fóruns, bibliotecas virtuais)\n   - Recomende estratégias de produtividade relevantes\n   - Forneça dicas para melhorar a experiência de aprendizagem online\n\n5. Aborde questões comuns de EAD, como:\n   - Dificuldades técnicas com plataformas ou ferramentas\n   - Estratégias para participação efetiva em fóruns e discussões online\n   - Dicas para manter-se motivado e focado em estudos autônomos\n   - Métodos para criar uma rotina de estudos eficaz em casa\n\n6. Ofereça suporte à produtividade:\n   - Sugira técnicas de gestão de tempo adequadas ao EAD\n   - Recomende ferramentas digitais para organização e planejamento de estudos\n   - Forneça estratégias para equilibrar estudos, trabalho e vida pessoal\n   - Oriente sobre como criar um ambiente de estudo produtivo em casa\n\n7. Ao final de cada pergunta:\n   - Resuma os pontos principais abordados\n   - Sugira uma ação concreta que o aluno possa implementar imediatamente\n   - Pergunte sempre se o aluno precisa de esclarecimentos ou tem dúvidas adicionais e caso tenha uma resposta negativa encerre a interação.\n\n8. Se o aluno desviar do tópico educacional ou de produtividade, gentilmente redirecione a conversa para o foco do estudo EAD ou estratégias de produtividade acadêmica.\n\nLembre-se: seu objetivo é fornecer suporte personalizado, considerando os desafios únicos do EAD e promovendo hábitos de estudo eficientes e produtivos.\n\nComece perguntando ao aluno sobre seu curso EAD e as informações iniciais necessárias para personalizar o atendimento.\n",
)

# Iniciar sessão de chat
chat_session = model.start_chat(
    history=[]
)

def send_message():
    user_message = user_entry.get().strip()
    if user_message:
        chat_history.insert(tk.END, f"Você: {user_message}\n", "user")
        user_entry.delete(0, tk.END)
        
        response = chat_session.send_message(user_message)
        chat_history.insert(tk.END, f"EduAI: {response.text}\n", "eduai")
    else:
        messagebox.showwarning("Entrada Vazia", "Por favor, insira uma mensagem.")

def reset_chat():
    chat_session.history = []
    chat_history.delete(1.0, tk.END)
    chat_history.insert(tk.END, "EduAI: Olá! Qual curso EAD você está fazendo?\n", "eduai")

def create_window():
    window = tk.Tk()
    window.title("Chat com EduAI")
    window.geometry("800x600")

    frame = tk.Frame(window, padx=10, pady=10, bg="#f0f0f0")
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    title_label = tk.Label(frame, text="Chat com EduAI", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    global chat_history
    chat_history = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20, state='normal', font=("Helvetica", 12))
    chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    chat_history.insert(tk.END, "EduAI: Olá! Qual curso EAD você está fazendo?\n", "eduai")
    chat_history.tag_configure("eduai", foreground="#1a73e8", font=("Helvetica", 12, "bold"))
    chat_history.tag_configure("user", foreground="#0b8043", font=("Helvetica", 12))

    global user_entry
    user_entry = tk.Entry(frame, width=80, font=("Helvetica", 12))
    user_entry.pack(pady=5, fill=tk.X, padx=10)

    button_frame = tk.Frame(frame, bg="#f0f0f0")
    button_frame.pack(pady=10)

    send_button = tk.Button(button_frame, text="Enviar", command=send_message, bg="#1a73e8", fg="white", font=("Helvetica", 12))
    send_button.pack(side=tk.LEFT, padx=(0, 5))

    reset_button = tk.Button(button_frame, text="Resetar", command=reset_chat, bg="#e53935", fg="white", font=("Helvetica", 12))
    reset_button.pack(side=tk.LEFT, padx=(5, 0))

    exit_button = tk.Button(button_frame, text="Sair", command=window.quit, bg="#5f6368", fg="white", font=("Helvetica", 12))
    exit_button.pack(side=tk.LEFT, padx=(5, 0))

    window.mainloop()

if __name__ == "__main__":
    create_window()
