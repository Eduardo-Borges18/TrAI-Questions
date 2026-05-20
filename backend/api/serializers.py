from rest_framework import serializers
from .models import Exam, Question, Alternative, Submission, Feedback


class AlternativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternative
        fields = ["id", "letter", "text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    alternatives = AlternativeSerializer(many=True, read_only=True)
    difficulty_label = serializers.CharField(
        source="get_difficulty_display", read_only=True)
    question_type_label = serializers.CharField(
        source="get_question_type_display", read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "order_num",
            "statement",
            "question_type",
            "question_type_label",
            "difficulty",
            "difficulty_label",
            "alternatives"]


class ExamListSerializer(serializers.ModelSerializer):
    total_questions = serializers.SerializerMethodField()
    difficulty_label = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ["id", "title", "subject", "description", "total_questions",
                  "difficulty_label", "is_active", "created_at"]

    def get_total_questions(self, obj):
        return obj.questions.count()

    def get_difficulty_label(self, obj):
        # Pega a dificuldade da primeira questão como referência do nível da
        # prova
        q = obj.questions.first()
        return q.get_difficulty_display() if q else "—"


class ExamDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = [
            "id",
            "title",
            "subject",
            "description",
            "questions",
            "created_at"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "submission", "score", "constructive_feedback",
                  "key_strengths", "areas_for_improvement", "generated_at"]


class SubmissionSerializer(serializers.ModelSerializer):
    feedback = FeedbackSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id",
            "question",
            "exam",
            "answer_text",
            "submitted_at",
            "feedback"]
