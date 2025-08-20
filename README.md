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

#### :rocket: Novas Features

*   **Múltiplas Abas de Despesas:** A aplicação foi reestruturada para suportar diferentes tipos de despesas em abas separadas. Agora existem abas para:
    *   `Refeições` (`tab_expenses.py`): Funcionalidade similar à da versão antiga, mas agora contida em sua própria aba.
    *   `Combustível` (`tab_fuel.py`): Permite registrar despesas com combustível, calculando o valor com base na distância, consumo médio e preço por litro.
    *   `Passagens Aéreas` (`tab_plane_tickets.py`): Permite registrar custos de passagens aéreas, com campos para datas de ida/volta e origem/destino.
    *   `Hospedagem` (`tab_accomodations.py`): Permite registrar custos de hospedagem, com campos para período e localização.
*   **Configurações Específicas por Aba:** A janela de configurações agora mostra opções relevantes para a aba atualmente selecionada. Por exemplo, ao visualizar a aba `Combustível`, as configurações mostrarão opções para preço do litro e consumo médio do veículo.

#### :building_construction: Refatoração e Mudanças Estruturais

*   **Arquitetura Baseada em Abas (Tabs):** A mudança mais significativa foi a refatoração da `MainWindow`. Em vez de uma única tela com uma lista de despesas, a janela principal agora usa um `ttk.Notebook` para organizar as diferentes categorias de despesas (`Refeições`, `Combustível`, etc.) em abas.
*   **Renomeação e Reorganização de Arquivos:**
    *   `controller.py`: A classe `Sasori` foi renomeada para `MainController`.
    *   `configs_window.py` foi renomeado para `config_window.py`.
    *   `viagens_window.py` foi renomeado para `trip_mgmt_window.py`.
    *   A lógica que antes estava diretamente em `main_window.py` para criar as linhas de despesa foi movida e dividida entre os novos arquivos de "abas" (`tab_expenses.py`, `tab_fuel.py`, etc.).
*   **Banco de Dados:** O esquema do banco de dados foi expandido para suportar as novas categorias de despesas. Foram criadas novas tabelas:
    *   `fuel`: Para armazenar dados de combustível.
    *   `plane_tickets`: Para armazenar dados de passagens aéreas.
    *   `accomodations`: Para armazenar dados de hospedagem.
    *   A tabela `viagens` foi renomeada para `trips` e `despesas` para `expenses`.
*   **Lógica do Controlador:** O `MainController` foi atualizado para gerenciar a criação e interação com as novas abas, além de orquestrar o salvamento e carregamento dos dados de todas as tabelas do banco de dados.

#### :art: Melhorias na Interface do Usuário (UI)

*   **Navegação por Abas:** A interface principal agora é mais organizada, permitindo que o usuário navegue facilmente entre os diferentes tipos de despesas.
*   **Botão de Configurações Contextual:** O botão "Configurações" agora só aparece quando uma aba que possui configurações específicas (como `Refeições` ou `Combustível`) está ativa.

#### :wastebasket: Código Removido/Substituído

*   O arquivo `src/viagens_window.py` foi efetivamente substituído por `src/trip_mgmt_window.py`, que possui uma funcionalidade muito similar, mas com nomes de classes e variáveis atualizados para refletir a nova estrutura.
*   A maior parte da lógica de criação de widgets de despesa que estava em `src/main_window.py` foi removida e reimplementada dentro das classes de cada aba.

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