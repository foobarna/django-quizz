from django import forms


class QuestionsPageForm(forms.Form):
    """Form for rendering a set of questions."""
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super(QuestionsPageForm, self).__init__(*args, **kwargs)
        for question in questions:
            self.fields[question.html_name] = question.form_field_type(
                label=question,
                required=True,
                widget=question.form_widget_type,
                choices=((answer.id, answer.answer_text) for answer in question.answer_set.all())
            )
