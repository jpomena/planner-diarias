# Lista de Tarefas - Planner de Diárias

### Refatoração Crítica (Prioridade Alta)
- [ ] **Corrigir `traces` em `src/configs_window.py`:**
  - [ ] Unificar `CriarEntrysCapitais` e `CriarEntrysOutras` em um único método `CriarEntrysPercentuais(self, tipo_localidade, column)`.
  - [ ] Unificar `ValidarPctCapitais` e `ValidarPctOutras` em `ValidarPct(...)`.
  - [ ] Implementar a lógica correta de `trace_id` para cada `StringVar`, armazenando o ID na instância `self` (`setattr`) e usando-o para remover (`trace_remove`) o trace antes de cada atualização e recriá-lo depois.

- [ ] **Corrigir bug em `src/controller.py`:**
  - [ ] No método `MostrarLocalidade`, a linha `tipo_var_str = widgets_linha["tipo_var"]` está incorreta. Corrigir para `tipo_var_str = widgets_linha["tipo_var"].get()` para obter o valor da `StringVar`.

### Melhorias e Qualidade do Código (Prioridade Média)
- [ ] **Refatorar `src/viagens_window.py`:**
  - [ ] Unificar as classes `AbrirWindow` e `ApagarWindow` para reduzir a duplicação de código. Elas compartilham a mesma interface. Pode-se criar uma classe base ou uma única classe que aceite o tipo de ação ("abrir" ou "apagar") como parâmetro.

- [ ] **Refatorar `src/report_window.py`:**
  - [ ] No método `PreencherTabelaTotais`, a lógica de somar os totais é muito manual com `if/elif`. Considere usar um dicionário para acumular os valores, o que tornaria o código mais limpo e fácil de manter se novos tipos de despesa forem adicionados.

### Limpeza
- [ ] **Remover arquivos temporários:**
  - [ ] Apagar o arquivo `filter-script.py`, que foi usado apenas para corrigir o problema do Git.
- [ ] **Adicionar Docstrings:**
  - [ ] Adicionar docstrings aos métodos mais complexos para explicar sua função, especialmente em `controller.py`, `configs_window.py` e `database.py`.
