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


class PageAnswerValidateException(Exception):
    """Exception for PageView."""
    pass


class PageView(View):
    def get(self, request, questionnaire_id, page_order, *args, **kwargs):
        """GET method."""
        page_order = int(page_order)
        return self.render_page_questions(request, questionnaire_id, page_order, args, kwargs)

    def post(self, request, questionnaire_id, page_order, *args, **kwargs):
        """POST method."""
        page_order = int(page_order)
        try:
            self.validate_answer(request.POST)
            total_pages = Page.objects.filter(questionnairepage__questionnaire__id=questionnaire_id).count()
            url_kwargs = {
                'questionnaire_id': questionnaire_id
            }
            if page_order == total_pages:
                url_next = reverse('quizzer:result', kwargs=url_kwargs)
            else:
                url_kwargs['page_order'] = page_order + 1
                url_next = reverse('quizzer:page', kwargs=url_kwargs)

            return redirect(url_next)
        except PageAnswerValidateException as ex:
            return self.render_page_questions(request, questionnaire_id, page_order, ex.message, args, kwargs)

    def get_page_questions(self, questionnaire_id, page_order):
        """Returns the Questionnaire, Questionnaire's Page and Page's Questions objects based on page order and
        questionnaire's id."""
        page_index = page_order - 1
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
        return questionnaire, page, questions

    def render_page_questions(self, request, questionnaire_id, page_order, error_message=None, *args, **kwargs):
        """Renders the page of questionnaire."""
        questionnaire, page, questions = self.get_page_questions(questionnaire_id, page_order)

        context = {
            'questionnaire': questionnaire,
            'page': page,
            'questions': questions,
            'error_message': error_message,
        }
        return render(request, 'page/answer.html', context)

    def render_page_result(self, request, questionnaire_id):
        """Renders the result page of questionnaire."""
        questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
        return render(request, 'questionnaire/result.html', {'questionnaire': questionnaire})

    def validate_answer(self, post_data):
        """Validates the user's input of a page questions."""
        # TODO: Rigorous validating for submitted data.
        if len(post_data) <= 1:
            raise PageAnswerValidateException("You must answer to all questions in order to continue.")
        return True
