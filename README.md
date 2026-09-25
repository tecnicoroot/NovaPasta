# Organização de Projeto Python

> Guia prático para estruturar um projeto Python moderno, desde a criação do ambiente até qualidade de código, testes, Git, CI e documentação.

---

## Visão geral

A proposta é começar com uma base simples e evoluir o projeto conforme a necessidade.

A stack inicial será:

- **Python 3.13+**
- **uv** — ambiente virtual + gerenciamento de dependências
- **Ruff** — lint + formatter
- **mypy** — type checking
- **pytest** — testes
- **pytest-cov** — cobertura de testes
- **pre-commit** — validações automáticas antes do commit
- **Git** — controle de versão
- **pyproject.toml** — configuração central do projeto

A ideia principal é:

```text
Ambiente
   ↓
Estrutura
   ↓
Código
   ↓
Qualidade
   ↓
Testes
   ↓
Git
   ↓
Automação
   ↓
CI
   ↓
Documentação
```

Não precisamos configurar tudo de uma vez. A configuração deve acompanhar a evolução do projeto.

---

# Parte 1 — Ambiente

## Etapa 1 — verificar o que já está instalado

Inicialmente, vamos assumir:

- Windows
- PowerShell
- VS Code
- Git
- Python

Abra o PowerShell:

```powershell
python --version
git --version
code --version
uv --version
```

Se algum comando não funcionar, não instale tudo novamente automaticamente. Primeiro identifique qual ferramenta está faltando.

---

## Etapa 2 — instalar o uv

Se:

```powershell
uv --version
```

não funcionar, no PowerShell podemos instalar o `uv`:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Feche e abra novamente o PowerShell e teste:

```powershell
uv --version
```

---

# Parte 2 — Criar o projeto

## Etapa 3 — criar o projeto

Escolha uma pasta para seus projetos:

```powershell
cd C:\Projetos
```

Crie o projeto:

```powershell
uv init --package meu-projeto
```

Entre nele:

```powershell
cd meu-projeto
```

A estrutura inicial será semelhante a:

```text
meu-projeto/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── src/
    └── meu_projeto/
        └── __init__.py
```

## Por que usar `src/`?

A pasta `src/` separa o código da aplicação dos arquivos de configuração, documentação e testes.

Isso ajuda a evitar que testes funcionem por acidente apenas porque o diretório raiz do projeto está no caminho de importação.

---

## Etapa 4 — criar o ambiente virtual

Execute:

```powershell
uv sync
```

O `uv` criará:

```text
.venv/
```

O `.venv` não deve ser versionado no Git.

O `.gitignore` criado pelo `uv` normalmente já cuida disso.

---

# Parte 3 — Dependências e pyproject.toml

## Etapa 5 — entender dependências

Dependências de execução:

```powershell
uv add pacote
```

Dependências usadas apenas durante desenvolvimento:

```powershell
uv add --dev pacote
```

Por exemplo:

```powershell
uv add --dev ruff mypy pytest pytest-cov pre-commit
```

Para remover:

```powershell
uv remove pacote
```

Para sincronizar:

```powershell
uv sync
```

Para visualizar a árvore:

```powershell
uv tree
```

A relação entre os principais arquivos é:

```text
pyproject.toml
       ↓
declara dependências e configurações

uv.lock
       ↓
registra as versões resolvidas

.venv/
       ↓
ambiente usado para executar o projeto
```

O `uv.lock` deve ser versionado no Git.

---

## Etapa 6 — configurar o pyproject.toml

Uma configuração inicial pode ser:

```toml
[project]
name = "meu-projeto"
version = "0.1.0"
description = "Meu projeto Python"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []

[dependency-groups]
dev = [
    "mypy>=1.0",
    "pre-commit>=4.0",
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.0",
]

[tool.ruff]
line-length = 88
target-version = "py313"

[tool.ruff.lint]
select = [
    "E",
    "F",
    "I",
    "B",
    "UP",
    "SIM",
]

[tool.ruff.format]
quote-style = "double"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.mypy]
python_version = "3.13"
```

### Sobre as configurações do Ruff

Os grupos selecionados representam categorias diferentes:

```text
E   pycodestyle
F   Pyflakes
I   isort
B   flake8-bugbear
UP  pyupgrade
SIM flake8-simplify
```

O Ruff pode atuar em duas funções principais:

