from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(QuestionPaper)
admin.site.register(QuizResults)
admin.site.register(Option)
admin.site.register(Instruction)
admin.site.register(Doubt)
admin.site.register(Answer)