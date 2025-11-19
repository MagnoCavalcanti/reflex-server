# 📚 Documentação da API - Reflex Server

## 🌐 Base URL
```
http://localhost:8000
```

## 📖 Swagger/OpenAPI
```
http://localhost:8000/docs
```

---

## 🔐 Autenticação

### **POST** `/auth/register`

Registra um novo usuário no sistema.

**Request Body:**
```json
{
  "username": "joao123",
  "password": "Senha123",
  "email": "joao@example.com",
  "fullname": "João Silva",
  "telephone": "(11) 98765-4321",
  "type_user": "A"
}
```

**Campos:**
- `username` (string, obrigatório): Nome de usuário único
- `password` (string, obrigatório): Mínimo 8 caracteres, deve conter 1 maiúscula, 1 minúscula e 1 número
- `email` (string, obrigatório): Email válido (usuario@dominio.com)
- `fullname` (string, obrigatório): Nome completo
- `telephone` (string, obrigatório): Formato (XX) XXXXX-XXXX
- `type_user` (string, obrigatório): "A" (Aluno) ou "P" (Professor)

**Response (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**
- `422`: Dados inválidos (senha fraca, email inválido, telefone formato errado)
- `400`: Usuário já existe

---

### **POST** `/auth/login`

Autentica usuário e retorna tokens de acesso.

**Request Body (form-data):**
```
username: joao123
password: Senha123
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Possíveis Erros:**
- `401`: Credenciais inválidas

**Como usar o token:**
```
Authorization: Bearer {access_token}
```

---

## 🎓 Cursos

### **GET** `/courses/`

Lista todos os cursos disponíveis.

**Autenticação:** Não requerida

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Introdução à Programação",
    "description": "Aprenda os fundamentos da programação",
    "professor_id": 5
  },
  {
    "id": 2,
    "title": "Python Avançado",
    "description": "Domine Python com projetos práticos",
    "professor_id": 3
  }
]
```

---

### **POST** `/courses/`

Cria um novo curso.

**Autenticação:** Não requerida

**Request Body:**
```json
{
  "title": "Introdução à Programação",
  "description": "Aprenda os fundamentos da programação",
  "professor_id": 5
}
```

**Campos:**
- `title` (string, obrigatório): Título do curso (único)
- `description` (string, opcional): Descrição do curso
- `professor_id` (integer, obrigatório): ID de um usuário do tipo Professor (P)

**Response (201 Created):**
```json
{
  "message": "Curso criado com sucesso."
}
```

**Possíveis Erros:**
- `404`: Professor não encontrado ou inválido
- `400`: Título já existe

---

### **POST** `/courses/enrollments`

Matricula o usuário autenticado em um curso.

**Autenticação:** ✅ Requerida

**Query Parameters:**
- `course_id` (integer): ID do curso

**Exemplo:**
```
POST /courses/enrollments?course_id=1
```

**Response (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**
- `404`: Curso não encontrado
- `400`: Já matriculado neste curso
- `401`: Token inválido/expirado

---

## 📦 Módulos

### **GET** `/modules/`

Lista todos os módulos.

**Autenticação:** Não requerida

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Fundamentos de Python",
    "course_id": 1
  },
  {
    "id": 2,
    "title": "Estruturas de Dados",
    "course_id": 1
  }
]
```

---

### **POST** `/modules/`

Cria um novo módulo em um curso.

**Autenticação:** ✅ Requerida (apenas professor do curso)

**Request Body:**
```json
{
  "title": "Fundamentos de Python",
  "course_id": 1
}
```

**Campos:**
- `title` (string, obrigatório): Título do módulo
- `course_id` (integer, obrigatório): ID do curso

**Response (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**
- `404`: Curso não encontrado
- `403`: Apenas o professor do curso pode criar módulos
- `401`: Token inválido

---

### **GET** `/modules/{module_id}`

Retorna detalhes de um módulo específico.

**Autenticação:** Não requerida

**Path Parameters:**
- `module_id` (integer): ID do módulo

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Fundamentos de Python",
  "course_id": 1
}
```

**Possíveis Erros:**
- `404`: Módulo não encontrado

---

### **POST** `/modules/{module_id}`

Marca um módulo como concluído para o usuário autenticado.