```text
ruff check
    ↓
lint

ruff format
    ↓
formatter
```

---

# Parte 4 — Qualidade de código

## Etapa 7 — testar o Ruff

Crie:

```text
src/meu_projeto/main.py
```

Com:

```python
def hello(name: str) -> str:
    return f"Hello, {name}!"
```

Execute:

```powershell
uv run ruff check .
```

Depois:

```powershell
uv run ruff format .
```

Para verificar a formatação sem alterar arquivos:

```powershell
uv run ruff format --check .
```

---

## Etapa 8 — configurar o mypy

Inicialmente podemos usar:

```toml
[tool.mypy]
python_version = "3.13"
```

Execute:

```powershell
uv run mypy src
```

Depois que o projeto estiver confortável com type hints, podemos evoluir para:

```toml
[tool.mypy]
python_version = "3.13"
strict = true
```

A opção `strict` aumenta bastante a quantidade de verificações. Por isso, é interessante adotá-la conscientemente.

---

# Parte 5 — Testes

## Etapa 9 — criar os primeiros testes

Crie:

```text
tests/
└── unit/
    └── test_main.py
```

Com:

```python
from meu_projeto.main import hello


def test_hello():
    assert hello("David") == "Hello, David!"
```

Execute:

```powershell
uv run pytest
```

Conforme o projeto crescer:

```text
tests/
├── unit/
│   ├── test_main.py
│   ├── test_xml_reader.py
│   └── test_validator.py
│
└── integration/
    └── test_xml_validation.py
```

Além de testes unitários e de integração, podemos estudar:

- fixtures;
- parametrização;
- mocks;
- testes de exceções;
- cobertura.

---

# Parte 6 — Estrutura e arquitetura

Não devemos criar dezenas de pastas apenas porque parecem profissionais.

A arquitetura deve evoluir conforme o código exige.

Uma aplicação maior pode chegar a algo semelhante a:

```text
meu-projeto/
│
├── src/
│   └── meu_projeto/
│       ├── __init__.py
│       ├── main.py
│       ├── domain/
│       ├── services/
│       ├── repositories/
│       ├── models/
│       └── utils/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── docs/
│
├── .github/
│   └── workflows/
│
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── README.md
├── pyproject.toml
└── uv.lock
```

### Regra importante

Não crie camadas apenas para "parecer arquitetura".

Crie uma nova camada quando houver uma necessidade real.

---

# Parte 7 — Git

## Etapa 10 — configurar o Git

Inicialize:

```powershell
git init
```

Configure seu usuário:

```powershell
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

Verifique:

```powershell
git status
```

Faça o primeiro commit:

```powershell
git add .
git commit -m "chore: initial project setup"
```

---

# Parte 8 — Conventional Commits

Formato básico:

```text
tipo: descrição
```

Exemplo:

```text
feat: adiciona validação do XML TISS
```

Principais tipos:

| Tipo | Significado | Quando usar |
|---|---|---|
| `feat` | Feature | Nova funcionalidade |
| `fix` | Fix | Correção de bug |
| `refactor` | Refatoração | Mudança interna sem alterar comportamento |
| `test` | Testes | Adição ou alteração de testes |
| `docs` | Documentação | README/documentação |
| `style` | Estilo | Formatação sem mudança de lógica |
| `chore` | Manutenção | Tarefas técnicas/manutenção |
| `build` | Build | Build/dependências |
| `ci` | Continuous Integration | Pipelines/automação |
| `perf` | Performance | Melhoria de desempenho |
| `revert` | Reversão | Desfaz um commit anterior |

Exemplos:

```text
feat: adiciona validação de estrutura do XML TISS
fix: corrige validação do código do procedimento
test: adiciona testes para validação de beneficiário
refactor: separa regras de validação do parser XML
docs: atualiza instruções de instalação
chore: configura ruff e mypy
ci: adiciona pipeline de testes
```

## Escopo

Quando for útil:

```text
tipo(escopo): descrição
```

Exemplos:

```text
feat(xml): adiciona parser do XML TISS
fix(validation): corrige validação de procedimento
test(xml): adiciona testes do parser
refactor(domain): reorganiza regras de negócio
```

Para o `validador_tiss`, escopos possíveis incluem:

```text
xml
validation
api
database
test
docs
ci
```

## Breaking changes

Uma alteração incompatível pode ser indicada com `!`:

```text
feat!: altera formato da resposta da validação
```

Ou:

```text
feat(api): altera contrato da resposta

