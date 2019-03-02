# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'ovgmitglieder'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^editdata/(?P<obj>[\w]+)/(?P<pk>[0-9]+)/$', views.edit, name='edit'),
    url(r'^kontrollpunkt/(?P<ort>[\w]+)/$', views.kontrollpunkt, name='kontrollpunkt'),
    url(r'^saveform/(?P<obj>[\w]+)/(?P<pk>[0-9]+)/$', views.saveform, name='saveform'),
    url(r'^remove/(?P<obj>[\w]+)/(?P<pk>[0-9]+)/$', views.remove, name='remove'),
    url(r'^mitglieder/$', views.mitglieder, name='mitglieder'),
    url(r'^mitglieder/(?P<pk>[0-9]+)/$', views.mitglied_details, name='mitglied_details'),
    url(r'^mitglieder/(?P<obj>[\w]+)/(?P<pk>[0-9]+)/$', views.mitglieder, name='mitglied_filter'),
    url(r'^jubilare/$', views.jubilare, name='jubilare'),
    url(r'^land/$', views.land, name='land'),
    url(r'^beruf/$', views.beruf, name='beruf'),
    url(r'^mitgliedsart/$', views.mitgliedsart, name='mitgliedsart'),
    url(r'^mitgliedsbeitraege/$', views.mitgliedsbeitraege, name='mitgliedsbeitraege'),
    url(r'^mitgliedsbeitraege_neu/$', views.mitgliedsbeitraege_neu, name='mitgliedsbeitraege_neu'),
    url(r'^kosten/$', views.kosten, name='kosten'),
    url(r'^vgiuebersicht/$', views.vgiuebersicht, name='vgiuebersicht'),
    url(r'^emails_ausschicken/(?P<pk>[0-9]+)/$', views.emails_ausschicken, name='emails_ausschicken'),
    url(r'^beitragbezahlen/(?P<uuid>[0-9a-f\-]{36})/$', views.beitragbezahlen, name='beitragbezahlen'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