**Autenticação:** ✅ Requerida

**Path Parameters:**
- `module_id` (integer): ID do módulo

**Response (200 OK):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**
- `400`: Módulo já foi completado anteriormente
- `404`: Módulo não encontrado

---

## 📝 Aulas (Lessons)

### **GET** `/lessons/`

Lista todas as aulas.

**Autenticação:** Não requerida

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Introdução ao Python",
    "content_type": "V",
    "done": false,
    "module_id": 1
  },
  {
    "id": 2,
    "title": "Quiz - Fundamentos",
    "content_type": "Q",
    "done": false,
    "module_id": 1
  }
]
```

**content_type:**
- `"V"`: Vídeo
- `"Q"`: Quiz

---

### **POST** `/lessons/`

Cria uma nova aula.

**Autenticação:** ✅ Requerida (apenas professor do curso)

**Request Body:**
```json
{
  "title": "Introdução ao Python",
  "content_type": "V",
  "done": false,
  "module_id": 1
}
```

**Campos:**
- `title` (string, obrigatório): Título da aula
- `content_type` (string, obrigatório): "V" (Vídeo) ou "Q" (Quiz)
- `done` (boolean, opcional): Default false
- `module_id` (integer, obrigatório): ID do módulo

**Response (201 Created):**
```json
{
  "msg": "success",
  "id": 1
}
```

**Possíveis Erros:**
- `404`: Módulo não encontrado
- `403`: Apenas o professor do curso pode criar aulas
- `422`: content_type inválido

---

### **GET** `/lessons/{lesson_id}`

Retorna detalhes de uma aula específica.

**Autenticação:** Não requerida

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Introdução ao Python",
  "content_type": "V",
  "done": false,
  "module_id": 1
}
```

---

### **POST** `/lessons/{lesson_id}`

Marca uma aula como concluída para o usuário autenticado.

**Autenticação:** ✅ Requerida

**Path Parameters:**
- `lesson_id` (integer): ID da aula

**Response (200 OK):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**
- `400`: Aula já foi completada anteriormente

---

### **POST** `/lessons/create/video`

Adiciona conteúdo de vídeo a uma aula.

**Autenticação:** ✅ Requerida (apenas professor do curso)

**Request Body:**
```json
{
  "lesson_id": 1,
  "video_url": "https://youtube.com/watch?v=exemplo123"
}
```

**Campos:**
- `lesson_id` (integer, obrigatório): ID da aula
- `video_url` (string, obrigatório): URL do vídeo

