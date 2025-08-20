# Planner de Diárias

## 1. Visão Geral do Projeto

O "Planner de Diárias" é uma aplicação de desktop desenvolvida em Python com a biblioteca `Tkinter` e o tema `ttkbootstrap`. Seu propósito principal é auxiliar usuários no cálculo e registro de despesas de viagem, baseando-se em regras de reembolso e configurações personalizáveis.

As principais funcionalidades incluem:

-   **Gerenciamento de Viagens**: Capacidade de criar novas viagens, salvar o progresso, carregar viagens existentes e excluí-las permanentemente do sistema.
-   **Registro Detalhado de Despesas**:
    -   **Refeições**: Inclusão de despesas diárias com alimentação (lanche, café da manhã, almoço, café da tarde, jantar), com cálculo automático baseado em um percentual do salário mínimo e na localização (capital ou outras cidades).
    -   **Combustível**: Registro de rotas e distâncias para cálculo de custos de combustível, considerando o consumo do veículo e o preço por litro.
    -   **Passagens Aéreas**: Adição de detalhes e custos relacionados a bilhetes de avião.
    -   **Hospedagem**: Cadastro de datas de início e fim, local e valor total da hospedagem.
-   **Configurações Flexíveis**: Permite ajustar o valor do salário mínimo de referência, as porcentagens de reembolso para cada tipo de refeição, e as configurações de combustível (consumo e custo).
-   **Geração de Relatórios**: Criação de um relatório consolidado que detalha todas as despesas registradas e apresenta um resumo total por categoria (EM DESENVOLVIMENTO).

## 2. Estrutura de Arquivos

planner-diarias/
├── src/
│ ├── __init__.py
│ ├── config_window.py          # Janela de configurações
│ ├── controller.py             # Controlador principal
│ ├── database.py               # Gerenciamento do banco de dados
│ ├── main_window.py            # Janela principal da aplicação
│ ├── report_window.py          # Janela de relatório de despesas
│ ├── tab_accomodations.py      # Aba para despesas de hospedagem
│ ├── tab_expenses.py           # Aba para despesas de refeições
│ ├── tab_fuel.py               # Aba para despesas de combustível
│ ├── tab_plane_tickets.py      # Aba para despesas de passagens aéreas
│ └── trip_mgmt_window.py       # Janela para gerenciamento (abrir/apagar) de viagens
├── main.py                     # Ponto de entrada da aplicação
├── README.md                   # Este arquivo
├── requirements.txt            # Dependências do projeto
├── icon.ico                    # Ícone do aplicativo
├── TODO.md                     # Lista de tarefas e planos futuros
└── Sugestões_Gemini            # Sugestões de melhoria arquitetural (pelo modelo de IA)

## 3. Melhorias Recentes

Esta seção destaca as refatorações e melhorias mais recentes no projeto:

*   **Criação de Tabela de Hospedagem**: Foi corrigido um erro de digitação na definição da tabela `accomodations` em `src/database.py`, onde o nome da coluna `trip_integer` foi corrigido para `trip_id INTEGER`. Além disso, a sintaxe SQL para a definição da chave estrangeira foi ajustada para incluir o tipo de dado `INTEGER`.
*   **Ajuste na Passagem de Dados para Hospedagem**: Em `src/controller.py`, a chamada ao método `get_accomodations_data` na aba de hospedagem foi corrigida para incluir os parênteses `()`, garantindo que o método seja invocado e que os dados sejam passados corretamente para o banco de dados, resolvendo um `TypeError`.
*   **Melhoria na Modularização da Interface**: A interface principal foi refatorada para utilizar um sistema de abas (`ttk.Notebook`), permitindo uma organização mais intuitiva das diferentes categorias de despesas (Refeições, Combustível, Passagens Aéreas, Hospedagem). Cada categoria agora possui sua própria classe de aba dedicada (`tab_expenses.py`, `tab_fuel.py`, etc.).
*   **Padronização de Nomenclatura**: Métodos e variáveis foram ajustados para seguir o padrão `snake_case`, conforme preferência do usuário, aumentando a consistência e legibilidade do código.
*   **Gerenciamento Unificado de Viagens**: As funcionalidades de abrir e apagar viagens foram consolidadas em uma única janela (`trip_mgmt_window.py`), reduzindo a duplicação de código e simplificando o fluxo de gerenciamento de viagens.
*   **Cálculo de Totais no Relatório**: A lógica de cálculo de totais no relatório (`src/report_window.py`) foi aprimorada, utilizando uma abordagem mais flexível para somar os valores por tipo de despesa, facilitando a adição de novas categorias no futuro.
*   **Ícone do Aplicativo**: O aplicativo agora utiliza um ícone personalizado (`icon.ico`), melhorando a experiência visual.

## 4. Dependências e Execução

### Dependências

A principal dependência externa é `ttkbootstrap`, utilizada para o tema visual da aplicação. Todas as dependências necessárias estão listadas no arquivo `requirements.txt`.

### Como Executar

Para configurar e rodar o projeto localmente:

1.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv .venv
    # No Linux/macOS:
    source .venv/bin/activate
    # No Windows (PowerShell):
    .venv\Scripts\activate
    ```

2.  **Instale as dependências do projeto:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    ```bash
    python main.py
    ```

### Como Gerar um Executável (Windows)

Para criar um único arquivo executável do aplicativo, sem a janela do terminal, você pode usar `PyInstaller`. Certifique-se de ter o `PyInstaller` instalado (`pip install pyinstaller`).

```bash
pyinstaller --onefile --noconsole --icon=icon.ico main.py
```

Após a execução, o arquivo executável será gerado na pasta `dist/`.


---

<a href="https://www.flaticon.com/free-icons/trip" title="trip icons">Trip icons created by Wichai.wi - Flaticon</a>