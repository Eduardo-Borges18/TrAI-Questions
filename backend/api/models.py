from django.db import models
from django.contrib.auth.models import User


DIFFICULTY_CHOICES = [
    ("facil", "Fácil"),
    ("medio", "Médio"),
    ("dificil", "Difícil"),
]

QUESTION_TYPE_CHOICES = [
    ("dissertativa", "Dissertativa"),
    ("fechada", "Fechada (Múltipla Escolha)"),
]

LETTER_CHOICES = [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]


class Exam(models.Model):
    title = models.CharField(max_length=255, verbose_name="Título")
    subject = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Disciplina/Assunto")
    description = models.TextField(
        blank=True, verbose_name="Descrição para o aluno")
    is_active = models.BooleanField(default=False, verbose_name="Publicada?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Prova"
        verbose_name_plural = "Provas"

    def __str__(self):
        return self.title

    def total_questions(self):
        return self.questions.count()
    total_questions.short_description = "Questões"


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,
                             related_name="questions", verbose_name="Prova")
    order_num = models.PositiveIntegerField(default=1, verbose_name="Nº")
    statement = models.TextField(verbose_name="Enunciado")
    rubric = models.TextField(
        verbose_name="Rubrica (uso da IA)",
        help_text="Resposta esperada — não é exibida ao aluno.")
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default="dissertativa",
        verbose_name="Tipo")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES,
                                  default="medio", verbose_name="Dificuldade")

    class Meta:
        ordering = ["exam", "order_num"]
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

    def __str__(self):
        return f"Q{self.order_num} — {self.statement[:60]}"


class Alternative(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="alternatives",
        verbose_name="Questão")
    letter = models.CharField(max_length=1, choices=LETTER_CHOICES)
    text = models.TextField(verbose_name="Texto")
    is_correct = models.BooleanField(default=False, verbose_name="Correta?")

    class Meta:
        ordering = ["letter"]
        unique_together = [("question", "letter")]
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"

    def __str__(self):
        return f"{self.letter}) {self.text[:50]}"


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name="submissions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name="submissions")
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name="submissions")
    answer_text = models.TextField(verbose_name="Resposta")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Submissão"
        verbose_name_plural = "Submissões"

    def __str__(self):
        return f"Submissão #{self.pk}"


class Feedback(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE,
                                      related_name="feedback")
    score = models.DecimalField(max_digits=5, decimal_places=2,
                                null=True, blank=True, verbose_name="Nota")
    constructive_feedback = models.TextField(
        verbose_name="Feedback Construtivo")
    key_strengths = models.TextField(verbose_name="Pontos Fortes")
    areas_for_improvement = models.TextField(verbose_name="Pontos a Melhorar")
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return f"Feedback #{self.pk} — {self.score}"
