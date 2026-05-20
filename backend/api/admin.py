from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import Exam, Question, Alternative, Submission, Feedback


# ── Inlines ─────────────────────────────────────────────────────────────────

class AlternativeInline(admin.TabularInline):
    model = Alternative
    extra = 4
    max_num = 4
    fields = ("letter", "text", "is_correct")


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    show_change_link = True
    fields = (
        "order_num",
        "question_type",
        "difficulty",
        "statement",
        "rubric")
    inlines = []   # alternativas ficam na página da questão


# ── Question Admin ──────────────────────────────────────────────────────

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "order_num",
        "exam",
        "question_type",
        "difficulty",
        "__str__")
    list_filter = ("exam", "question_type", "difficulty")
    inlines = [AlternativeInline]
    fieldsets = (
        ("Questão", {"fields": ("exam", "order_num", "question_type", "difficulty", "statement")}),
        ("Rubrica (uso interno da IA)", {"fields": ("rubric",), "classes": ("collapse",)}),
    )


# ── Exam Admin ──────────────────────────────────────────────────────────

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "total_questions",
        "is_active",
        "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "subject")
    list_editable = ("is_active",)
    readonly_fields = ("created_at",)
    inlines = [QuestionInline]
    change_list_template = "admin/api/exam_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "generate/",
                self.admin_site.admin_view(self.generate_wizard_view),
                name="api_exam_generate",
            ),
        ]
        return custom + urls

    def add_view(self, request, form_url='', extra_context=None):
        return redirect("admin:api_exam_generate")

    def generate_wizard_view(self, request):
        """Serve a página do wizard de geração de provas."""
        context = dict(self.admin_site.each_context(request))
        return render(request, "admin/api/generate_exam.html", context)


# ── Submission / Feedback ───────────────────────────────────────────────

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "exam", "submitted_at")
    list_filter = ("exam",)
    readonly_fields = ("submitted_at",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "submission", "score", "generated_at")
    readonly_fields = ("generated_at",)
