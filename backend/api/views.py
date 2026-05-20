from .serializers import ExamListSerializer, ExamDetailSerializer, FeedbackSerializer
from .models import Exam, Question, Alternative, Submission, Feedback
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from openai import OpenAI
import os
import json
import logging
from dotenv import load_dotenv
load_dotenv()


logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

FEEDBACK_SYSTEM_PROMPT = (
    "Você é um professor tutor universitário. Analise a resposta do aluno com base no enunciado "
    "e na rubrica. Seja encorajador e pedagógico. Nunca dê a resposta pronta.\n"
    "Responda SOMENTE em JSON válido (sem markdown) com as chaves:\n"
    '  "score": float 0-10,\n'
    '  "key_strengths": string,\n'
    '  "areas_for_improvement": string,\n'
    '  "constructive_feedback": string\n')

GENERATION_SYSTEM_PROMPT = (
    "Você é um especialista em criação de avaliações educacionais brasileiras.\n"
    "Crie questões no nível especificado. Para questões fechadas, gere exatamente 4 alternativas (A-D) "
    "com apenas uma correta. Para dissertativas, não inclua alternativas.\n"
    "Responda SOMENTE em JSON válido (sem markdown) com o seguinte formato:\n"
    '{"questions": [{"statement": "...", "rubric": "resposta esperada e critérios", '
    '"question_type": "dissertativa|fechada", "difficulty": "facil|medio|dificil", '
    '"alternatives": [{"letter":"A","text":"...","is_correct":false}]}]}')


def call_openai(system_prompt, user_prompt, temperature=0.7):
    client = OpenAI(api_key=OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    raw = resp.choices[0].message.content
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()
    return json.loads(raw)


# ─── Listagem de provas (aluno) ─────────────────────────────────────────

class ExamListView(generics.ListAPIView):
    queryset = Exam.objects.filter(is_active=True).order_by("-created_at")
    serializer_class = ExamListSerializer


class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.filter(is_active=True)
    serializer_class = ExamDetailSerializer


# ─── Geração de prova com IA (professor — chamado pelo wizard do admin) ─

class GenerateExamView(APIView):
    """POST /api/generate-exam/  →  retorna JSON com questões geradas (sem salvar)."""

    def post(self, request):
        title = request.data.get("title", "").strip()
        subject = request.data.get("subject", "").strip()
        questions_specs = request.data.get("questions_specs", [])

        if not title or not questions_specs:
            return Response({"error": "title e questions_specs são obrigatórios."},
                            status=status.HTTP_400_BAD_REQUEST)

        specs_text = ""
        for i, spec in enumerate(questions_specs, 1):
            specs_text += (
                f"Questão {i}:\n"
                f"  - Tema/Conteúdo: {spec.get('content', '')}\n"
                f"  - Dificuldade: {spec.get('difficulty', 'medio')}\n"
                f"  - Tipo: {spec.get('type', 'dissertativa')}\n\n"
            )

        user_prompt = (
            f'Crie uma prova chamada "{title}" sobre {subject}.\n\n'
            f"Especificações por questão:\n{specs_text}"
        )

        try:
            data = call_openai(
                GENERATION_SYSTEM_PROMPT,
                user_prompt,
                temperature=0.8)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Erro na geração: %s", e)
            return Response({"error": "Falha ao gerar prova. Tente novamente."},
                            status=status.HTTP_502_BAD_GATEWAY)


# ─── Salvar prova gerada ────────────────────────────────────────────────

class SaveExamView(APIView):
    """POST /api/save-exam/  →  persiste Exam + Questions + Alternatives."""

    def post(self, request):
        title = request.data.get("title", "").strip()
        subject = request.data.get("subject", "").strip()
        desc = request.data.get("description", "").strip()
        questions = request.data.get("questions", [])

        if not title or not questions:
            return Response({"error": "title e questions são obrigatórios."},
                            status=status.HTTP_400_BAD_REQUEST)

        exam = Exam.objects.create(
            title=title,
            subject=subject,
            description=desc,
            is_active=True)

        for i, q_data in enumerate(questions, 1):
            q = Question.objects.create(
                exam=exam,
                order_num=i,
                statement=q_data.get("statement", ""),
                rubric=q_data.get("rubric", ""),
                question_type=q_data.get("question_type", "dissertativa"),
                difficulty=q_data.get("difficulty", "medio"),
            )
            for alt in q_data.get("alternatives", []):
                Alternative.objects.create(
                    question=q,
                    letter=alt.get("letter", "A"),
                    text=alt.get("text", ""),
                    is_correct=alt.get("is_correct", False),
                )

        return Response({"id": exam.id, "title": exam.title},
                        status=status.HTTP_201_CREATED)


# ─── Submissão + Feedback IA ────────────────────────────────────────────

class SubmitAnswerView(APIView):
    """POST /api/submissions/  →  grava resposta e retorna feedback da IA."""

    def post(self, request):
        question_id = request.data.get("question_id")
        answer_text = request.data.get("answer_text", "").strip()
        exam_id = request.data.get("exam_id")

        if not question_id or not answer_text:
            return Response(
                {
                    "error": "'question_id' e 'answer_text' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({"error": "Questão não encontrada."},
                            status=status.HTTP_404_NOT_FOUND)

        exam = None
        if exam_id:
            try:
                exam = Exam.objects.get(id=exam_id)
            except Exam.DoesNotExist:
                pass

        submission = Submission.objects.create(
            question=question, exam=exam, answer_text=answer_text
        )

        user_prompt = (
            f"Enunciado: {question.statement}\n"
            f"Rubrica: {question.rubric}\n"
            f"Resposta do Aluno: {answer_text}\n\n"
            "Corrija e retorne APENAS o JSON."
        )

        try:
            ai = call_openai(
                FEEDBACK_SYSTEM_PROMPT,
                user_prompt,
                temperature=0.4)
        except Exception as e:
            logger.exception("Erro no feedback: %s", e)
            return Response({"error": "Serviço de IA indisponível."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        feedback = Feedback.objects.create(
            submission=submission,
            score=ai.get("score", 0),
            key_strengths=ai.get("key_strengths", ""),
            areas_for_improvement=ai.get("areas_for_improvement", ""),
            constructive_feedback=ai.get("constructive_feedback", ""),
        )

        return Response(
            FeedbackSerializer(feedback).data,
            status=status.HTTP_201_CREATED)
