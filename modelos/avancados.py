from chatbot._gemini import GeminiAnalyzer

def get_prompt_example(prompt_type):
    prompts = {
        'zero_shot': "Qual a importância da inovação tecnológica no crescimento econômico dos países em desenvolvimento?",
        'few_shot': """
        Exemplo 1: Pergunta: Quem pintou 'A Noite Estrelada'? Resposta: Vincent van Gogh.
        Exemplo 2: Pergunta: Qual é o principal ingrediente da paella? Resposta: Arroz.
        Pergunta: Quem foi o primeiro presidente do Brasil? Resposta:
        """,
        'chain_of_thought': "Se um trem sai de São Paulo às 08:00 e viaja a 80 km/h, e outro trem sai do Rio de Janeiro às 09:30 e viaja a 100 km/h, qual trem chegará primeiro em Belo Horizonte? Considere os passos lógicos.",
        'self_consistency': "Qual é o pico mais alto do mundo? Liste sua resposta e verifique se ela é consistente com várias fontes confiáveis.",
        'creative_rewriting': "Reescreva o final da história 'Chapeuzinho Vermelho' onde ela e o lobo se tornam amigos e ensinam uma lição sobre entendimento e amizade às crianças da vila.",
        'automatic_translation': "Traduza a frase 'A tecnologia está mudando o mundo rapidamente' para o francês, mantendo o mesmo tom e nuances.",
        'code_generation': "Escreva um script Python que gere e imprima uma lista de números pares entre 1 e 20."
    }

    # Retorna a string de prompt correspondente ao tipo solicitado, ou uma mensagem de erro se o tipo for inválido
    return prompts.get(prompt_type, "Tipo de prompt inválido. Escolha entre: 'zero_shot', 'few_shot', 'chain_of_thought', 'self_consistency', 'creative_rewriting', 'automatic_translation', 'code_generation'.")

# Exemplos de uso da função
print(get_prompt_example('zero_shot'))
print(get_prompt_example('few_shot'))
print(get_prompt_example('chain_of_thought'))
print(get_prompt_example('self_consistency'))
print(get_prompt_example('creative_rewriting'))
print(get_prompt_example('automatic_translation'))
print(get_prompt_example('code_generation'))
