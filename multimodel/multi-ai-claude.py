from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain

# Configurar os modelos de IA
llm_formatter = OpenAI(temperature=0.5)
llm_writer = ChatOpenAI(temperature=0.7)

# Função para formatar o texto e gerar tópicos
format_and_topics_prompt = PromptTemplate(
    input_variables=["text"],
    template="Formate o seguinte texto e gere 5 tópicos principais:\n\n{text}\n\nFormato:\nTítulo:\nTópicos:"
)

format_and_topics_chain = LLMChain(llm=llm_formatter, prompt=format_and_topics_prompt)

# Função para escrever o conteúdo de cada seção
write_content_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Escreva um parágrafo detalhado sobre o seguinte tópico para um ebook:\n\n{topic}"
)

write_content_chain = LLMChain(llm=llm_writer, prompt=write_content_prompt)

# Função para combinar todo o conteúdo em um ebook
combine_ebook_prompt = PromptTemplate(
    input_variables=["content"],
    template="Organize o seguinte conteúdo em um formato de ebook coeso, adicionando uma introdução e conclusão:\n\n{content}"
)

combine_ebook_chain = LLMChain(llm=llm_writer, prompt=combine_ebook_prompt)

# Função principal para gerar o ebook
def generate_ebook(input_text):
    # Passo 1: Formatar e gerar tópicos
    formatted_and_topics = format_and_topics_chain.run(input_text)
    print("Formatação e tópicos gerados:")
    print(formatted_and_topics)
    
    # Passo 2: Escrever conteúdo para cada tópico
    topics = formatted_and_topics.split("Tópicos:")[1].strip().split("\n")
    content = []
    for topic in topics:
        section_content = write_content_chain.run(topic)
        content.append(f"## {topic}\n\n{section_content}")
    
    full_content = "\n\n".join(content)
    print("Conteúdo gerado para cada tópico.")
    
    # Passo 3: Combinar em um ebook
    final_ebook = combine_ebook_chain.run(full_content)
    print("Ebook finalizado:")
    print(final_ebook)
    
    return final_ebook

# Exemplo de uso
input_text = """
A inteligência artificial (IA) está revolucionando diversos setores da sociedade. 
Desde assistentes virtuais até carros autônomos, a IA está mudando a forma como vivemos e trabalhamos. 
No entanto, também existem preocupações éticas e sociais sobre o impacto da IA no futuro do trabalho e na privacidade.
"""

ebook = generate_ebook(input_text)