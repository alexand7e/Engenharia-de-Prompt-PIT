from time import sleep
from _gpt import GPTAnalyzer
from unittest.mock import patch

def complex_task_prompts(region):
    prompts = [
        f"Descreva os principais tipos de culturas agrícolas na {region}.",
        f"Explique como as mudanças climáticas afetaram essas culturas nos últimos 10 anos na {region}.",
        f"Identifique e discuta as estratégias que os agricultores na {region} estão adotando para mitigar os impactos das mudanças climáticas.",
        f"Qual o impacto econômico estimado dessas mudanças para a agricultura na {region} nos próximos 10 anos?"
    ]
    return prompts


def plan_trip_steps(destination):
    steps = [
        f"Liste as principais cidades turísticas da {destination} que devem ser incluídas em uma viagem de duas semanas.",
        f"Para cada cidade listada, identifique as principais atrações turísticas.",
        "Crie um itinerário diário que inclua transporte, hospedagem e alimentação.",
        "Calcule o orçamento aproximado necessário para a viagem, incluindo despesas de viagem, acomodação, alimentação e visitas a atrações."
    ]
    return steps


def optimize_information_flow(policy):
    optimized_prompts = [
        f"Qual é o objetivo principal da {policy}?",
        f"Explique os mecanismos através dos quais a {policy} pretende atingir seus objetivos.",
        "Identifique os grupos sociais que serão mais afetados pela política.",
        "Analise os impactos econômicos a curto e longo prazo da política.",
        "Discuta possíveis reações do mercado e de outros setores da sociedade à implementação desta política.",
        "sair"
    ]
    return optimized_prompts


def main():
    prompts = plan_trip_steps("Piauí")

    try:
        ia = GPTAnalyzer()
        print("GPTAnalyzer instanciado com sucesso.")
    except NameError:
        print("Classe GPTAnalyzer não está definida.")
        return

    original_input = input 

    try:
        # Simulando os inputs
        with patch('builtins.input', side_effect=prompts):
            ia.generate_chat()

    finally:
        __builtins__.input = original_input  # Restaura o input para a função original
        print("Input restaurado para função original.")

# Executa a função principal
main()
