from django.shortcuts import render, get_object_or_404, redirect
from quizzerapp.models import Questionnaire, QuestionnairePage, Page, Question
from django.views.generic import View, ListView
from django.core.urlresolvers import reverse
from forms import QuestionsPageForm


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


def page_restrict(func):
    """Decorator for restricting questionnaire's page access."""
    def restrict(*args, **kwargs):
        # TODO make the checks

        return func(*args, **kwargs)

    return restrict


class PageView(View):
    def get(self, request, questionnaire_id, page_order):
        """GET method."""
        page_order = int(page_order)
        return self.render_page_questions(request, questionnaire_id, page_order)

    def post(self, request, questionnaire_id, page_order):
        """POST method."""
        page_order = int(page_order)
        q, p, qs = self.get_page_questions(questionnaire_id, page_order)
        form = QuestionsPageForm(request.POST, questions=qs)

        if form.is_valid():
            self.store_answers(request, questionnaire_id, form.cleaned_data)
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
        else:
            return self.render_page_questions_form(request, questionnaire_id, int(page_order), form)

    def store_answers(self, request, q_id, cleaned_data):
        q_key = q_id
        answers = request.session.get(q_key, [])
        current_answers = []
        for a in cleaned_data.values():
            if isinstance(a, list):
                current_answers.extend(a)
            else:
                current_answers.append(a)

        answers.extend(current_answers)
        request.session[q_key] = answers

    def get_page_questions(self, questionnaire_id, page_order):
        """Returns the Questionnaire, Questionnaire's Page and Page's Questions objects based on page order and
        questionnaire's id."""
        questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
        page = questionnaire.ordered_page(page_order)
        questions = page.ordered_questions

        return questionnaire, page, questions

    def render_page_questions(self, request, questionnaire_id, page_order):
        """Renders the page of questionnaire."""
        questionnaire, page, questions = self.get_page_questions(questionnaire_id, page_order)

        questions_form = QuestionsPageForm(questions=questions)

        context = {
            'questionnaire': questionnaire,
            'page': page,
            'questions_form': questions_form,
        }
        return render(request, 'page/answer.html', context)

    def render_page_questions_form(self, request, questionnaire_id, page_order, questions_form):
        questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
        page = questionnaire.ordered_page(page_order)

        context = {
            'questionnaire': questionnaire,
            'page': page,
            'questions_form': questions_form,
        }
        return render(request, 'page/answer.html', context)
