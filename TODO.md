# Lista de Tarefas - Planner de Diárias - Implementação de Abas

### Refatoração da Interface (Prioridade Alta)

-   [ ] **Reestruturar `src/main_window.py` para usar Abas (`ttk.Notebook`):**
    -   [ ] Adicionar um widget `ttk.Notebook` (abas) à `MainWindow`.
    -   [ ] Migrar todo o conteúdo da aba "Despesas" (elementos da interface e suas lógicas de layout) para um `ttk.Frame` dedicado que será adicionado como a primeira aba.

-   [ ] **Criar novas classes/arquivos para as abas de "Carro", "Avião" e "Hotel":**
    -   [ ] Criar `src/carro_window.py`: Definir a interface (campos de entrada para dados de carro como combustível, estacionamento, etc.) e métodos de layout.
    -   [ ] Criar `src/aviao_window.py`: Definir a interface (campos para passagens, taxas, etc.) e métodos de layout.
    -   [ ] Criar `src/hotel_window.py`: Definir a interface (campos para diárias, serviços, etc.) e métodos de layout.
    -   [ ] Cada nova classe de aba deve receber o `controller` como parâmetro para delegar a lógica.

### Atualizações no Controlador (Prioridade Alta)

-   [ ] **Adaptar `src/controller.py` para gerenciar as novas abas:**
    -   [ ] Instanciar as novas classes de abas (`CarroWindow`, `AviaoWindow`, `HotelWindow`) no `__init__` da classe `Sasori`.
    -   [ ] Passar a instância do `controller` para cada uma dessas novas abas.
    -   [ ] Desenvolver novos métodos no `controller` para manipular a lógica de negócios e persistência de dados para "Carro", "Avião" e "Hotel".

### Modelo (Banco de Dados) (Prioridade Média)

-   [ ] **Estender `src/database.py` para as novas abas:**
    -   [ ] Criar novas tabelas no banco de dados para armazenar informações de "Carro", "Avião" e "Hotel" (Ex: `tabela_carros`, `tabela_avioes`, `tabela_hoteis`).
    -   [ ] Adicionar métodos ao `Database` para `add`, `get` e `delete` dados específicos de carro, avião e hotel.

### Lógica Específica das Abas (Prioridade Média)

-   [ ] **Implementar a lógica de entrada e cálculo para "Carro", "Avião" e "Hotel":**
    -   [ ] Definir campos de entrada (Entry, Combobox, etc.) apropriados para cada tipo de despesa.
    -   [ ] Implementar a lógica de cálculo (se houver) para cada nova aba dentro do `controller`, similar à lógica de `atualizar_valor` para despesas.
    -   [ ] Lidar com a persistência dos dados de cada aba através do `database.py`.

### Integração e Testes (Prioridade Média/Baixa)

-   [ ] **Revisar e ajustar interações existentes:**
    -   [ ] Garantir que funcionalidades como "Abrir Viagem" e "Salvar Viagem" no `controller` possam lidar com os dados de todas as abas.
    -   [ ] Considerar como o "Gerar Relatório" pode ser estendido para incluir dados das novas abas.
-   [ ] **Atualizar imports:**
    -   [ ] Garantir que todos os arquivos tenham os imports corretos para as novas classes.
-   [ ] **Testar exaustivamente:**
    -   [ ] Testar a navegação entre as abas.
    -   [ ] Testar a entrada e salvamento de dados em cada nova aba.
    -   [ ] Testar a funcionalidade de "Abrir" e "Salvar" com dados de todas as abas.
