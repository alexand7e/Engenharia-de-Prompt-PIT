from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape_service(driver, card):
    # Extrair título e descrição
    titulo = card.find_element(By.CLASS_NAME, "xvia-listing-card__title").text
    descricao = card.find_element(By.CLASS_NAME, "xvia-listing-card__subtitle").text
    
    # Clicar no botão "Acessar Serviço Digital"
    botao = card.find_element(By.XPATH, ".//button[contains(text(), 'Acessar Serviço Digital')]")
    driver.execute_script("arguments[0].click();", botao)
    
    # Esperar pela nova página e extrair informações adicionais
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "xvia-card-section")))
        
        secretaria = driver.find_element(By.CLASS_NAME, "xvia-card-section").text
        
        info_elements = driver.find_elements(By.CLASS_NAME, "xvia-info__text")
        endereco = info_elements[0].text if len(info_elements) > 0 else "Não disponível"
        horario = info_elements[1].text if len(info_elements) > 1 else "Não disponível"
        
        # Voltar para a página anterior
        driver.back()
        
        # Esperar pelos cards carregarem novamente
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "xvia-listing-card")))
        
        return {
            "titulo": titulo,
            "descricao": descricao,
            "secretaria": secretaria,
            "endereco": endereco,
            "horario": horario
        }
    except TimeoutException:
        print(f"Timeout ao carregar detalhes para o serviço: {titulo}")
        driver.back()
        return None

# Configuração do driver
driver = webdriver.Chrome()

# URL da página
url = "https://pidigital.pi.gov.br/app/catalog/list/"

# Navegar até a página
driver.get(url)

# Lista para armazenar os resultados
resultados = []

# Esperar até que os cards de serviço estejam carregados
wait = WebDriverWait(driver, 10)
cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "xvia-listing-card")))

# Iterar sobre cada card
for card in cards:
    resultado = scrape_service(driver, card)
    if resultado:
        resultados.append(resultado)

# Imprimir os resultados
for resultado in resultados:
    print(f"Título: {resultado['titulo']}")
    print(f"Descrição: {resultado['descricao']}")
    print(f"Secretaria: {resultado['secretaria']}")
    print(f"Endereço: {resultado['endereco']}")
    print(f"Horário: {resultado['horario']}")
    print("---")

# Fechar o navegador
driver.quit()