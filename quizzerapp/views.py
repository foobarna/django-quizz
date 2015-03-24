from django.shortcuts import render, get_object_or_404, redirect
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
    def render_page_questions(self, request, questionnaire_id, page_order, error_message=None, *args, **kwargs):
        page_index = int(page_order) - 1

        questionnaire = Questionnaire.objects.get(pk=questionnaire_id)

        page = Page.objects \
            .prefetch_related('questions') \
            .order_by('questionnairepage__weight') \
            .filter(questionnairepage__questionnaire=questionnaire) \
            .all()[page_index]

        questions = Question.objects \
            .prefetch_related('answer_set') \
            .order_by('pagequestion__weight') \
            .filter(pagequestion__page=page) \
            .all()

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
            'error_meesage': error_message,
        }

        return render(request, 'page/answer.html', context)

    def get(self, request, questionnaire_id, page_order, *args, **kwargs):
        return self.render_page_questions(request, questionnaire_id, page_order, args, kwargs)

    def post(self, request, questionnaire_id, page_order, *args, **kwargs):
        return self.render_page_questions(request, questionnaire_id, page_order, args, kwargs)
