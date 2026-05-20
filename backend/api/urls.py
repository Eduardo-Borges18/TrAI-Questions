from django.urls import path
from .views import (
    ExamListView, ExamDetailView,
    GenerateExamView, SaveExamView,
    SubmitAnswerView,
)

urlpatterns = [
    path("exams/", ExamListView.as_view(), name="exam-list"),
    path("exams/<int:pk>/", ExamDetailView.as_view(), name="exam-detail"),
    path("generate-exam/", GenerateExamView.as_view(), name="generate-exam"),
    path("save-exam/", SaveExamView.as_view(), name="save-exam"),
    path("submissions/", SubmitAnswerView.as_view(), name="submit-answer"),
]
