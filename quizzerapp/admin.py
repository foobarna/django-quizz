from django.contrib import admin
from models import *

DEFAULT_EXTRA_INLINES = 3


# Inline models
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = DEFAULT_EXTRA_INLINES


class ResultInline(admin.TabularInline):
    model = Result
    extra = DEFAULT_EXTRA_INLINES
    ordering = ["-upper_limit"]


class QuestionnairePageInline(admin.TabularInline):
    model = QuestionnairePage
    extra = DEFAULT_EXTRA_INLINES
    ordering = ["weight"]


class PageQuestionInline(admin.TabularInline):
    model = PageQuestion
    extra = DEFAULT_EXTRA_INLINES
    ordering = ["weight"]


# Admin models
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, PageQuestionInline]
    list_display = ("question_text", "question_type")


class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [ResultInline, QuestionnairePageInline]


class PageAdmin(admin.ModelAdmin):
    inlines = [PageQuestionInline, QuestionnairePageInline]


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Page, PageAdmin)
