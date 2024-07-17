from _gpt import GPTAnalyzer


def ask_generate(acao, explain):

    mensagens = [
        {"role": "system", "content": explain},
        {"role": "user", "content": f"O que aconteceu:\n'''{acao}'''\nResposta: "}
    ]
    return mensagens


def processar_prompt(mensagem):

    modelo = GPTAnalyzer()
    resposta = modelo.answer_generate(messages=mensagem)
    print(resposta)

# Exemplo de uso completo
acao_exemplo = "A máquina foi ligada às 14h, mas não iniciou corretamente."
explain_exemplo = "A ação que você está perguntando refere-se a um problema técnico comum em máquinas antigas."

# Construindo o prompt
prompt = ask_generate(acao_exemplo, explain_exemplo)

# Processando e obtendo a resposta
processar_prompt(prompt)