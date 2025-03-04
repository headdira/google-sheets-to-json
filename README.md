```markdown
# Projeto de Extração de Dados do Google Sheets para JSON

Este projeto permite extrair dados de múltiplas abas de uma planilha do Google Sheets e gerar um arquivo JSON com os dados corrigidos, com suporte para caracteres especiais.

## Funcionalidades

- Autenticação com a API do Google Sheets.
- Extração de dados de abas selecionadas de uma planilha.
- Correção de caracteres especiais.
- Geração de um arquivo JSON com os dados extraídos.

## Requisitos

- Python 3.13.1
- Bibliotecas: `gspread`, `oauth2client`

## Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/headdira/google-sheets-to-json.git
   ```
   
2. Instale as dependências:
   ```bash
   pip install gspread oauth2client
   ```

3. Coloque o arquivo `credentials.json` da sua conta de serviço do Google API na mesma pasta do script.

4. Altere o ID da planilha (`sheet_id`) no código para o ID da planilha que você deseja acessar.

5. Execute o script:
   ```bash
   python app.py
   ```

6. Escolha as abas que deseja acessar e aguarde a geração do arquivo `conectividade_2024.json` com os dados corrigidos.

## Estrutura do Projeto

- `app.py`: Script principal para a extração dos dados e geração do JSON.
- `credentials.json`: Arquivo de credenciais da API do Google (não incluído no repositório).

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
```