# 🤖 Engenharia de Prompt e Rastreabilidade

Este documento cumpre as exigências dos tópicos **1.2** e **1.4** do edital de Entrega Final, detalhando as integrações de Inteligência Artificial e a rastreabilidade do core da aplicação.

---

## 📋 1.2 — Documentação de Integrações de IA e Engenharia de Prompt

### Configurações Gerais da API
* **API Utilizada:** OpenAI API
* **Modelo:** `gpt-3.5-turbo`
* **Localização no Código:** `backend/api/views.py`

### Mapeamento de Endpoints e Funcionalidades

| Funcionalidade | Endpoint | Temperatura | Descrição |
| :--- | :--- | :--- | :--- |
| **Geração de provas** | `POST /api/generate-exam/` | `0.8` | Temperatura mais alta para permitir criatividade na elaboração de novas questões educacionais. |
| **Correção de respostas** | `POST /api/submissions/` | `0.4` | Temperatura mais baixa para garantir foco, precisão e consistência técnica na avaliação do aluno. |

### Prompts de Sistema (System Prompts) que Sustentam a Aplicação

#### 1. Prompt de Geração (`GENERATION_SYSTEM_PROMPT`)
```text
Você é um especialista em criação de avaliações educacionais brasileiras.
Crie questões no nível especificado. Para questões fechadas, gere exatamente 4 alternativas (A-D) com apenas uma correta. Para dissertativas, não inclua alternativas.
Responda SOMENTE em JSON válido (sem markdown) com o seguinte formato:
{"questions": [{"statement": "...", "rubric": "resposta esperada e critérios", "question_type": "dissertativa|fechada", "difficulty": "facil|medio|dificil", "alternatives": [{"letter": "A", "text": "...", "is_correct": false}]}]}
```

#### 2. Prompt de Correção (`FEEDBACK_SYSTEM_PROMPT`)
```text
Você é um professor tutor universitário. Analise a resposta do aluno com base no enunciado e na rubrica. Seja encorajador e pedagógico. Nunca dê a resposta pronta.
Responda SOMENTE em JSON válido (sem markdown) com as chaves:
"score": float 0-10,
"key_strengths": string,
"areas_for_improvement": string,
"constructive_feedback": string
```

## 🔄 1.4 — Versão Final do Repositório de Prompts com Rastreabilidade
Todos os prompts que controlam o core do sistema estão desacoplados e versionados diretamente no arquivo de visualizações da API do backend. Qualquer alteração ou refatoração no comportamento da IA gera um novo registro histórico no versionamento do projeto.

🔗 Link Direto para a Rastreabilidade de Alterações (Histórico de Commits): [Acesse aqui o Histórico de Alterações dos Prompts no GitHub](https://github.com/Eduardo-Borges18/TrAI-Questions/commits/main)
