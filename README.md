# 🎓 TrAI Questions — Plataforma de Avaliação com IA

Plataforma educacional que automatiza a **criação de provas** e a **correção de respostas** utilizando Inteligência Artificial (OpenAI GPT). O professor configura as provas pelo painel administrativo; a IA gera as questões, corrige as respostas dos alunos e entrega feedback pedagógico instantâneo.

🔗 **Frontend (aluno):** https://app-frontend-7nug.onrender.com  
🔗 **Backend / Admin (professor):** https://app-backend-3bsg.onrender.com/admin/

---

## 🚀 Funcionalidades

- **Geração de provas com IA:** o professor informa título, disciplina e especificações por questão; a IA gera enunciados, rubricas e alternativas automaticamente.
- **Correção baseada em rubricas:** a IA avalia a resposta do aluno comparando com a rubrica secreta definida na geração, minimizando alucinações.
- **Feedback multicritério:** nota (0–10), pontos fortes, pontos a melhorar e comentário construtivo.
- **Suporte a múltiplos tipos:** questões fechadas (múltipla escolha, 4 alternativas) e dissertativas.
- **Painel administrativo:** gestão completa de provas, questões, submissões e feedbacks via Django Admin.
- **Histórico persistente:** todas as submissões e feedbacks ficam salvos no banco de dados.

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Frontend | React 18 + Vite, Axios |
| Backend | Python 3.10, Django 5, Django REST Framework |
| IA | OpenAI API (`gpt-3.5-turbo`) |
| Banco de dados | SQLite |
| Deploy | Render (Blueprint via `render.yaml`) |

---

## ⚙️ Arquitetura e Fluxo

```
Professor (Admin)
   │
   ├─► Wizard de criação → POST /api/generate-exam/ → OpenAI (gera questões)
   └─► Salva prova       → POST /api/save-exam/

Aluno (Frontend)
   │
   ├─► Lista provas → GET /api/exams/
   ├─► Detalha prova → GET /api/exams/{id}/
   └─► Responde questão → POST /api/submissions/ → OpenAI (corrige) → Feedback
```

---

## 💻 Como executar localmente

### Pré-requisitos
- Python 3.10+
- Node.js 18+
- Chave de API da OpenAI (`sk-proj-...`)

---

### Passo 1 — Backend (Django)

```bash
cd backend
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o arquivo `.env` dentro da pasta `backend` (junto ao `manage.py`):

```env
OPENAI_API_KEY=sk-SUA_CHAVE_AQUI
```

Execute as migrações e inicie o servidor:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend disponível em: http://localhost:8000  
Painel admin em: http://localhost:8000/admin/

---

### Passo 2 — Frontend (React/Vite)

Abra um **novo terminal** (mantenha o backend rodando):

```bash
cd frontend
npm install
npm run dev
```

Frontend disponível em: http://localhost:5173

---

## 🔑 Variáveis de Ambiente

### Backend (`backend/.env`)

| Variável | Descrição | Obrigatória |
|---|---|---|
| `OPENAI_API_KEY` | Chave de API da OpenAI | ✅ Sim |
| `SECRET_KEY` | Chave secreta do Django (gerada automaticamente no Render) | ✅ Sim (produção) |
| `RENDER` | Setar como `true` para desativar o DEBUG em produção | ✅ Sim (produção) |

### Frontend (`frontend/.env`)

| Variável | Descrição | Obrigatória |
|---|---|---|
| `VITE_API_URL` | URL base da API do backend | ✅ Sim (produção) |

Exemplo:
```env
VITE_API_URL=https://app-backend-3bsg.onrender.com/api
```

---

## 🌐 Deploy (Render)

O arquivo `render.yaml` na raiz do projeto configura automaticamente os dois serviços (backend Python e frontend estático).

**Passos:**
1. Faça fork/clone do repositório para sua conta GitHub
2. Acesse [render.com](https://render.com) → **New Blueprint**
3. Conecte o repositório
4. Após criar os serviços, vá em **app-backend → Environment** e adicione manualmente:
   - `OPENAI_API_KEY` = sua chave da OpenAI
5. Aguarde o redeploy automático

> ⚠️ A `OPENAI_API_KEY` deve ser adicionada manualmente no painel do Render por segurança — o GitHub bloqueia o envio de chaves de API em arquivos públicos.

---

## 🔒 Segurança

- Chaves de API protegidas via `.env` (ignorado pelo `.gitignore`)
- `SECRET_KEY` do Django gerada automaticamente pelo Render (`generateValue: true`)
- `DEBUG=False` em produção (detectado via variável `RENDER`)
- CORS restrito ao domínio do frontend em produção
- `ALLOWED_HOSTS` restrito ao domínio do backend

---

## 🤖 Engenharia de Prompt

O ecossistema de inteligência artificial da plataforma foi desenvolvido com foco em robustez estrutural e rastreabilidade técnica. A documentação completa exigida pelo edital foi dividida para melhor legibilidade:

* 📄 [**Documentação de Integrações e Rastreabilidade (Itens 1.2 e 1.4)**](./PROMPTS.md)
* 📄 [**Relatório de Prompts que Falharam (Item 1.5)**](./FALHAS.md)
---

Desenvolvido como Projeto Integrador — TrAI Questions.
