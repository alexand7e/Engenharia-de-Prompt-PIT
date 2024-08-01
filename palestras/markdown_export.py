import subprocess
from lmm import GeminiAnalyzer
import os
from fpdf import FPDF

class PDFGenerator:
    def __init__(self, output_path=''):
        self.output_path = output_path
        self.input_path = os.getcwd()+"//teste.md"
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def ensure_directory(self):
        """Garante que o diretório de saída exista."""
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def add_title(self, text):
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, text, ln=True)

    def add_subtitle(self, text):
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, text, ln=True)

    def add_paragraph(self, text):
        self.pdf.set_font("Arial", "", 12)
        self.pdf.multi_cell(0, 10, text)

    def generate(self, content, output_file):
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                self.add_title(line[2:])
            elif line.startswith('## '):
                self.add_subtitle(line[3:])
            elif line.startswith('### '):
                self.add_subtitle(line[4:])
            elif line.strip():
                self.add_paragraph(line)
        
        self.pdf.output(output_file)
        
    def export_marp_to_pdf(self):
        """Converte um arquivo Markdown (Marp) para PDF usando o comando marp."""
        try:
            # Use o caminho completo para o executável marp, se necessário
            marp_path = 'marp'  # Ou forneça o caminho completo, ex: r'C:\path\to\marp.exe'
            command = [marp_path, f'{self.input_path}', '--pdf', '-o', f'{self.output_path}']
            subprocess.run(command, check=True)
            print(f"PDF exportado com sucesso: {self.output_path}")
            return self.output_path
        except subprocess.CalledProcessError as e:
            print(f"Erro ao exportar PDF: {e}")
        except FileNotFoundError as e:
            print(f"Comando 'marp' não encontrado: {e}")

    def criar_prompts(self, texto, saída, seção: None):
        """Cria prompts para diferentes saídas com base no texto de entrada."""
        prompts = {
'primeiro': '''
# Instrução
A partir do texto abaixo, crie uma estrutura de tópicos em markdown, com títulos (#) e subtítulos (##)
''',
'segundo': f'''
# Instrução
Com base no texto informado, escreva o conteúdo de cada seção. Seja coerente com a quantidade de texto, mantendo a quantidade de palavras do texto original.
Use uma estrutura de tópicos em markdown, com títulos (#) até subtítulos (##)

# Seções
"""
{seção}
"""
'''
        }
        comando = prompts.get(saída)
        if comando:
            return comando + f'\n# Texto para resumir:\n{texto}\n'
        else:
            return None

    def process_prompt(self, text):
        """Gera uma saída formatada usando um analisador externo."""
        analyzer = GeminiAnalyzer()
        seção = ""
        saída = ""
        for i in range(2):
            if i == 0:
                seção = None 
                saída = 'primeiro' 
            else:
                seção = resultado 
                saída = 'segundo' 

            prompt = self.criar_prompts(text, saída, seção)
            resultado, _ = analyzer.generate_google_response(prompt)

        print(resultado)
        self.resultado = resultado.replace("*", "")
        self.generate(self.resultado, self.output_path)
        return self.output_path

