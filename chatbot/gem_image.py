import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image, ImageTk
from _gemini import GeminiAnalyzer

def process_text():
    text_input = text_entry.get("1.0", tk.END).strip()
    if text_input:
        analyzer = GeminiAnalyzer()
        texto_resposta, _ = analyzer.generate_google_response(text_input)
        result_label.config(text=f"Resposta Analise de Texto: {texto_resposta}")
    else:
        result_label.config(text="Por favor, insira um texto.")

def process_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        analyzer = GeminiAnalyzer()
        prompt_imagem = "Descreva os principais elementos visuais presentes na imagem."
        texto_imagem = analyzer.processed_text_image(url=file_path, prompt=prompt_imagem)
        result_label.config(text=f"Texto Extraído da Imagem: {texto_imagem}")

        image = Image.open(file_path)
        image = image.resize((300, 300), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        image_label.config(image=image)
        image_label.image = image
    else:
        result_label.config(text="Por favor, selecione uma imagem.")

def create_window():
    window = tk.Tk()
    window.title("Análise de Texto e Imagem com Gemini")

    frame = tk.Frame(window, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    text_label = tk.Label(frame, text="Insira seu texto:")
    text_label.pack()

    global text_entry
    text_entry = Text(frame, height=5, width=50)
    text_entry.pack()

    text_button = tk.Button(frame, text="Processar Texto", command=process_text)
    text_button.pack(pady=5)

    image_button = tk.Button(frame, text="Selecionar Imagem", command=process_image)
    image_button.pack(pady=5)

    global image_label
    image_label = tk.Label(frame)
    image_label.pack()

    global result_label
    result_label = tk.Label(frame, text="", wraplength=400, justify="left")
    result_label.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_window()
