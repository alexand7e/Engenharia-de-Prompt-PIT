import streamlit as st
from config import YouTubeTranscriber
from markdown_export import PDFGenerator
import os

from urllib.parse import urlparse, urlunparse

def clean_url(url):
    """
    Remove o conteúdo extra de uma URL, mantendo apenas a parte base do URL.
    """
    parsed_url = urlparse(url)
    clean_path = parsed_url.path.split('&')[0]  # Remove qualquer coisa após o primeiro '&'
    clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, clean_path, '', '', ''))
    return clean_url

def main():
    st.title("Transcritor de Vídeos do YouTube")
    st.write("Insira a URL de um vídeo do YouTube para baixar e transcrever o áudio.")

    # Inicialização do estado da sessão
    if 'transcription' not in st.session_state:
        st.session_state.transcription = None
    if 'url' not in st.session_state:
        st.session_state.url = ""

    # Campo de entrada para URL do YouTube
    url = st.text_input("URL do Vídeo do YouTube", value=clean_url(st.session_state.url))

    # Botão para acionar o processo de transcrição
    if st.button("Transcrever"):
        if url:
            st.session_state.url = url  # Armazena a URL atual
            with st.spinner("Processando..."):
                transcriber = YouTubeTranscriber(url)
                transcriber.process()
                st.session_state.transcription = transcriber.get_transcription()
                
            if st.session_state.transcription:
                st.success("Transcrição concluída!")
            else:
                st.error("Falha ao transcrever o vídeo.")
        else:
            st.error("Por favor, insira uma URL válida do YouTube.")

    # Exibição da transcrição
    if st.session_state.transcription:
        st.text_area("Transcrição", st.session_state.transcription, height=300)

        option = st.selectbox("Escolha o formato para baixar:",
                              ('Selecione um formato', 'eBook'))

        if option != 'Selecione um formato':
            if st.button("Gerar PDF"):
                with st.spinner(f"Gerando {option}..."):
                    mk = PDFGenerator(os.path.join(os.getcwd(), "documento.pdf"))
                    content = st.session_state.transcription
                    pdf_path = mk.process_prompt(content)
                    print(content)
                    st.success(f"{option} gerado com sucesso!")
                    st.download_button(f'Baixar {option} em PDF', 
                                       data=open(pdf_path, 'rb').read(), 
                                       file_name=f"{option.lower().replace(' ', '_')}.pdf",
                                       mime="application/pdf")

if __name__ == "__main__":
    main()