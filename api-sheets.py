import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Função para autenticar com o Google Sheets
def autenticar_google_sheets():
    escopo = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credenciais = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', escopo)
    cliente = gspread.authorize(credenciais)
    return cliente

# Função para extrair as abas da planilha
def extrair_dados_da_planilha(sheet_id):
    cliente = autenticar_google_sheets()
    planilha = cliente.open_by_key(sheet_id)  # ID da planilha
    abas = planilha.worksheets()  # Obtém todas as abas da planilha
    return abas

# Função para selecionar múltiplas abas desejadas
def selecionar_abas(abas):
    print("\nAbas encontradas:")
    for i, aba in enumerate(abas, 1):
        print(f"{i}. {aba.title}")  # Mostra o nome de cada aba com número de índice

    while True:
        try:
            escolha = input("\nEscolha os números das abas que deseja acessar, separados por vírgula (exemplo: 1, 3, 5): ")
            escolhas = [int(x.strip()) for x in escolha.split(",")]  # Converte as escolhas para uma lista de inteiros
            if all(1 <= e <= len(abas) for e in escolhas):
                return [abas[e - 1] for e in escolhas]  # Retorna as abas selecionadas
            else:
                print("Escolha inválida, por favor tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite números válidos separados por vírgula.")

# Função para extrair dados da aba escolhida
def extrair_dados_da_aba(aba):
    dados = aba.get_all_values()  # Extrai todos os valores da aba
    cabecalho = dados[0]  # Primeiro item (cabeçalho)
    dados_selecionados = dados[1:]  # Resto dos dados (sem o cabeçalho)

    dados_com_header = []

    for linha in dados_selecionados:
        item = {}
        for i, valor in enumerate(linha):
            if i < len(cabecalho):  # Atribui o valor da linha ao cabeçalho correspondente
                item[cabecalho[i]] = valor
        dados_com_header.append(item)

    return dados_com_header

# Função para corrigir caracteres especiais
def corrigir_caracteres_especiais(texto):
    substituicoes = {
        'Ã©': 'é',
        'Ã§': 'ç',
        'Ã³': 'ó',
        'Ãº': 'ú',
        'Ã´': 'ô',
        'Ã¡': 'á',
        'Ã£': 'ã',
        'Ã': 'Á',
        'Â': '',
    }
    for char_errado, char_correto in substituicoes.items():
        texto = texto.replace(char_errado, char_correto)
    return texto

# Função para corrigir dados e gerar JSON
def gerar_json(dados):
    dados_corrigidos = []
    for item in dados:
        item_corrigido = {}
        for key, value in item.items():
            if isinstance(value, str):  # Verifica se o valor é uma string
                value_corrigido = corrigir_caracteres_especiais(value)
                item_corrigido[key] = value_corrigido
            else:
                item_corrigido[key] = value
        dados_corrigidos.append(item_corrigido)

    # Salvando os dados corrigidos em um arquivo JSON com codificação UTF-8
    resultado = {'dados': dados_corrigidos}
    with open('conectividade_2024.json', 'w', encoding='utf-8') as json_file:
        json.dump(resultado, json_file, indent=4, ensure_ascii=False)
    print("Arquivo JSON gerado com sucesso!")

    return resultado  # Retorna o resultado para utilização posterior

def main():
    sheet_id = '1tBxD8kzGkcOwg6HIohEIi8kpmvp6CFH_3NdC9oeG9Ac'  # ID da planilha
    abas = extrair_dados_da_planilha(sheet_id)

    if abas:
        abas_selecionadas = selecionar_abas(abas)  # Chama a função para escolher múltiplas abas
        dados_totais = []

        # Extraindo dados das abas selecionadas
        for aba in abas_selecionadas:
            print(f"\nVocê selecionou a aba: {aba.title}")
            dados = extrair_dados_da_aba(aba)
            if dados:
                print(f"Dados extraídos da aba {aba.title}: {dados[:2]}")  # Mostra os dois primeiros registros como exemplo
                dados_totais.extend(dados)  # Adiciona os dados da aba selecionada à lista de dados totais
            else:
                print(f"Nenhum dado encontrado na aba {aba.title}.")

        if dados_totais:
            gerar_json(dados_totais)  # Gerando o JSON com os dados de todas as abas selecionadas
        else:
            print("Nenhum dado encontrado nas abas selecionadas.")
    else:
        print("Nenhuma aba encontrada!")

if __name__ == "__main__":
    main()
