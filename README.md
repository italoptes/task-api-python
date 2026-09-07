# Task API

## 2. Descrição

A Task API é uma aplicação de gerenciamento de tarefas criada para estudo e prática de desenvolvimento de sistemas modernos. O projeto foca em consolidar conceitos como:

- Desenvolvimento de API REST de alta performance
- Arquitetura em camadas (separação de responsabilidades)
- Persistência de dados com PostgreSQL
- Gerenciamento de versionamento de banco com migrations (Alembic)
- Construção de frontend utilizando React
- Integração e comunicação entre frontend e backend através de proxy (Nginx)
- Containerização utilizando Docker e Docker Compose
- Fundamentos estabelecidos para automação futura (ex: n8n)

## 3. Arquitetura

O sistema é dividido em múltiplas camadas que facilitam a manutenção e testabilidade.

A arquitetura macro do sistema funciona da seguinte forma:

```text
Frontend
React + TypeScript + Nginx
        ↓
FastAPI
        ↓
SQLAlchemy
        ↓
PostgreSQL
```

Dentro do **Backend**, a aplicação segue a arquitetura em camadas:

```text
Controller
    ↓
Service
    ↓
Repository
    ↓
Model
    ↓
PostgreSQL
```

- **Controller**: Recebe as requisições HTTP, valida as entradas e envia a resposta (roteamento).
- **Service**: Concentra a regra de negócio e tomada de decisão da aplicação.
- **Repository**: Gerencia a interação direta com o banco de dados (abstração de consultas e persistência).
- **Model**: Representação das entidades do banco de dados utilizando SQLAlchemy.

## 4. Tecnologias

| Tecnologia | Função |
| :--- | :--- |
| **Python** | Linguagem de programação base do backend |
| **FastAPI** | Framework assíncrono para a criação da API REST |
| **SQLAlchemy** | ORM para a comunicação e mapeamento do banco de dados |
| **PostgreSQL** | Banco de dados relacional escolhido para a aplicação |
| **Alembic** | Ferramenta para gerenciar o controle de versão do banco (migrations) |
| **React** | Biblioteca JavaScript/TypeScript para a criação da interface do usuário |
| **TypeScript** | Superset do JavaScript que adiciona tipagem estática (usado no frontend e tipicamente presente com React) |
| **Axios** | Cliente HTTP do frontend para consumir a API REST |
| **Nginx** | Servidor web que serve os arquivos do frontend e atua como proxy reverso |
| **Docker** | Plataforma de containerização que encapsula os serviços |
| **Docker Compose** | Orquestrador para subir o banco, a API e o Frontend de uma vez |

## 5. Funcionalidades

O sistema contém o CRUD completo para gerenciamento de tarefas:

- Criar tarefa
- Listar tarefas
- Buscar tarefa por ID
- Editar tarefa
- Alterar status
- Excluir tarefa

O modelo de tarefa suporta os seguintes status:
- `PENDENTE`
- `EM_ANDAMENTO`
- `CONCLUIDA`

*Toda nova tarefa é criada por padrão com o status PENDENTE.*

## 6. Estrutura do projeto

A estrutura principal do projeto é organizada assim:

```text
.
├── app/
│   ├── controllers/    # Controladores das rotas HTTP
│   ├── database/       # Configuração de conexão do banco e session (SQLAlchemy)
│   ├── exceptions/     # Exceções customizadas e mapeamento de tratamento de erro
│   ├── models/         # Entidades de persistência SQLAlchemy
│   ├── repositories/   # Classes para interagir com os dados no banco
│   ├── schemas/        # Tipagens Pydantic (validação de I/O)
│   └── services/       # Lógica e regras de negócio
├── migrations/         # Arquivos de versionamento do banco gerados pelo Alembic
├── frontend/           # Aplicação web React, Vite, TS, e config Nginx
├── docker-compose.yml  # Configuração dos serviços e containers Docker
├── Dockerfile          # Definição do container base do backend
├── requirements.txt    # Dependências do Python/Backend
└── alembic.ini         # Configuração base do Alembic
```

## 7. API

Abaixo encontram-se os endpoints expostos pela API REST do projeto.

### `POST /tarefas`
- **Objetivo**: Criar uma nova tarefa.
- **Body**: `{ "titulo": "string", "descricao": "string" }`
- **Resposta**: Objeto com a tarefa criada (incluindo `id` e `status: "PENDENTE"`).
- **Código HTTP**: 201 Created (ou 200 OK dependendo da configuração padrão do repositório).

### `GET /tarefas`
- **Objetivo**: Listar todas as tarefas cadastradas.
- **Resposta**: Lista contendo todas as tarefas.
- **Código HTTP**: 200 OK.

### `GET /tarefas/{id}`
- **Objetivo**: Recuperar os dados de uma tarefa específica.
- **Resposta**: Objeto da tarefa com o ID referenciado.
- **Código HTTP**: 200 OK.

### `PUT /tarefas/{id}`
- **Objetivo**: Atualizar o título e a descrição de uma tarefa inteiramente.
- **Body**: `{ "titulo": "string", "descricao": "string" }`
- **Resposta**: Objeto da tarefa atualizado.
- **Código HTTP**: 200 OK.

