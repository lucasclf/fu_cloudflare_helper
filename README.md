# Fabula Helper Importer

Aplicação Python responsável por popular a API do projeto **Fabula Ultima Helper** a partir de arquivos JSON locais.

O importador lê arquivos de definição presentes na pasta `jsons/`, envia os dados para os endpoints administrativos da API e resolve automaticamente dependências entre entidades, como classes, personagens, facções, monstros, NPCs, itens, magias e vínculos.

A aplicação também exibe barras de progresso durante a importação e gera um relatório JSON ao final de cada execução, informando quantos registros foram criados, quantos já existiam e quais erros ocorreram.

---

## Tecnologias utilizadas

- Python 3.11+
- Requests
- python-dotenv
- Dataclasses
- Argparse
- Logging

---

## Estrutura do projeto

```txt
fabula_helper/
  main.py
  config.py
  http_client.py

  api_result.py
  console_progress.py
  constants.py
  import_context.py
  import_context_factory.py
  import_pipeline.py
  import_report.py
  import_step.py
  import_targets.py
  json_loader.py
  request_definitions.py
  request_groups.py

  services/
    __init__.py
    batch_import_service.py
    faction_import_service.py
    job_import_service.py
    monster_import_service.py
    npc_import_service.py
    pc_import_service.py

  normalizers/
    __init__.py
    common.py
    faction_normalizer.py
    job_normalizer.py
    monster_normalizer.py
    npc_normalizer.py
    pc_normalizer.py

  jsons/
    *.json

  reports/
    import-report-*.json
```

---

## Como funciona

O fluxo geral da aplicação é:

```txt
JSON local
  ↓
json_loader
  ↓
normalizer
  ↓
BatchImportService
  ↓
ApiClient
  ↓
API administrativa
  ↓
ImportBatchReport
  ↓
ImportRunReport
  ↓
reports/import-report-*.json
```

Os arquivos JSON são escritos de forma amigável para humanos, usando nomes em vez de IDs.

Exemplo de entrada:

```json
{
  "pc_id": "Kafra",
  "item_id": "Poção"
}
```

Durante a importação, os normalizers consultam os endpoints públicos e convertem nomes para IDs:

```json
{
  "pc_id": 1,
  "item_id": 27
}
```

---

## Responsabilidades dos principais arquivos

### `main.py`

Ponto de entrada da aplicação.

Responsável por:

- ler argumentos da linha de comando;
- configurar logs;
- carregar configurações;
- criar o contexto de importação;
- executar o pipeline.

### `config.py`

Carrega variáveis de ambiente e cria o objeto `Settings`.

Variáveis esperadas:

```env
API_BASE_URL=http://127.0.0.1:8787
TOKEN=seu_token_admin
```

### `http_client.py`

Cliente HTTP usado para comunicação com a API.

Responsável por:

- fazer `POST` autenticado nos endpoints administrativos;
- fazer `GET` nos endpoints públicos;
- interpretar status HTTP;
- retornar o resultado da criação para o serviço de batch.

Regras do `POST`:

| Status | Significado |
|---|---|
| `200`, `201`, `204` | Registro criado/processado com sucesso |
| `409` | Registro já existia |
| Outros status | Erro real |
| Timeout/conexão | Erro real |

### `services/`

Camada de orquestração da importação.

| Service | Responsabilidade |
|---|---|
| `BatchImportService` | Importação em lote, barra de progresso e relatório por lote |
| `JobImportService` | Classes, perguntas, aliases, poderes e magias |
| `MonsterImportService` | Monstros, traits, afinidades e ações |
| `NpcImportService` | NPCs, regras especiais, inventário e equipamento |
| `PcImportService` | Personagens, inventário, equipamento, classes, poderes, magias, arcanas e vínculos |
| `FactionImportService` | Facções e relações com localidades |

### `normalizers/`

Camada responsável por transformar nomes em IDs.

Exemplos:

| Entrada | Saída |
|---|---|
| `"job_id": "Arcanista"` | `"job_id": 3` |
| `"pc_id": "Kafra"` | `"pc_id": 1` |
| `"item_id": "Vestes de Sábio"` | `"item_id": 27` |
| `"target_type": "npc", "target_id": "Fulano"` | `"target_id": 5` |