**Response (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**
- `404`: Aula não encontrada
- `403`: Apenas o professor do curso pode criar conteúdo

---

### **POST** `/lessons/create/quiz`

Cria um quiz completo com perguntas e opções.

**Autenticação:** ✅ Requerida (apenas professor do curso)

**Request Body:**
```json
{
  "lesson_id": 1,
  "questions": [
    {
      "quiz_id": 1,
      "question_text": "O que é Python?",
      "options": [
        {
          "question_id": 1,
          "option_text": "Uma linguagem de programação",
          "is_correct": true
        },
        {
          "question_id": 1,
          "option_text": "Um tipo de cobra",
          "is_correct": false
        },
        {
          "question_id": 1,
          "option_text": "Um framework web",
          "is_correct": false
        }
      ]
    },
    {
      "quiz_id": 1,
      "question_text": "Python é interpretado ou compilado?",
      "options": [
        {
          "question_id": 2,
          "option_text": "Interpretado",
          "is_correct": true
        },
        {
          "question_id": 2,
          "option_text": "Compilado",
          "is_correct": false
        }
      ]
    }
  ]
}
```

**Regras:**
- Cada pergunta deve ter **exatamente uma** opção com `is_correct: true`
- Mínimo 2 opções por pergunta

**Response (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**
- `400`: Pergunta sem opção correta ou com múltiplas corretas
- `404`: Aula não encontrada
- `403`: Apenas o professor pode criar quizzes

---

### **GET** `/lessons/quiz/questions`

Lista todas as perguntas de um quiz.

**Autenticação:** Não requerida

**Query Parameters:**
- `quiz_id` (integer): ID do quiz

**Exemplo:**
```
GET /lessons/quiz/questions?quiz_id=1
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "question_text": "O que é Python?",
    "options": [
      {
        "id": 1,
        "option_text": "Uma linguagem de programação"
      },
      {
        "id": 2,
        "option_text": "Um tipo de cobra"
      },
      {
        "id": 3,
        "option_text": "Um framework web"
      }
    ]
  }
]
```

**Nota:** A resposta **não inclui** `is_correct` para evitar spoilers.

**Possíveis Erros:**
- `404`: Nenhuma pergunta encontrada

---

### **POST** `/lessons/quiz/question`

Adiciona uma pergunta a um quiz existente.

**Autenticação:** ✅ Requerida (apenas professor do curso)

**Request Body:**
```json
{
  "quiz_id": 1,
  "question_text": "Qual a versão mais recente do Python?",
  "options": [
    {
      "question_id": 3,
      "option_text": "Python 3.12",
      "is_correct": true
    },
    {
      "question_id": 3,
      "option_text": "Python 2.7",
      "is_correct": false
    },
    {
      "question_id": 3,
      "option_text": "Python 4.0",
      "is_correct": false
    }
  ]
}
```

**Campos:**
- `quiz_id` (integer, obrigatório): ID do quiz
- `question_text` (string, obrigatório): Texto da pergunta
- `options` (array, obrigatório): Lista de opções (mínimo 2)
  - `option_text` (string, obrigatório): Texto da opção
  - `is_correct` (boolean, obrigatório): Exatamente uma deve ser true

**Response (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**
- `400`: Opção correta duplicada ou ausente
- `404`: Quiz não encontrado
- `403`: Apenas o professor pode adicionar perguntas

---

### **POST** `/lessons/quiz/answer`

Responde um quiz e marca a aula como concluída.

**Autenticação:** ✅ Requerida

**Query Parameters:**
- `lesson_id` (integer): ID da aula
- `quiz_id` (integer): ID do quiz

**Request Body:**
```json
{
  "answer_option_ids": [1, 5, 9]
}
```

**Campos:**
- `answer_option_ids` (array de integers): IDs das opções selecionadas

**Exemplo Completo:**
```
POST /lessons/quiz/answer?lesson_id=2&quiz_id=1

Body:
["answer_option_ids": [1, 5, 9]]
```

**Response (200 OK):**
```json
{
  "msg": "success"
}
```

**O que acontece:**
1. Sistema valida respostas
2. Calcula nota (acertos / total_perguntas × 100)
3. Salva tentativa com nota
4. Marca aula como concluída

**Possíveis Erros:**
- `400`: Quiz já foi respondido anteriormente
- `404`: Opção não encontrada

---

## 📊 Estrutura de Dados

### **User (Usuário)**
```typescript
{
  id: number
  username: string
  password: string (hasheada)
  email: string
  fullname: string
  telephone: string
  type_user: "A" | "P"  // Aluno ou Professor
}
```

### **Course (Curso)**
```typescript
{
  id: number
  title: string
  description: string
  professor_id: number
}
```

### **Module (Módulo)**
```typescript
{
  id: number
  title: string
  course_id: number
}
```

### **Lesson (Aula)**
```typescript
{
  id: number
  title: string
  content_type: "V" | "Q"  // Vídeo ou Quiz
  done: boolean
  module_id: number
}
```

### **LessonVideo**
```typescript
{
  id: number
  lesson_id: number
  video_url: string
}
```

### **QuizQuestion**
```typescript
{
  id: number
  quiz_id: number
  question_text: string
  options: QuizOption[]
}
```

### **QuizOption**
```typescript
{
  id: number
  question_id: number
  option_text: string
  is_correct: boolean
}
```

---

## 🔒 Autenticação e Autorização

### **Rotas Públicas (sem token):**
- `POST /auth/register`
- `POST /auth/login`
- `GET /courses/`
- `GET /modules/`
- `GET /lessons/`
- `GET /lessons/{id}`
- `GET /modules/{id}`
- `GET /lessons/quiz/questions`

### **Rotas Autenticadas (requer token):**
- `POST /courses/enrollments`
- `POST /modules/{id}` (completar)
- `POST /lessons/{id}` (completar)
- `POST /lessons/quiz/answer`

### **Rotas Restritas a Professores:**
- `POST /modules/` (apenas do próprio curso)
- `POST /lessons/` (apenas do próprio curso)
- `POST /lessons/create/video`
- `POST /lessons/create/quiz`
- `POST /lessons/quiz/question`

---

## ⚠️ Códigos de Status HTTP

| Código | Significado | Quando Ocorre |
|--------|-------------|---------------|
| 200 | OK | Operação bem-sucedida (GET, completar) |
| 201 | Created | Recurso criado com sucesso |
| 400 | Bad Request | Dados inválidos, duplicação, regras violadas |
| 401 | Unauthorized | Token ausente, inválido ou expirado |
| 403 | Forbidden | Sem permissão (não é o professor) |
| 404 | Not Found | Recurso não encontrado |
| 422 | Unprocessable Entity | Validação de schema falhou |
| 500 | Internal Server Error | Erro no servidor |

---

## 🧪 Exemplos de Uso

### **1. Fluxo Completo de um Aluno**

````bash
# 1. Registrar
POST /auth/register
{
  "username": "maria",
  "password": "Maria123",
  "email": "maria@example.com",
  "fullname": "Maria Santos",
  "telephone": "(11) 98765-4321",
  "type_user": "A"
}

# 2. Login
POST /auth/login
username=maria&password=Maria123

# Resposta:
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}

# 3. Ver cursos disponíveis
GET /courses/

# 4. Matricular-se
POST /courses/enrollments?course_id=1
Authorization: Bearer eyJ...

# 5. Ver módulos do curso
GET /modules/

# 6. Ver aulas de um módulo
GET /lessons/

# 7. Assistir vídeo e completar
POST /lessons/1
Authorization: Bearer eyJ...

# 8. Responder quiz
POST /lessons/quiz/answer?lesson_id=2&quiz_id=1
Authorization: Bearer eyJ...
Body: {"answer_option_ids": [1, 5, 9]}

# 9. Completar módulo
POST /modules/1
Authorization: Bearer eyJ...
````

### **2. Fluxo de um Professor**

````bash
# 1. Registrar como professor
POST /auth/register
{
  "username": "prof_joao",
  "password": "Prof123",
  "email": "joao@prof.com",
  "fullname": "João Professor",
  "telephone": "(11) 91234-5678",
  "type_user": "P"
}

# 2. Login
POST /auth/login
username=prof_joao&password=Prof123

# 3. Criar curso
POST /courses/
{
  "title": "Python para Iniciantes",
  "description": "Curso completo de Python",
  "professor_id": 5
}

# 4. Criar módulo
POST /modules/
Authorization: Bearer eyJ...
{
  "title": "Introdução",
  "course_id": 1
}

# 5. Criar aula de vídeo
POST /lessons/
Authorization: Bearer eyJ...
{
  "title": "Primeira Aula",
  "content_type": "V",
  "module_id": 1
}

# 6. Adicionar vídeo
POST /lessons/create/video
Authorization: Bearer eyJ...
{
  "lesson_id": 1,
  "video_url": "https://youtube.com/..."
}

# 7. Criar aula com quiz
POST /lessons/
Authorization: Bearer eyJ...
{
  "title": "Quiz - Python Básico",
  "content_type": "Q",
  "module_id": 1
}

# 8. Criar quiz completo
POST /lessons/create/quiz
Authorization: Bearer eyJ...
{
  "lesson_id": 2,
  "questions": [...]
}
````

---

## 🐛 Troubleshooting

### **401 Unauthorized**
- Verifique se o token está no formato: `Authorization: Bearer {token}`
- Token pode ter expirado (30 minutos de validade)
- Faça login novamente

### **403 Forbidden**
- Você não é o professor deste curso
- Apenas professores podem criar/editar conteúdo
- Verifique se está usando a conta correta

### **422 Unprocessable Entity**
- Dados não passaram na validação
- Verifique formatos: email, telefone, senha
- Veja a mensagem de erro para detalhes

### **400 Bad Request**
- Regra de negócio violada
- Exemplos: já matriculado, quiz já respondido, múltiplas respostas corretas
- Leia a mensagem `detail` para mais informações

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação Swagger: http://localhost:8000/docs
2. Consulte os logs do servidor
3. Verifique exemplos acima

---

**Última atualização:** 18 de novembro de 2025
**Versão da API:** 1.0.0
