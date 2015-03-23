from django.db import models

SHORT_TEXT = 200
MEDIUM_TEXT = 500
LONG_TEXT = 1000


class Question(models.Model):
    """Question model that has Questionnaire and Answer sets."""
    SINGLE = 'sg'
    MULTIPLE = 'mp'
    QUESTION_TYPE_CHOICES = (
        (SINGLE, 'Single answer'),
        (MULTIPLE, 'Multiple answers'),
    )
    question_text = models.CharField(max_length=MEDIUM_TEXT)
    question_type = models.CharField(max_length=2,
                                     choices=QUESTION_TYPE_CHOICES,
                                     default=SINGLE)

    def html_type(self):
        """Returns the html type of the question: radio or checkbox (default)."""
        html_types = {
            Question.SINGLE: "radio",
            Question.MULTIPLE: "checkbox",
        }
        return html_types.get(self.question_type, "checkbox")

    def __unicode__(self):
        return self.question_text


class Answer(models.Model):
    answer_text = models.CharField(max_length=MEDIUM_TEXT)
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return self.answer_text


class Page(models.Model):
    name = models.CharField(max_length=SHORT_TEXT)
    questions = models.ManyToManyField(Question, through="PageQuestion")

    def __unicode__(self):
        return self.name


class PageQuestion(models.Model):
    weight = models.IntegerField(default=0)
    page = models.ForeignKey(Page)
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return "%s : %s" % (self.page, self.question)

    class Meta:
        ordering = ["weight"]


class Questionnaire(models.Model):
    name = models.CharField(max_length=SHORT_TEXT)
    description = models.CharField(max_length=MEDIUM_TEXT)
    pages = models.ManyToManyField(Page, through="QuestionnairePage")

    def __unicode__(self):
        return self.name


class QuestionnairePage(models.Model):
    weight = models.IntegerField(default=0)
    questionnaire = models.ForeignKey(Questionnaire)
    page = models.ForeignKey(Page)

    def __unicode__(self):
        return "%s : %s" % (self.questionnaire, self.page)

    class Meta:
        ordering = ["weight"]


class Result(models.Model):
    result_text = models.CharField(max_length=LONG_TEXT)
    upper_limit = models.IntegerField(default=0)
    questionnaire = models.ForeignKey(Questionnaire)

    def __unicode__(self):
        return self.result_text
