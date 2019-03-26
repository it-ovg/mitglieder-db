from django.conf.urls import url, include
from django.urls import path, re_path
from django.contrib.auth.models import User
from rest_framework import routers
from knox import views as knox_views
from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'vereinsmitglieder', views.VereinsMitgliedViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'berufe', views.BerufeViewSet)
router.register(r'mitgliedsart', views.MitgliedsartViewSet)
router.register(r'kosten', views.KostenViewSet)
router.register(r'vortragsort', views.VortragsortViewSet)
router.register(r'adresse', views.AdresseViewSet)
router.register(r'institutionen', views.InstitutionenViewSet)
router.register(r'aboheft', views.AboHeftViewSet)
router.register(r'abonnent', views.AbonnentViewSet)
router.register(r'offeneposten', views.offenePostenViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^auth/register/$', views.RegistrationAPI.as_view()),
    url(r'^auth/login/$', views.LoginAPI.as_view()),
    url(r'^auth/user/$', views.UserAPI.as_view()),
    url(r'^auth/logout/$', knox_views.LogoutView.as_view()),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
