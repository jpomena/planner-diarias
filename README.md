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

O projeto segue a arquitetura **Model-View-Controller (MVC)**, com uma clara separação de responsabilidades entre as camadas:

-   **Modelo (Model):** Representado pela classe `Database` (`src/database.py`). É responsável por toda a comunicação com o banco de dados `SQLite`, abstraindo as consultas SQL, e gerenciando a persistência e recuperação de dados.
-   **Visão (View):** Composta por todas as janelas e elementos da interface gráfica. Inclui `src/main_window.py`, `src/configs_window.py`, `src/report_window.py`, e `src/viagens_window.py`. A camada View é responsável apenas por exibir dados e capturar interações do usuário, sem lógica de negócios ou acesso direto ao banco de dados.
-   **Controlador (Controller):** A classe `Sasori` em `src/controller.py` atua como o controlador central. Ela orquestra o fluxo de dados entre a View e o Modelo, processa as entradas do usuário, aplica a lógica de negócios e atualiza tanto o Modelo quanto a View.

## 3. Estrutura de Arquivos

```
planner-diarias/
├── src/
│ ├── init.py
│ ├── configs_window.py
│ ├── controller.py
│ ├── database.py
│ ├── main_window.py
│ ├── report_window.py
│ └── viagens_window.py
├── main.py
├── README.md
├── requirements.txt
├── icon.ico
└── TODO.md
```

## 4. Melhorias Recentes (v1.1.0)

Esta seção detalha as principais refatorações e melhorias implementadas:

*   **Padronização de Nomenclatura**: Os nomes dos métodos foram ajustados para seguir o padrão `snake_case`, melhorando a consistência e legibilidade do código em todo o projeto.
*   **Janela de Viagens Unificada**: As classes separadas `AbrirWindow` e `ApagarWindow` em `src/viagens_window.py` foram refatoradas e unificadas em uma única e mais versátil `WindowViagem`. Isso reduz a duplicação de código e otimiza o gerenciamento das operações relacionadas a viagens (abertura e exclusão).
*   **Cálculo de Totais do Relatório Aprimorado**: O método `PreencherTabelaTotais` em `src/report_window.py` foi aprimorado. Agora ele utiliza uma abordagem baseada em dicionário para somar os totais das despesas, substituindo a estrutura anterior de `if/elif`. Essa mudança melhora significativamente a legibilidade, a manutenibilidade e a extensibilidade do código para futuros tipos de despesa.
*   **Ajustes no Controlador**: O arquivo `src/controller.py` foi atualizado para se integrar perfeitamente com a nova classe `WindowViagem`, garantindo a comunicação e a funcionalidade adequadas para abrir e apagar viagens.
*   **Ícone do Aplicativo**: O ícone padrão do Tkinter foi substituído pelo `icon.ico` fornecido, presente na raiz do projeto.

## 5. Dependências e Execução

### Dependências

A principal dependência externa é `ttkbootstrap`. As dependências completas estão listadas em `requirements.txt`.

### Como Executar

1.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv .venv
    # No Linux/macOS:
    source .venv/bin/activate
    # No Windows:
    .venv\Scripts\activate
    ```
2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Execute a aplicação:**
    ```bash
    python main.py
    ```

### Como Gerar um Executável (Windows)

Para criar um único arquivo executável do aplicativo, sem a janela do terminal, use `PyInstaller`:

```bash
pyinstaller --onefile --noconsole --icon=icon.ico main.py
```
O executável será gerado na pasta `dist/`.

## 6. Próximos Passos e Planos Futuros

O futuro do "Planner de Diárias" inclui uma expansão significativa da interface do usuário e da funcionalidade, migrando para uma estrutura de abas:

*   **Interface por Abas**: A janela principal será reestruturada para usar um sistema de abas (`ttk.Notebook`), permitindo uma melhor organização das funcionalidades.
    *   A primeira aba manterá a funcionalidade atual de "Despesas".
    *   Novas abas serão adicionadas para gerenciar despesas específicas relacionadas a:
        *   **Carro**: Para registrar custos como combustível, estacionamento, pedágios, etc.
        *   **Avião**: Para gerenciar custos de passagens, taxas de embarque, bagagem, etc.
        *   **Hotel**: Para registrar valores de diárias, serviços de quarto, etc.

Esta mudança implicará em atualizações nas camadas de View, Controller e Model para suportar os novos tipos de dados e lógica de negócios.




<a href="https://www.flaticon.com/free-icons/trip" title="trip icons">Trip icons created by Wichai.wi - Flaticon</a>