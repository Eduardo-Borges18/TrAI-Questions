import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Exam, Question, Alternative, Submission, Feedback
from django.contrib.auth.models import User

# Evita re-execução
if Exam.objects.filter(subject__in=["Linguagem C", "Python", "Java"]).exists():
    print("Dados já existem. Pulando seed.")
    exit()

admin_user = User.objects.filter(username="admin").first()

EXAMS = [
    {
        "title": "Fundamentos de Linguagem C",
        "subject": "Linguagem C",
        "description": "Avalia conhecimentos fundamentais da linguagem C, incluindo ponteiros, memória e estruturas.",
        "questions": [
            {
                "order_num": 1, "question_type": "fechada", "difficulty": "facil",
                "statement": "Em C, qual operador é usado para acessar o valor armazenado no endereço de um ponteiro?",
                "rubric": "Resposta correta: * (asterisco). O operador de dereferência '*' acessa o valor contido no endereço de memória apontado pelo ponteiro.",
                "alternatives": [
                    {"letter": "A", "text": "& (e comercial)", "is_correct": False},
                    {"letter": "B", "text": "* (asterisco)", "is_correct": True},
                    {"letter": "C", "text": "-> (seta)", "is_correct": False},
                    {"letter": "D", "text": ". (ponto)", "is_correct": False},
                ],
                "mock_answer": "B",
                "mock_score": "10.00",
                "mock_feedback": "Excelente! O operador '*' é usado corretamente para derreferenciar ponteiros em C.",
                "mock_strengths": "Conhecimento preciso do operador de dereferência.",
                "mock_improvements": "Nenhum ponto a melhorar nesta questão.",
            },
            {
                "order_num": 2, "question_type": "fechada", "difficulty": "medio",
                "statement": "Qual função da biblioteca stdlib.h é usada para alocar memória dinamicamente em C?",
                "rubric": "Resposta correta: malloc(). A função malloc() aloca um bloco de memória do tamanho especificado em bytes e retorna um ponteiro para ele.",
                "alternatives": [
                    {"letter": "A", "text": "alloc()", "is_correct": False},
                    {"letter": "B", "text": "new()", "is_correct": False},
                    {"letter": "C", "text": "malloc()", "is_correct": True},
                    {"letter": "D", "text": "memset()", "is_correct": False},
                ],
                "mock_answer": "C",
                "mock_score": "10.00",
                "mock_feedback": "Correto! malloc() é a função padrão para alocação dinâmica de memória em C.",
                "mock_strengths": "Conhece as funções padrão da stdlib.",
                "mock_improvements": "Lembre-se sempre de verificar se malloc() retornou NULL antes de usar o ponteiro.",
            },
            {
                "order_num": 3, "question_type": "dissertativa", "difficulty": "medio",
                "statement": "Explique com suas palavras o que é um ponteiro em C e dê um exemplo de declaração.",
                "rubric": "Espera-se: ponteiro é uma variável que armazena o endereço de memória de outra variável. Exemplo: int *p; p = &x;",
                "alternatives": [],
                "mock_answer": "Um ponteiro é uma variável que guarda o endereço de memória de outra variável. Por exemplo: int x = 10; int *p = &x; — aqui p armazena o endereço de x.",
                "mock_score": "9.00",
                "mock_feedback": "Boa resposta! O conceito foi bem explicado e o exemplo está correto.",
                "mock_strengths": "Explicação clara e exemplo funcional com uso do operador &.",
                "mock_improvements": "Poderia mencionar que ponteiros permitem manipulação direta de memória, o que é um dos recursos mais poderosos e perigosos da linguagem C.",
            },
            {
                "order_num": 4, "question_type": "fechada", "difficulty": "dificil",
                "statement": "O que ocorre quando se tenta acessar um ponteiro que aponta para NULL em C?",
                "rubric": "Resposta correta: Segmentation Fault. O sistema operacional detecta o acesso indevido à memória e encerra o programa com um Segmentation Fault.",
                "alternatives": [
                    {"letter": "A", "text": "O programa retorna 0 automaticamente", "is_correct": False},
                    {"letter": "B", "text": "O compilador lança um erro em tempo de compilação", "is_correct": False},
                    {"letter": "C", "text": "O programa gera um Segmentation Fault e é encerrado", "is_correct": True},
                    {"letter": "D", "text": "O ponteiro é reinicializado para um endereço válido", "is_correct": False},
                ],
                "mock_answer": "C",
                "mock_score": "10.00",
                "mock_feedback": "Perfeito! Segmentation Fault é o comportamento esperado ao dereferenciar um ponteiro NULL.",
                "mock_strengths": "Compreende o comportamento do sistema operacional diante de acesso de memória inválido.",
                "mock_improvements": "Estude também como usar ferramentas como Valgrind para detectar esses erros em tempo de execução.",
            },
            {
                "order_num": 5, "question_type": "dissertativa", "difficulty": "dificil",
                "statement": "Qual a diferença entre struct e union em C? Em qual situação cada um é mais indicado?",
                "rubric": "struct: cada membro ocupa seu próprio espaço de memória. union: todos os membros compartilham o mesmo espaço. union é indicado quando só um campo será usado por vez, economizando memória.",
                "alternatives": [],
                "mock_answer": "Em struct cada campo tem seu próprio espaço de memória, então todos podem ser usados ao mesmo tempo. Já em union todos os campos compartilham o mesmo espaço, então só um pode conter um valor válido por vez. Union é útil quando se quer economizar memória e só um dos campos será usado.",
                "mock_score": "8.50",
                "mock_feedback": "Resposta bem estruturada com os conceitos corretos.",
                "mock_strengths": "Entendimento correto da alocação de memória de cada estrutura.",
                "mock_improvements": "Poderia incluir um exemplo de código para ilustrar melhor a diferença prática entre os dois.",
            },
            {
                "order_num": 6, "question_type": "fechada", "difficulty": "facil",
                "statement": "Qual é o tipo de retorno da função main() em um programa C padrão (C99/C11)?",
                "rubric": "Resposta correta: int. A função main() deve retornar int para indicar ao sistema operacional o código de saída do programa.",
                "alternatives": [
                    {"letter": "A", "text": "void", "is_correct": False},
                    {"letter": "B", "text": "int", "is_correct": True},
                    {"letter": "C", "text": "char", "is_correct": False},
                    {"letter": "D", "text": "bool", "is_correct": False},
                ],
                "mock_answer": "B",
                "mock_score": "10.00",
                "mock_feedback": "Correto! O tipo int é obrigatório no padrão C99 e C11.",
                "mock_strengths": "Conhece os padrões da linguagem C.",
                "mock_improvements": "Nenhum ponto a melhorar.",
            },
        ],
    },
    {
        "title": "Programação em Python",
        "subject": "Python",
        "description": "Avalia conhecimentos em Python, abrangendo estruturas de dados, paradigmas e recursos avançados da linguagem.",
        "questions": [
            {
                "order_num": 1, "question_type": "fechada", "difficulty": "facil",
                "statement": "Qual método é usado para adicionar um elemento ao final de uma lista em Python?",
                "rubric": "Resposta correta: append(). O método list.append(x) adiciona o item x ao final da lista.",
                "alternatives": [
                    {"letter": "A", "text": "add()", "is_correct": False},
                    {"letter": "B", "text": "insert()", "is_correct": False},
                    {"letter": "C", "text": "append()", "is_correct": True},
                    {"letter": "D", "text": "push()", "is_correct": False},
                ],
                "mock_answer": "C",
                "mock_score": "10.00",
                "mock_feedback": "Correto! append() é o método padrão para adicionar ao final de listas.",
                "mock_strengths": "Conhece os métodos básicos de listas.",
                "mock_improvements": "Estude também extend() e insert() para adicionar múltiplos itens ou em posições específicas.",
            },
            {
                "order_num": 2, "question_type": "fechada", "difficulty": "facil",
                "statement": "Qual é a principal diferença entre uma lista (list) e uma tupla (tuple) em Python?",
                "rubric": "Resposta correta: Tuplas são imutáveis. Listas são mutáveis (podem ser alteradas após criação), tuplas são imutáveis (não podem ser alteradas).",
                "alternatives": [
                    {"letter": "A", "text": "Listas são mais rápidas que tuplas", "is_correct": False},
                    {"letter": "B", "text": "Tuplas aceitam apenas números, listas aceitam qualquer tipo", "is_correct": False},
                    {"letter": "C", "text": "Listas são mutáveis, tuplas são imutáveis", "is_correct": True},
                    {"letter": "D", "text": "Não há diferença prática entre os dois tipos", "is_correct": False},
                ],
                "mock_answer": "C",
                "mock_score": "10.00",
                "mock_feedback": "Exato! Mutabilidade é a diferença fundamental entre list e tuple.",
                "mock_strengths": "Compreende a imutabilidade de tuplas.",
                "mock_improvements": "Aprofunde-se em quando usar cada estrutura: tuplas são preferidas para dados que não devem mudar, como coordenadas ou chaves de dicionário.",
            },
            {
                "order_num": 3, "question_type": "dissertativa", "difficulty": "medio",
                "statement": "O que são list comprehensions em Python? Escreva um exemplo que gere uma lista com os quadrados dos números de 1 a 5.",
                "rubric": "List comprehensions são uma sintaxe concisa para criar listas. Exemplo correto: quadrados = [x**2 for x in range(1, 6)]",
                "alternatives": [],
                "mock_answer": "List comprehensions são uma forma compacta de criar listas em Python usando uma sintaxe dentro de colchetes. Exemplo: quadrados = [x**2 for x in range(1, 6)] — isso gera [1, 4, 9, 16, 25].",
                "mock_score": "10.00",
                "mock_feedback": "Perfeito! Definição correta e exemplo funcional.",
                "mock_strengths": "Sabe criar e explicar list comprehensions com exemplo prático.",
                "mock_improvements": "Explore também dict comprehensions e set comprehensions para expandir o conhecimento.",
            },
            {
                "order_num": 4, "question_type": "dissertativa", "difficulty": "dificil",
                "statement": "O que é um decorator em Python? Explique como ele funciona e dê um exemplo prático.",
                "rubric": "Decorator é uma função que recebe outra função como argumento, adiciona comportamento e retorna a função modificada. Usa-se @nome_do_decorator acima da função alvo.",
                "alternatives": [],
                "mock_answer": "Um decorator é uma função que envolve outra função para modificar ou estender seu comportamento sem alterar seu código. Exemplo: @meu_decorator def saudacao(): print('Olá'). O decorator recebe a função, faz algo antes/depois e retorna a versão modificada.",
                "mock_score": "8.00",
                "mock_feedback": "Boa resposta! O conceito está correto mas o exemplo poderia ser mais completo.",
                "mock_strengths": "Entende o conceito de função de ordem superior e o açúcar sintático do @.",
                "mock_improvements": "No exemplo, mostre também o corpo do decorator com a função wrapper interna para ficar mais claro como ele funciona internamente.",
            },
            {
                "order_num": 5, "question_type": "fechada", "difficulty": "dificil",
                "statement": "O que é o GIL (Global Interpreter Lock) no CPython e qual é seu principal impacto?",
                "rubric": "Resposta correta: impede execução paralela de threads. O GIL é um mutex que permite apenas uma thread executar código Python por vez, limitando o paralelismo real em programas multi-thread.",
                "alternatives": [
                    {"letter": "A", "text": "É um mecanismo de coleta de lixo que libera memória não utilizada", "is_correct": False},
                    {"letter": "B", "text": "É um mutex que impede que múltiplas threads executem código Python simultaneamente", "is_correct": True},
                    {"letter": "C", "text": "É uma ferramenta para otimizar laços de repetição automaticamente", "is_correct": False},
                    {"letter": "D", "text": "É uma biblioteca para programação assíncrona com async/await", "is_correct": False},
                ],
                "mock_answer": "B",
                "mock_score": "10.00",
                "mock_feedback": "Excelente! Compreende um dos aspectos mais avançados do CPython.",
                "mock_strengths": "Conhecimento sólido sobre concorrência e as limitações do CPython.",
                "mock_improvements": "Estude alternativas ao GIL como multiprocessing, asyncio ou Jython para contornar essa limitação.",
            },
            {
                "order_num": 6, "question_type": "dissertativa", "difficulty": "medio",
                "statement": "Explique a diferença entre os métodos __str__ e __repr__ em Python e quando cada um é chamado.",
                "rubric": "__str__ é chamado por str() e print(), deve retornar representação legível para humanos. __repr__ é chamado por repr(), deve retornar representação técnica/unambígua, útil para debug.",
                "alternatives": [],
                "mock_answer": "__str__ retorna uma representação legível da classe, usada pelo print(). __repr__ retorna uma representação técnica, usada no console interativo e para debug. Se __str__ não existir, Python usa __repr__ como fallback.",
                "mock_score": "9.50",
                "mock_feedback": "Ótima resposta! Mencionou o fallback, o que demonstra conhecimento aprofundado.",
                "mock_strengths": "Compreende os dois métodos e sabe que __repr__ funciona como fallback.",
                "mock_improvements": "Poderia adicionar um exemplo concreto de uma classe com os dois métodos implementados.",
            },
        ],
    },
    {
        "title": "Orientação a Objetos com Java",
        "subject": "Java",
        "description": "Avalia os pilares da orientação a objetos aplicados em Java: herança, polimorfismo, encapsulamento e abstração.",
        "questions": [
            {
                "order_num": 1, "question_type": "fechada", "difficulty": "facil",
                "statement": "Qual palavra-chave é usada em Java para que uma classe herde de outra?",
                "rubric": "Resposta correta: extends. Em Java, 'class Filho extends Pai' estabelece a herança.",
                "alternatives": [
                    {"letter": "A", "text": "implements", "is_correct": False},
                    {"letter": "B", "text": "inherits", "is_correct": False},
                    {"letter": "C", "text": "extends", "is_correct": True},
                    {"letter": "D", "text": "super", "is_correct": False},
                ],
                "mock_answer": "C",
                "mock_score": "10.00",
                "mock_feedback": "Correto! extends é a palavra-chave de herança em Java.",
                "mock_strengths": "Conhece a sintaxe básica de herança em Java.",
                "mock_improvements": "Lembre-se que Java só permite herança simples (uma classe pai), diferente de linguagens como C++.",
            },
            {
                "order_num": 2, "question_type": "dissertativa", "difficulty": "medio",
                "statement": "Explique o conceito de polimorfismo em Java e mostre um exemplo usando sobrescrita de método (override).",
                "rubric": "Polimorfismo permite que objetos de classes diferentes sejam tratados como objetos da classe pai. Override: subclasse redefine método da superclasse usando @Override.",
                "alternatives": [],
                "mock_answer": "Polimorfismo é a capacidade de um objeto assumir múltiplas formas. No override, uma subclasse redefine um método da superclasse: class Animal { void falar(){} } class Cachorro extends Animal { @Override void falar(){ System.out.println('Au!'); } }",
                "mock_score": "9.00",
                "mock_feedback": "Boa resposta com exemplo funcional e uso correto da anotação @Override.",
                "mock_strengths": "Exemplo claro com uso correto da anotação @Override.",
                "mock_improvements": "Mencione também o polimorfismo via interface e como uma referência do tipo pai pode apontar para um objeto filho (upcasting).",
            },
            {
                "order_num": 3, "question_type": "fechada", "difficulty": "facil",
                "statement": "Qual palavra-chave define uma interface em Java?",
                "rubric": "Resposta correta: interface. Ex: public interface Voavel { void voar(); }",
                "alternatives": [
                    {"letter": "A", "text": "abstract", "is_correct": False},
                    {"letter": "B", "text": "interface", "is_correct": True},
                    {"letter": "C", "text": "implements", "is_correct": False},
                    {"letter": "D", "text": "contract", "is_correct": False},
                ],
                "mock_answer": "B",
                "mock_score": "10.00",
                "mock_feedback": "Correto! interface é a palavra-chave para declarar interfaces em Java.",
                "mock_strengths": "Conhece a sintaxe de interfaces.",
                "mock_improvements": "Estude também as diferenças entre interface e classe abstrata, pois é uma pergunta clássica em entrevistas.",
            },
            {
                "order_num": 4, "question_type": "fechada", "difficulty": "medio",
                "statement": "O que é o Garbage Collector no Java?",
                "rubric": "Resposta correta: mecanismo automático de gerenciamento de memória. O GC da JVM identifica e libera objetos que não têm mais referências, evitando memory leaks.",
                "alternatives": [
                    {"letter": "A", "text": "Um compilador que otimiza o bytecode Java", "is_correct": False},
                    {"letter": "B", "text": "Um mecanismo que libera automaticamente a memória de objetos sem referência", "is_correct": True},
                    {"letter": "C", "text": "Uma ferramenta de análise de código para encontrar bugs", "is_correct": False},
                    {"letter": "D", "text": "Um processo que reinicia a JVM quando há falta de memória", "is_correct": False},
                ],
                "mock_answer": "B",
                "mock_score": "10.00",
                "mock_feedback": "Perfeito! O Garbage Collector é um dos recursos mais importantes da JVM.",
                "mock_strengths": "Compreende o gerenciamento automático de memória da JVM.",
                "mock_improvements": "Aprofunde-se nos algoritmos do GC (como G1 e ZGC) para entrevistas de nível avançado.",
            },
            {
                "order_num": 5, "question_type": "dissertativa", "difficulty": "dificil",
                "statement": "Qual a diferença entre uma classe abstrata e uma interface em Java? Quando você usaria cada uma?",
                "rubric": "Classe abstrata: pode ter estado (atributos) e métodos concretos, herança simples. Interface: contrato puro (antes do Java 8), herança múltipla. Usar classe abstrata para compartilhar código, interface para definir contratos.",
                "alternatives": [],
                "mock_answer": "Classe abstrata pode ter atributos e métodos com implementação, mas só pode ser herdada por uma classe. Interface define apenas o contrato (métodos sem corpo, antes do Java 8) e pode ser implementada por várias classes. Uso classe abstrata quando quero compartilhar código entre subclasses, e interface quando quero garantir que classes diferentes implementem um contrato comum.",
                "mock_score": "9.50",
                "mock_feedback": "Excelente resposta, bem estruturada e com critério de decisão claro.",
                "mock_strengths": "Explica claramente quando usar cada um com base em herança múltipla e compartilhamento de código.",
                "mock_improvements": "Mencione os default methods introduzidos no Java 8, que permitem que interfaces tenham implementações concretas, tornando a fronteira entre os dois conceitos mais tênue.",
            },
            {
                "order_num": 6, "question_type": "fechada", "difficulty": "medio",
                "statement": "Qual modificador de acesso em Java torna um atributo visível apenas dentro da própria classe?",
                "rubric": "Resposta correta: private. O modificador private restringe o acesso ao atributo apenas à classe onde ele foi declarado, implementando encapsulamento.",
                "alternatives": [
                    {"letter": "A", "text": "protected", "is_correct": False},
                    {"letter": "B", "text": "public", "is_correct": False},
                    {"letter": "C", "text": "internal", "is_correct": False},
                    {"letter": "D", "text": "private", "is_correct": True},
                ],
                "mock_answer": "D",
                "mock_score": "10.00",
                "mock_feedback": "Correto! private é o modificador mais restritivo e base do encapsulamento.",
                "mock_strengths": "Compreende os modificadores de acesso e o princípio de encapsulamento.",
                "mock_improvements": "Revise todos os níveis de acesso: private, default (package), protected e public.",
            },
        ],
    },
]

for exam_data in EXAMS:
    exam = Exam.objects.create(
        title=exam_data["title"],
        subject=exam_data["subject"],
        description=exam_data["description"],
        is_active=True,
    )
    print(f"Prova criada: {exam.title}")

    for q_data in exam_data["questions"]:
        question = Question.objects.create(
            exam=exam,
            order_num=q_data["order_num"],
            statement=q_data["statement"],
            rubric=q_data["rubric"],
            question_type=q_data["question_type"],
            difficulty=q_data["difficulty"],
        )

        for alt in q_data["alternatives"]:
            Alternative.objects.create(
                question=question,
                letter=alt["letter"],
                text=alt["text"],
                is_correct=alt["is_correct"],
            )

        submission = Submission.objects.create(
            user=admin_user,
            question=question,
            exam=exam,
            answer_text=q_data["mock_answer"],
        )

        Feedback.objects.create(
            submission=submission,
            score=q_data["mock_score"],
            constructive_feedback=q_data["mock_feedback"],
            key_strengths=q_data["mock_strengths"],
            areas_for_improvement=q_data["mock_improvements"],
        )

        print(f"  Q{q_data['order_num']} + submission + feedback criados.")

print("\nSeed concluído com sucesso!")
