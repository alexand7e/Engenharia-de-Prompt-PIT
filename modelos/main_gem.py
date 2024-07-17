from chatbot._gemini import GeminiAnalyzer

def main():
    analyzer = GeminiAnalyzer()
    messages_texto = "Ola bom dia"

    texto_resposta, _ = analyzer.generate_google_response(messages_texto)
    print("Resposta Analise de Texto:", texto_resposta)

    url_imagem = "https://ipapel.com.br/wp-content/uploads/2023/05/QIPTEPA38009.webp" 
    prompt_imagem = """Descreva os principais elementos visuais presentes na imagem."""

    texto_imagem = analyzer.processed_text_image(url = url_imagem, prompt = prompt_imagem)
    print("Texto Extraído da Imagem:", texto_imagem)

if __name__ == "__main__":
    main()