### `import_pipeline.py`

Controla a ordem de execução das etapas de importação e gera o relatório final.

Etapas disponíveis:

| Target | Descrição |
|---|---|
| `all` | Executa todas as etapas |
| `sessions` | Importa sessões |
| `arcanas` | Importa arcanas |
| `locations` | Importa localidades |
| `factions` | Importa facções |
| `items` | Importa armas, armaduras, escudos, acessórios e artefatos |
| `jobs` | Importa classes e dependências |
| `monsters` | Importa monstros e dependências |
| `npcs` | Importa NPCs e dependências |
| `pcs` | Importa personagens e dependências |

---

## Preparando o ambiente

### 1. Criar ambiente virtual

```bash
python -m venv .venv
```

### 2. Ativar ambiente virtual

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Windows CMD:

```bash
.venv\Scripts\activate.bat
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

Caso ainda não exista um `requirements.txt`, crie com:

```txt
requests
python-dotenv
```

Ou gere a partir do ambiente atual:

```bash
pip freeze > requirements.txt
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
API_BASE_URL=http://127.0.0.1:8787
TOKEN=seu_token_admin
```

### Variáveis

| Variável | Obrigatória | Descrição |
|---|---|---|
| `API_BASE_URL` | Sim | URL base da API |
| `TOKEN` | Sim para rotas administrativas | Token usado nas rotas administrativas |

Exemplo com Cloudflare Workers local:

```env
API_BASE_URL=http://127.0.0.1:8787
TOKEN=meu-token-local
```

Também é recomendado criar um `.env.example` versionado:

```env
API_BASE_URL=http://127.0.0.1:8787
TOKEN=change-me
```

---

## Como executar

### Executar tudo

```bash
python main.py
```

Ou explicitamente:

```bash
python main.py --only all
```

### Executar apenas um grupo

```bash
python main.py --only jobs
```

```bash
python main.py --only monsters
```

```bash
python main.py --only npcs
```

```bash
python main.py --only pcs
```

```bash
python main.py --only factions
```

### Listar targets disponíveis

```bash
python main.py --list-targets
```

Exemplo de saída:

```txt
Targets disponíveis:

all
  Executa todas as etapas de importação.

sessions
  Importa sessões.

arcanas
  Importa arcanas.

locations
  Importa localidades.

factions
  Importa facções e suas relações com localidades.

items
  Importa armas, armaduras, escudos, acessórios e artefatos.

jobs
  Importa classes, perguntas, aliases, poderes e magias.

monsters
  Importa monstros, traits, afinidades e ações.

npcs
  Importa NPCs, regras especiais, inventário e equipamento.

pcs
  Importa personagens, inventário, equipamento, classes, poderes, magias, magias de monstro, arcanas e vínculos.