### `PATCH /tarefas/{id}/status`
- **Objetivo**: Alterar o status da tarefa para PENDENTE, EM_ANDAMENTO ou CONCLUIDA.
- **Body**: `{ "status": "string" }`
- **Resposta**: Objeto da tarefa com o status alterado.
- **Código HTTP**: 200 OK.

### `DELETE /tarefas/{id}`
- **Objetivo**: Apagar permanentemente a tarefa.
- **Resposta**: Vazio.
- **Código HTTP**: 204 No Content.

## 8. Exemplos de requisição

**Criar tarefa:**
```json
{
  "titulo": "Minha tarefa",
  "descricao": "Descrição da tarefa"
}
```

**Atualizar tarefa:**
```json
{
  "titulo": "Título atualizado",
  "descricao": "Descrição atualizada"
}
```

**Alterar status:**
```json
{
  "status": "EM_ANDAMENTO"
}
```

## 9. Tratamento de erros

Operações envolvendo um `{id}` que não existe no banco de dados levantam exceções mapeadas nativamente pelo framework.

Quando uma tarefa não é encontrada, a API retorna o status **HTTP 404** com o seguinte corpo:
```json
{
  "detail": "Tarefa não encontrada"
}
```

## 10. Banco de dados e Alembic

A persistência do sistema é baseada em:
- O banco relacional **PostgreSQL**, hospedado em um container independente.
- **SQLAlchemy** agindo como ORM para gerenciar o mapeamento e as queries.
- **Alembic**, que é responsável pelas *migrations* – permitindo rastrear o histórico das tabelas e a evolução estrutural do banco.

Para executar o upgrade nas migrations diretamente no Docker, utilize:
```bash
docker compose exec backend alembic upgrade head
```
*Esse comando instrui o Alembic (rodando dentro do container backend) a aplicar qualquer mudança pendente na estrutura de dados do Postgres e atualizá-la para a versão mais recente (`head`).*

## 11. Docker

A aplicação está inteiramente containerizada. No orquestrador `docker-compose.yml`, encontram-se três serviços fundamentais:

- `postgres`: Banco de dados relacional.
- `backend`: Aplicação FastAPI servida na porta 8000.
- `frontend`: Container Nginx servindo o site em React na porta 3000 e funcionando como gateway para o backend.

Para construir a imagem e subir os serviços, execute:
```bash
docker compose up --build
```
*(Você pode usar `docker compose up -d --build` para subir em modo silencioso).*

Para verificar se os contêineres iniciaram e o status das portas mapeadas, execute:
```bash
docker compose ps
```

## 12. Acessar a aplicação

Após levantar os containers com o Docker Compose, as interfaces podem ser acessadas nas URLs:

- **Frontend**: http://localhost:3000
- **Backend (Diretamente)**: http://localhost:8000
- **Swagger (Documentação interativa da API)**: http://localhost:8000/docs

## 13. Desenvolvimento local

A forma principal e oficial de rodar a aplicação para desenvolvimento é através do Docker Compose, visto que ele orquestra perfeitamente a rede interna e evita problemas com falta de dependências e configuração de portas. Basta utilizar `docker compose up --build`.

## 14. Frontend

O frontend é implementado em **React** com **TypeScript** e usa o **Axios** para consumo de dados.
Ele está encapsulado num container que tem o **Nginx** operando tanto como servidor de recursos estáticos quanto como *proxy reverso*.

Isso permite um fluxo fluido de requisições de frontend onde o navegador nem sequer acessa o backend diretamente:

```text
React
 ↓ (via fetch Axios p/ '/api/tarefas')
Nginx
 ↓ (Proxy Pass)
FastAPI
 ↓
PostgreSQL
```

## 15. Alembic

A arquitetura do banco assume que as modificações e a criação de tabelas aconteçam exclusivamente pelo Alembic, em detrimento do uso inseguro e implícito do `.create_all()`.

Quando criar uma nova versão, e desejar aplicar ao banco real:
```bash
docker compose exec backend alembic upgrade head
```
*Se houver necessidade de gerar um novo mapeamento a partir do SQLAlchemy no ambiente dev:*
```bash
docker compose exec backend alembic revision --autogenerate -m "nome_da_migracao"
```

## 16. Fluxo geral da aplicação

Quando um usuário decide criar uma tarefa na interface visual, a cadeia de eventos ocorre de forma sequencial, conforme o esquema:

```text
Usuário
 ↓
React (App.tsx / Axios)
 ↓
Nginx (/api -> backend:8000)
 ↓
FastAPI Controller
 ↓
Service (Validações de negócio)
 ↓
Repository (Tradução para SQL)
 ↓
SQLAlchemy
 ↓
PostgreSQL
```
O usuário preenche um formulário no React; o Axios despacha os dados JSON para a porta do Nginx local que atua como proxy reverso. O Nginx por sua vez reencaminha essa chamada para a camada de Controladores do FastAPI, que transita pelo Service até o Repository persistir no banco de dados.

