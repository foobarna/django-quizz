from django.shortcuts import render, get_object_or_404
from quizzerapp.models import Questionnaire, QuestionnairePage, Page, Question
from django.views.generic import View
from django.core.urlresolvers import reverse


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
    def get(self, request, questionnaire_id, page_order, *args, **kwargs):
        page_index = int(page_order) - 1
        questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
        page = Page.objects \
            .order_by('questionnairepage__weight') \
            .prefetch_related('questions') \
            .filter(questionnairepage__questionnaire=questionnaire)[page_index]
        questions = page.questions.prefetch_related('answer_set').all()

        total_pages = Page.objects.filter(questionnairepage__questionnaire=questionnaire).count()
        url_kwargs = {
            'questionnaire_id': questionnaire_id
        }
        if page_index + 1 == total_pages:
            url_next = reverse('quizzer:result', kwargs=url_kwargs)
        else:
            url_kwargs['page_order'] = str(page_index + 2)
            url_next = reverse('quizzer:page', kwargs=url_kwargs)

        context = {
            'questionnaire': questionnaire,
            'page': page,
            'questions': questions,
            'url_next': url_next,
        }

        return render(request, 'page/answer.html', context)

    def post(self, request, questionnaire_id, page_order, *args, **kwargs):
        page_index = int(page_order) - 1
        questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
        page = Page.objects \
            .order_by('questionnairepage__weight') \
            .prefetch_related('questions') \
            .filter(questionnairepage__questionnaire=questionnaire)[page_index]

        total_pages = Page.objects.filter(questionnairepage__questionnaire=questionnaire).count()
        url_kwargs = {
            'questionnaire_id': questionnaire_id
        }
        if page_index + 1 == total_pages:
            url_next = reverse('quizzer:result', kwargs=url_kwargs)
        else:
            url_kwargs['page_order'] = str(page_index + 2)
            url_next = reverse('quizzer:page', kwargs=url_kwargs)

        questions = page.questions.prefetch_related('answer_set').all()

        context = {
            'questionnaire': questionnaire,
            'page': page,
            'questions': questions,
            'url_next': url_next,
        }

        return render(request, 'page/answer.html', context)
