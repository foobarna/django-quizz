from django.shortcuts import render, get_object_or_404
from quizzerapp.models import Questionnaire, QuestionnairePage, Page, Question
from django.views.generic import View


# Create your views here.
def index(request):
    questionnaires = Questionnaire.objects.all()

    return render(request, 'questionnaire/index.html', {'questionnaires_list': questionnaires})


def questionnaire_start(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)

    return render(request, 'questionnaire/start.html', {'questionnaire': questionnaire})


def questionnaire_result(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)

    return render(request, 'questionnaire/result.html', {'questionnaire': questionnaire})


class PageView(View):
    def get(self, request, questionnaire_id, page_no, *args, **kwargs):
        questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
        page = Page.objects.filter(questionnairepage__questionnaire=questionnaire)[0]
        questions_list = Question.objects.filter(pagequestion_page=page)

        context = {'questionnaire': questionnaire, 'page': page, 'questions_list' : questions_list}

        return render(request, 'page/answer.html', context)

    def post(self, request, questionnaire_id, page_no, *args, **kwargs):
        pass
