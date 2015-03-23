from django.conf.urls import patterns, url
from quizzerapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^questionnaire/(?P<questionnaire_id>[1-9][0-9]*)$', views.questionnaire_start, name='start'),
    url(r'^questionnaire/(?P<questionnaire_id>[1-9][0-9]*)/result$', views.questionnaire_result, name='result'),
    url(r'^questionnaire/(?P<questionnaire_id>[1-9][0-9]*)/page/(?P<page_order>[1-9][0-9]*)$', views.PageView.as_view(), name='page'),
)
