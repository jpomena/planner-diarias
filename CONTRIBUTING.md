# Contribuindo para o Planner Diarias

Primeiramente, obrigado por considerar contribuir com o Planner Diarias! São pessoas como você que tornam a comunidade de código aberto tão incrível.

Acolhemos qualquer tipo de contribuição, não apenas código. Você pode ajudar com:
*   **Relatando um bug**
*   **Discutindo o estado atual do código**
*   **Enviando uma correção**
*   **Propondo novas funcionalidades**
*   **Tornando-se um mantenedor**

## Primeiros Passos

### Pré-requisitos

*   Python 3.8+
*   Git

### Configuração do Ambiente de Desenvolvimento

1.  **Faça um fork do repositório** no GitHub.
2.  **Clone o seu repositório forkado** para sua máquina local:
    ```bash
    git clone https://github.com/SEU_USUARIO/planner-diarias.git
    cd planner-diarias
    ```
3.  **Crie um ambiente virtual**:
    ```bash
    python -m venv .venv
    ```
4.  **Ative o ambiente virtual**:
    *   No Windows:
        ```bash
        .venv\Scripts\activate
        ```
    *   No macOS e Linux:
        ```bash
        source .venv/bin/activate
        ```
5.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```
6.  **Execute a aplicação**:
    ```bash
    python main.py
    ```

## Como Contribuir

### Relatando Bugs

Se você encontrar um bug, por favor, abra uma issue no GitHub. Inclua:
*   Um título claro e descritivo.
*   Uma descrição detalhada do problema.
*   Passos para reproduzir o bug.
*   Quaisquer capturas de tela ou mensagens de erro relevantes.

### Sugerindo Melhorias

Se você tem uma ideia para uma nova funcionalidade ou uma melhoria em uma existente, por favor, abra uma issue no GitHub para discuti-la. Isso nos permite coordenar nossos esforços e evitar trabalho duplicado.

### Pull Requests

1.  Crie uma nova branch para sua funcionalidade ou correção de bug:
    ```bash
    git checkout -b feature/sua-feature
    ```
2.  Faça suas alterações e commite-as com uma mensagem descritiva.
3.  Envie suas alterações para o seu repositório forkado:
    ```bash
    git push origin feature/sua-feature
    ```
4.  Abra um pull request para a branch `main` do repositório original.
5.  Forneça uma descrição clara das alterações no seu pull request.

## Guias de Estilo

*   Este projeto segue o guia de estilo [PEP 8](https://www.python.org/dev/peps/pep-0008/) para o código Python.
*   Os nomes dos métodos devem usar `snake_case`. [[memory:6152723]]

## Código de Conduta

Este projeto e todos que participam dele são regidos pelo [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, espera-se que você cumpra este código. Por favor, reporte comportamentos inaceitáveis.

Aguardamos suas contribuições!