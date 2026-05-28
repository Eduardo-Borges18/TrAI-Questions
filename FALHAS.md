# ❌ 1.5 — Exemplos de Prompts que Falharam

Este relatório atende ao requisito **1.5** do edital de Entrega Final, apresentando de forma analítica dois cenários práticos onde as instruções iniciais da IA falharam, as respectivas correções de engenharia de prompt e as metodologias de validação da equipe.

---

### 🔍 Falha 1 — Retorno fora do formato JSON (Quebra do Backend)

* **Prompt Original:** O sistema enviava apenas comandos genéricos de avaliação como `"avalie a resposta do aluno"`, sem delimitação estrita de formato de saída.
* **Problema Identificado:** A IA retornava textos corridos e livres (ex: *"A resposta está boa! O aluno demonstrou..."*). Como o backend esperava um objeto estruturado para processar a nota e salvar no banco de dados, o sistema lançava exceções e quebrava, tornando impossível a leitura pelo código.
* **Ajuste Aplicado:** Foi adicionada a instrução imperativa `"Responda SOMENTE em JSON válido (sem markdown)"` junto com as chaves obrigatórias delimitadas, além de uma lógica de limpeza de blocos extras de código (como \`\`\`json \`\`\`) caso a IA insistisse em usá-los.
* **Validação do Output:** A equipe validou a correção realizando testes manuais massivos direto no endpoint `/api/submissions/` simulando diferentes tipos de respostas de alunos. Verificou-se que o método `json.loads()` do Python parou de lançar exceções, confirmando a estabilidade da estrutura.

---

### 🔍 Falha 2 — Tipo de questão ignorado pela IA (Quebra do Frontend)

* **Prompt Original:** O comando inicial enviado para o modelo não diferenciava explicitamente a estrutura comportamental por tipo de questão (dissertativa ou fechada).
* **Problema Identificado:** Em testes de homologação, a IA gerava alternativas de múltipla escolha mesmo quando o professor solicitava uma questão estritamente dissertativa. Em outros momentos, omitia as alternativas em questões fechadas. Isso quebrava a renderização de telas do frontend, que tentava mapear opções inexistentes.
* **Ajuste Aplicado:** O *system prompt* de geração foi enriquecido com regras condicionais claras: `"Para questões fechadas, gere exatamente 4 alternativas (A-D) com apenas uma correta. Para dissertativas, não inclua alternativas."`
* **Validação do Output:** A equipe gerou baterias de provas de teste contendo um mix variado de questões (fechadas e dissertativas simultaneamente). Foi validado visualmente e via console de desenvolvedor que o array `alternatives` vinha devidamente vazio nas dissertativas e com exatamente 4 itens nas fechadas.