BREAKING CHANGE: o campo `errors` agora é retornado como lista.
```

Evite commits como:

```text
alterações
mudanças
ajustes
corrige coisas
implementação
```

Prefira:

```text
fix(validation): corrige validação do campo registro_ans
```

---

# Parte 9 — Pre-commit

## Etapa 11 — configurar o pre-commit

Crie:

```text
.pre-commit-config.yaml
```

Uma configuração inicial:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.0
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format
```

Instale:

```powershell
uv run pre-commit install
```

Teste:

```powershell
uv run pre-commit run --all-files
```

Uma estratégia equilibrada é deixar verificações rápidas no commit:

```text
pre-commit
    ↓
Ruff
    ↓
format
```

e verificações mais completas na CI:

```text
CI
 ├── Ruff
 ├── mypy
 ├── pytest
 └── coverage
```

---

# Parte 10 — CI

## Etapa 12 — automatizar a qualidade

Depois que tudo funcionar localmente:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

podemos automatizar na CI.

Fluxo:

```text
git push
    ↓
GitHub Actions
    ↓
uv sync
    ↓
ruff check
    ↓
ruff format --check
    ↓
mypy
    ↓
pytest
    ↓
coverage
```

Estrutura:

```text
.github/
└── workflows/
    └── ci.yml
```

Primeiro fazemos os comandos funcionarem localmente. Depois automatizamos exatamente esses mesmos comandos.

---

# Parte 11 — Documentação

## Etapa 13 — README

Uma estrutura possível:

```markdown
# Meu Projeto

## Descrição

## Requisitos

## Instalação

## Configuração

## Execução

## Testes

## Qualidade

## Estrutura

## Contribuição

## Licença
```

O README deve permitir que outra pessoa entenda rapidamente o projeto e consiga executá-lo.

---

# Parte 12 — Resultado final

Uma estrutura inicial:

```text
meu-projeto/
│
├── .git/
├── .venv/
│
├── src/
│   └── meu_projeto/
│       ├── __init__.py
│       └── main.py
│
├── tests/
│   └── unit/
│       └── test_main.py
│
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── README.md
├── pyproject.toml
└── uv.lock
```

Com a evolução:

```text
meu-projeto/
│
├── src/
│   └── meu_projeto/
│       ├── domain/
│       ├── services/
│       ├── repositories/
│       ├── models/
│       └── main.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── docs/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .pre-commit-config.yaml
├── README.md
├── pyproject.toml
└── uv.lock
```

---

# Fluxo recomendado

```text
1. Criar/alterar código
        ↓
2. Escrever/atualizar testes
        ↓
3. uv run ruff check .
        ↓
4. uv run ruff format .
        ↓
5. uv run mypy src
        ↓
6. uv run pytest
        ↓
7. git status
        ↓
8. git add
        ↓
9. git commit
        ↓
10. pre-commit
        ↓
11. git push
        ↓
12. CI
```

---

# Princípios

## 1. Comece simples

Não crie complexidade antes de precisar dela.

## 2. Automatize tarefas repetitivas

Ruff, mypy, pytest, pre-commit e CI reduzem trabalho manual.

## 3. Teste comportamento

Os testes devem proteger o comportamento esperado do sistema.

## 4. Tipagem deve ajudar

Type hints devem tornar o código mais claro e seguro.

## 5. Commits devem contar uma história

Ao olhar:

```powershell
git log
```

deve ser possível entender como o projeto evoluiu.

## 6. A arquitetura deve evoluir com o projeto

Uma aplicação pequena não precisa ter a mesma estrutura de uma aplicação grande.

## 7. O pyproject.toml é o centro da configuração

Sempre que possível, mantenha nele as configurações relacionadas ao projeto.

---

# Próximo passo

A sequência recomendada é:

```text
Python + Git
      ↓
uv
      ↓
projeto
      ↓
src/
      ↓
pyproject.toml
      ↓
Ruff
      ↓
mypy
      ↓
pytest
      ↓
Git
      ↓
Conventional Commits
      ↓
pre-commit
      ↓
CI
      ↓
documentação
      ↓
arquitetura conforme necessidade
```

A partir daí, o projeto terá uma base sólida para crescer sem introduzir complexidade desnecessária.
