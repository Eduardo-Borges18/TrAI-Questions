from api.models import Question
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


print("OK - Todos os imports verificados com sucesso")
print(f"Questões no BD: {Question.objects.count()}")
