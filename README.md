# Planner de Diárias

## 1. Visão Geral do Projeto

O "Planner de Diárias" é uma aplicação de desktop desenvolvida em Python com a biblioteca `Tkinter` e o tema `ttkbootstrap`. O objetivo principal da aplicação é permitir que os usuários calculem os custos de despesas de viagem com base em regras de reembolso pré-definidas (percentuais sobre o salário mínimo).

A aplicação permite:
- Criar e nomear viagens.
- Adicionar múltiplas linhas de despesas, especificando data, tipo e localidade.
- Calcular automaticamente o valor de cada despesa com base em configurações personalizáveis.
- Salvar, carregar e apagar viagens completas em um banco de dados local.
- Gerar um relatório resumido com o detalhamento das despesas e os totais por categoria.

## 2. Arquitetura do Projeto

O projeto segue uma arquitetura em camadas, separando a interface do usuário (View), a lógica de negócio (Controller) e a persistência de dados (Data Layer).

- **Camada de Visualização (View):** Responsável por toda a interface gráfica. É composta por todas as janelas da aplicação (`MainWindow`, `ConfigsWindow`, `ReportWindow`, etc.) e utiliza os widgets do `ttkbootstrap`.

- **Camada de Controle (Controller):** A classe `MainWindow` (`src/main_window.py`) atua como o controlador central, orquestrando o fluxo de dados entre a UI e a camada de dados.

- **Camada de Dados (Data Layer):** A classe `Database` (`src/database.py`) é responsável por toda a comunicação com o banco de dados `SQLite`, abstraindo as consultas SQL.

## 3. Estrutura de Arquivos
Calc. Viagens/
├── src/
│ ├── init.py
│ ├── main_window.py
│ ├── database.py
│ ├── configs_window.py
│ ├── report_window.py
│ └── viagens_window.py
├── main.py
├── README.md
├── requirements.txt
└── icon.ico


## 4. Dependências e Execução

- **Dependências:** A principal dependência externa é `ttkbootstrap`.
- **Como Executar:**
    1.  Crie e ative um ambiente virtual:
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # No Linux/macOS
        # ou
        .venv\Scripts\activate  # No Windows
        ```
    2.  Instale as dependências:
        ```bash
        pip install -r requirements.txt
        ```
    3.  Execute a aplicação:
        ```bash
        python main.py
        ```

## 5. Possíveis Melhorias (v2)

- Implementar uma suíte de testes unitários.
- Adicionar funcionalidade para importar/exportar dados para Excel/CSV.
- Aprimorar o tratamento de exceções.
- Adicionar documentação interna (docstrings) ao código.