```

### Executar com logs detalhados

```bash
python main.py --only pcs --debug
```

---

## Relatórios de importação

Ao final de cada execução, a aplicação gera um relatório JSON na pasta:

```txt
reports/
```

Formato do arquivo:

```txt
reports/import-report-YYYYMMDD-HHMMSS.json
```

Exemplo:

```txt
reports/import-report-20260514-110457.json
```

O relatório contém:

- data/hora de início;
- data/hora de fim;
- target executado;
- etapas processadas;
- total de registros;
- registros criados;
- registros que já existiam;
- erros encontrados.

Exemplo simplificado:

```json
{
  "started_at": "2026-05-14T10:58:05",
  "finished_at": "2026-05-14T11:04:57",
  "only": "all",
  "steps": [
    {
      "target": "jobs",
      "label": "jobs",
      "batches": [
        {
          "label": "jobs",
          "path": "admin/jobs",
          "total": 16,
          "created": 16,
          "already_exists": 0,
          "errors": []
        }
      ]
    }
  ],
  "summary": {
    "created": 16,
    "already_exists": 0,
    "errors": 0
  }
}
```

---

## Barra de progresso

Durante a importação, a aplicação exibe uma barra de progresso por lote.

Exemplo:

```txt
[██████████████████████████████] 16/16 jobs
[██████████████████████████████] 64/64 job questions
[██████████████████████████████] 48/48 job aliases
```

Ao final da etapa, o pipeline exibe o resumo:

```txt
Etapa finalizada: jobs | criados=128 | já existiam=0 | erros=0
```

---

## Ordem de importação

Quando executado com:

```bash
python main.py --only all
```

A ordem é:

```txt
sessions
arcanas
locations
factions
items
jobs
monsters
npcs
pcs
```

Essa ordem é importante porque algumas entidades dependem de outras.

Exemplos:

- facções dependem de localidades;
- personagens dependem de itens, classes, magias, arcanas, NPCs e monstros;
- NPCs dependem de itens;
- poderes e magias de personagens dependem de dados previamente cadastrados.

---

## Comportamento com registros duplicados

A aplicação trata HTTP `409 Conflict` como registro já existente.

Isso permite rodar o importador mais de uma vez sem quebrar o processo.

Exemplo:

```json
{
  "created": 0,
  "already_exists": 16,
  "errors": 0
}
```

Isso significa que os registros já estavam cadastrados.

---

## Tratamento de erros

A aplicação diferencia:

| Caso | Tratamento |
|---|---|
| `200`, `201`, `204` | Conta como criado/processado |
| `409` | Conta como já existente |
| Outros status HTTP | Conta como erro |
| Falha de conexão/timeout | Conta como erro |

Erros reais são registrados no relatório JSON.

Exemplo:

```json
"errors": [
  {
    "identifier": "Fulgur",
    "status_code": 500,
    "message": "Falha ao importar Fulgur: 500 - Internal Server Error"
  }
]
```

---

## Arquivos JSON

Os arquivos de entrada ficam na pasta:

```txt
jsons/
```

Eles são definidos em:

```txt
request_definitions.py
```

E agrupados em:

```txt
request_groups.py
```

Exemplo de definição:

```python
JOB = ImportDefinition(
    path="admin/jobs",
    json_file="./jsons/jobs_request.json",
    identifier="name",
)
```

---

## Boas práticas para adicionar novos imports

Ao adicionar uma nova entidade:

1. Crie o arquivo JSON em `jsons/`.
2. Adicione uma `ImportDefinition` em `request_definitions.py`.
3. Adicione a definition em um grupo de `request_groups.py`.
4. Crie ou atualize um normalizer, se houver dependências por nome.
5. Crie ou atualize um service.
6. Registre a etapa no `ImportPipeline`, se for um novo target.
7. Rode com `--only nome-do-target`.
8. Verifique o relatório em `reports/`.

---

## Problemas comuns

### `API_BASE_URL` não configurada

Erro:

```txt
Variável de ambiente API_BASE_URL não configurada.
```

Solução:

Crie ou ajuste o arquivo `.env`:

```env
API_BASE_URL=http://127.0.0.1:8787
```

### Token não configurado

Erro:

```txt
TOKEN não configurado para chamada autenticada.
```

Solução:

Adicione no `.env`:

```env
TOKEN=seu_token_admin
```

### Entidade não encontrada no mapa

Exemplo:

```txt
Item não encontrado no mapa de IDs.
Campo: item_id
Valor procurado: Genocidio
```

Isso significa que o JSON está referenciando um nome que não existe no retorno da API pública.

Verifique:

- se a entidade foi importada antes;
- se o nome no JSON está escrito exatamente igual;
- se há diferença de acento, maiúsculas/minúsculas ou espaços.

### Registro já existe

Se o relatório mostrar:

```json
{
  "already_exists": 10
}
```

Isso normalmente não é erro.

Significa que a API retornou `409 Conflict` e o importador seguiu normalmente.

---

## Recomendações

Antes de rodar:

```bash
python main.py --only pcs
```

garanta que já foram importados:

```txt
items
jobs
monsters
npcs
arcanas
```

Ou execute:

```bash
python main.py --only all
```

---

## Licença

```txt
Este projeto está licenciado sob a licença MIT.
```
#   f u _ c l o u d f l a r e _ h e l p e r  
 