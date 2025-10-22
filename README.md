# 🏗️ Documentação do Backend — Plataforma de Ensino de Tecnologia
## 📘 Introdução

Este documento descreve a arquitetura do backend da plataforma de ensino gratuita voltada à área de tecnologia.
O objetivo do sistema é democratizar o ensino de tecnologia e oferecer uma ferramenta de apoio para escolas, permitindo que professores cadastrem cursos gratuitamente e que alunos possam acessá-los de forma simples.

O backend foi projetado com foco em organização, clareza e baixo custo operacional, adequando-se ao contexto de um projeto de extensão universitária e à entrega de um MVP funcional até novembro.

Esta documentação serve tanto como guia técnico quanto como material de aprendizado para todos os integrantes da equipe.

## 🎯 Objetivos do Backend

Disponibilizar uma API REST organizada, escalável e de fácil manutenção.

Permitir autenticação de usuários (alunos e professores).

Suportar criação e gerenciamento de cursos e quizzes.

Oferecer endpoints para o player de vídeo.

Garantir segurança básica e tratamento consistente de erros.

Ser simples o suficiente para implantação em servidores de baixo custo.

## 🗂️ Estrutura de Pastas e Arquivos

Abaixo está o modelo de organização do projeto (exemplo para FastAPI):
```
backend/
│
├── app/
│   ├── main.py                     # Ponto de entrada da aplicação
│   ├── core/                       # Configurações e infraestrutura
│   │   ├── config.py               # Variáveis de ambiente e setup
│   │   ├── database.py             # Conexão com o banco de dados
│   │   ├── security.py             # Autenticação e JWT
│   │   └── exceptions.py           # Tratamento centralizado de erros
│   │
│   ├── models/                     # Modelos do banco (SQLAlchemy)
│   │   ├── user_model.py
│   │   ├── course_model.py
│   │   └── quiz_model.py
│   │
│   ├── schemas/                    # Validação e contratos da API (Pydantic)
│   │   ├── user_schema.py
│   │   ├── course_schema.py
│   │   └── quiz_schema.py
│   │
│   ├── repositories/               # Acesso a dados (CRUD)
│   │   ├── user_repository.py
│   │   ├── course_repository.py
│   │   └── quiz_repository.py
│   │
│   ├── services/                   # Regras de negócio
│   │   ├── user_service.py
│   │   ├── course_service.py
│   │   └── quiz_service.py
│   │
│   ├── routers/                    # Endpoints da API
│   │   ├── user_router.py
│   │   ├── course_router.py
│   │   └── quiz_router.py
│   │
│   ├── tests/                      # Testes unitários e de integração
│   │   ├── test_users.py
│   │   ├── test_courses.py
│   │   └── test_quizzes.py
│   │
│   └── utils/                      # Funções auxiliares
│       ├── file_utils.py
│       ├── video_utils.py
│       └── response_utils.py
│
├── requirements.txt                # Dependências do projeto
├── .env.example                    # Modelo de variáveis de ambiente
├── README_BACKEND.md               # Este documento
└── Dockerfile                      # (Opcional) Configuração de container
```

## 🔐 Autenticação e Segurança

    Autenticação via JWT (JSON Web Token)

    Alunos e professores autenticam-se com e-mail e senha.

    Tokens são gerados e verificados em core/security.py.

    Rotas protegidas usam Depends(get_current_user).

    Boas práticas adotadas:

    Senhas armazenadas com hash (bcrypt).

    Variáveis sensíveis no .env (ex: SECRET_KEY, DATABASE_URL).

    Middleware de CORS para permitir o frontend React.

    Tratamento centralizado de exceções no exceptions.py.


## 🌱 Como Contribuir com o Projeto
1. Crie um ambiente virtual
```bash
python -m venv venv
```

2. Instale as dependências
```
pip install -r requirements.txt
```

3. Configure o ambiente

    - Crie um arquivo ```.env``` a partir do modelo:



4. Rode o servidor local

    ```
    uvicorn app.main:app --reload
    ```

5. Acesse a documentação interativa
    http://localhost:8000/docs

6. Padrões de código e commits

    - Nome de branch: ```feature/nome-funcionalidade``` ou ```fix/descricao-breve```

    - Commits curtos e descritivos:

        ```vbnet
        feat: adicionar endpoint de criação de curso
        fix: corrigir validação do email do usuário
        ```
